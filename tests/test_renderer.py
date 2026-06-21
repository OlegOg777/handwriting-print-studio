from pathlib import Path

from handwriting_studio.renderer import RenderSettings, render_document, render_pdf


FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
]


def test_render_document_and_pdf():
    font = next((path for path in FONT_CANDIDATES if path.exists()), None)
    if font is None:
        return

    settings = RenderSettings(
        font_path=str(font),
        font_size=36,
        page_size=(620, 877),
        margin_left=50,
        margin_right=50,
        margin_top=50,
        margin_bottom=50,
        line_spacing=10,
    )
    text = ("Проверка генератора рукописного текста. " * 80).strip()
    pages = render_document(text, settings)

    assert len(pages) >= 2
    assert pages[0].size == (620, 877)
    assert render_pdf(pages).startswith(b"%PDF")

