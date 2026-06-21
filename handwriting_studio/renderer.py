from __future__ import annotations

import io
import random
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


A4_150_DPI = (1240, 1754)
A4_300_DPI = (2480, 3508)


@dataclass(frozen=True)
class RenderSettings:
    font_path: str
    font_size: int = 52
    ink_color: str = "#173B70"
    page_size: tuple[int, int] = A4_150_DPI
    margin_left: int = 100
    margin_right: int = 100
    margin_top: int = 110
    margin_bottom: int = 110
    line_spacing: int = 18
    paragraph_spacing: int = 24
    line_jitter: int = 3
    word_jitter: int = 2
    rotation_jitter: float = 0.35
    paper_style: str = "plain"
    seed: int = 7


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _paper(settings: RenderSettings) -> Image.Image:
    width, height = settings.page_size
    image = Image.new("RGB", (width, height), "#FFFEFA")
    draw = ImageDraw.Draw(image)

    if settings.paper_style == "lined":
        step = max(settings.font_size + settings.line_spacing, 36)
        y = settings.margin_top + settings.font_size
        while y < height - settings.margin_bottom:
            draw.line((0, y, width, y), fill="#C9D8EB", width=max(1, width // 1200))
            y += step
        draw.line(
            (settings.margin_left - 22, 0, settings.margin_left - 22, height),
            fill="#E8B9B9",
            width=max(1, width // 1000),
        )
    elif settings.paper_style == "grid":
        step = max(settings.font_size + settings.line_spacing, 36)
        for x in range(0, width, step):
            draw.line((x, 0, x, height), fill="#E2EAF3", width=1)
        for y in range(0, height, step):
            draw.line((0, y, width, y), fill="#E2EAF3", width=1)

    return image


def _font(settings: RenderSettings) -> ImageFont.FreeTypeFont:
    path = Path(settings.font_path)
    if not path.is_file():
        raise FileNotFoundError(f"Font not found: {path}")
    return ImageFont.truetype(str(path), settings.font_size)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_paragraph(
    paragraph: str,
    draw: ImageDraw.ImageDraw,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    if not paragraph:
        return [""]

    lines: list[str] = []
    current = ""
    for word in paragraph.split(" "):
        candidate = word if not current else f"{current} {word}"
        if _text_width(draw, candidate, font) <= max_width:
            current = candidate
            continue

        if current:
            lines.append(current)
            current = ""

        if _text_width(draw, word, font) <= max_width:
            current = word
            continue

        fragment = ""
        for char in word:
            candidate = f"{fragment}{char}"
            if fragment and _text_width(draw, candidate, font) > max_width:
                lines.append(fragment)
                fragment = char
            else:
                fragment = candidate
        current = fragment

    if current:
        lines.append(current)
    return lines


def _draw_natural_line(
    page: Image.Image,
    line: str,
    x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    settings: RenderSettings,
    rng: random.Random,
) -> None:
    cursor = x + rng.randint(-settings.line_jitter, settings.line_jitter)
    words = line.split(" ")

    for index, word in enumerate(words):
        token = word if index == len(words) - 1 else f"{word} "
        box = font.getbbox(token)
        width = max(1, box[2] - box[0] + settings.word_jitter * 4)
        height = max(settings.font_size * 2, box[3] - box[1] + settings.word_jitter * 8)
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        layer_draw.text(
            (settings.word_jitter * 2, settings.word_jitter * 2 - box[1]),
            token,
            font=font,
            fill=settings.ink_color,
        )

        angle = rng.uniform(-settings.rotation_jitter, settings.rotation_jitter)
        if angle:
            layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

        offset_y = rng.randint(-settings.word_jitter, settings.word_jitter)
        page.paste(layer, (cursor, y + offset_y), layer)
        cursor += _text_width(ImageDraw.Draw(page), token, font)
        cursor += rng.randint(-settings.word_jitter, settings.word_jitter)


def render_document(text: str, settings: RenderSettings) -> list[Image.Image]:
    text = normalize_text(text)
    if not text:
        raise ValueError("Text is empty.")

    font = _font(settings)
    probe = _paper(settings)
    probe_draw = ImageDraw.Draw(probe)
    usable_width = settings.page_size[0] - settings.margin_left - settings.margin_right
    line_height = settings.font_size + settings.line_spacing

    flow: list[tuple[str, bool]] = []
    paragraphs = text.split("\n")
    for paragraph_index, paragraph in enumerate(paragraphs):
        for line in wrap_paragraph(paragraph, probe_draw, font, usable_width):
            flow.append((line, False))
        if paragraph_index != len(paragraphs) - 1:
            flow.append(("", True))

    rng = random.Random(settings.seed)
    pages: list[Image.Image] = []
    page = _paper(settings)
    y = settings.margin_top
    page_bottom = settings.page_size[1] - settings.margin_bottom

    for line, paragraph_break in flow:
        advance = settings.paragraph_spacing if paragraph_break else line_height
        if y + advance > page_bottom:
            pages.append(page)
            page = _paper(settings)
            y = settings.margin_top

        if line:
            _draw_natural_line(
                page,
                line,
                settings.margin_left,
                y,
                font,
                settings,
                rng,
            )
        y += advance

    pages.append(page)
    return pages


def render_pdf(pages: list[Image.Image], dpi: int = 150) -> bytes:
    if not pages:
        raise ValueError("No pages to export.")
    output = io.BytesIO()
    rgb_pages = [page.convert("RGB") for page in pages]
    rgb_pages[0].save(
        output,
        format="PDF",
        save_all=True,
        append_images=rgb_pages[1:],
        resolution=float(dpi),
    )
    return output.getvalue()

