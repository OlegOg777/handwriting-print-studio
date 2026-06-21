from __future__ import annotations

import io
import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
from docx import Document

from handwriting_studio import RenderSettings, render_document, render_pdf


APP_DIR = Path(__file__).resolve().parent
FONT_DIR = APP_DIR / "fonts"


@st.cache_data(show_spinner=False)
def discover_fonts() -> dict[str, str]:
    fonts: dict[str, str] = {}
    free_font_names = {
        "01-BadScript-Regular": "Рукописный 1 - Bad Script",
        "02-Caveat-Regular": "Рукописный 2 - Caveat",
        "03-MarckScript-Regular": "Рукописный 3 - Marck Script",
        "04-Neucha-Regular": "Рукописный 4 - Neucha",
        "05-Pacifico-Regular": "Рукописный 5 - Pacifico",
        "06-Lobster-Regular": "Рукописный 6 - Lobster",
        "07-AmaticSC-Regular": "Рукописный 7 - Amatic SC",
        "08-Pangolin-Regular": "Рукописный 8 - Pangolin",
        "09-SwankyAndMooMoo-Regular": "Рукописный 9 - Swanky and Moo Moo",
        "10-KellySlab-Regular": "Рукописный 10 - Kelly Slab",
    }

    if FONT_DIR.exists():
        for extension in ("*.ttf", "*.otf", "*.ttc"):
            for path in FONT_DIR.glob(extension):
                label = free_font_names.get(path.stem, f"Мой шрифт - {path.stem}")
                fonts[label] = str(path)

    priority = {
        "Рукописный 1 - Bad Script": 1,
        "Рукописный 2 - Caveat": 2,
        "Рукописный 3 - Marck Script": 3,
        "Рукописный 4 - Neucha": 4,
        "Рукописный 5 - Pacifico": 5,
        "Рукописный 6 - Lobster": 6,
        "Рукописный 7 - Amatic SC": 7,
        "Рукописный 8 - Pangolin": 8,
        "Рукописный 9 - Swanky and Moo Moo": 9,
        "Рукописный 10 - Kelly Slab": 10,
    }
    return dict(
        sorted(
            fonts.items(),
            key=lambda item: (priority.get(item[0], 100), item[0].lower()),
        )
    )


def read_text(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()
    if suffix == ".txt":
        for encoding in ("utf-8-sig", "utf-8", "cp1251"):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("Не удалось определить кодировку TXT.")
    if suffix == ".docx":
        document = Document(io.BytesIO(data))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("Поддерживаются только TXT и DOCX.")


def page_zip(pages) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for index, page in enumerate(pages, start=1):
            image = io.BytesIO()
            page.save(image, format="PNG")
            archive.writestr(f"page-{index:03d}.png", image.getvalue())
    return output.getvalue()


st.set_page_config(
    page_title="Handwriting Print Studio",
    page_icon="✍",
    layout="wide",
)

st.title("Handwriting Print Studio")
st.caption("Подготовка текста для аккуратной печати в рукописном стиле")

fonts = discover_fonts()
if not fonts:
    st.error(
        "Рукописные шрифты не найдены. Перезапустите программу через "
        "Запустить_на_Mac.command или Запустить_на_Windows.bat."
    )
    st.stop()

with st.sidebar:
    st.subheader("Оформление")
    uploaded_font = st.file_uploader("Добавить свой шрифт", type=["ttf", "otf"])
    selected_font = st.selectbox(
        "Рукописный шрифт",
        list(fonts),
        help="Все десять вариантов поддерживают русский язык.",
    )
    font_size = st.slider("Размер", 24, 92, 52)
    ink_color = st.color_picker("Цвет чернил", "#173B70")
    paper_label = st.selectbox("Бумага", ["Чистый лист", "Линейка", "Клетка"])
    line_spacing = st.slider("Интервал строк", 4, 48, 18)
    margin = st.slider("Поля", 40, 220, 100)

    st.subheader("Естественность")
    line_jitter = st.slider("Сдвиг строк", 0, 10, 3)
    rotation_jitter = st.slider("Наклон строки", 0.0, 1.0, 0.15, 0.05)
    seed = st.number_input("Вариант результата", 1, 9999, 7)

uploaded_text = st.file_uploader("Загрузить текст", type=["txt", "docx"])
default_text = (
    "Введите или загрузите текст. Программа автоматически перенесёт строки, "
    "разделит документ на страницы A4 и подготовит PDF для печати."
)

if "editor_text" not in st.session_state:
    st.session_state.editor_text = default_text

if uploaded_text is not None:
    signature = (uploaded_text.name, uploaded_text.size)
    if st.session_state.get("upload_signature") != signature:
        try:
            st.session_state.editor_text = read_text(uploaded_text)
            st.session_state.upload_signature = signature
        except ValueError as error:
            st.error(str(error))

text = st.text_area("Текст", key="editor_text", height=260)

font_path = fonts[selected_font]
temporary_font = None
if uploaded_font is not None:
    suffix = Path(uploaded_font.name).suffix.lower()
    temporary_font = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temporary_font.write(uploaded_font.getvalue())
    temporary_font.close()
    font_path = temporary_font.name

paper_styles = {
    "Чистый лист": "plain",
    "Линейка": "lined",
    "Клетка": "grid",
}

settings = RenderSettings(
    font_path=font_path,
    font_size=font_size,
    ink_color=ink_color,
    margin_left=margin,
    margin_right=margin,
    margin_top=margin,
    margin_bottom=margin,
    line_spacing=line_spacing,
    line_jitter=line_jitter,
    word_jitter=0,
    rotation_jitter=rotation_jitter,
    paper_style=paper_styles[paper_label],
    seed=int(seed),
)

try:
    pages = render_document(text, settings)
except (ValueError, FileNotFoundError, OSError) as error:
    st.error(str(error))
    pages = []

if temporary_font is not None:
    try:
        os.unlink(temporary_font.name)
    except OSError:
        pass

if pages:
    st.success(f"Подготовлено страниц: {len(pages)}")
    preview_column, action_column = st.columns([3, 1])

    with preview_column:
        page_number = st.number_input(
            "Страница предпросмотра",
            1,
            len(pages),
            1,
        )
        st.image(pages[int(page_number) - 1], width="stretch")

    with action_column:
        st.download_button(
            "Скачать PDF",
            render_pdf(pages),
            file_name="handwriting-document.pdf",
            mime="application/pdf",
            width="stretch",
        )
        st.download_button(
            "Скачать страницы PNG",
            page_zip(pages),
            file_name="handwriting-pages.zip",
            mime="application/zip",
            width="stretch",
        )
