from PyInstaller.utils.hooks import collect_all


streamlit_data, streamlit_binaries, streamlit_hidden = collect_all("streamlit")
altair_data, altair_binaries, altair_hidden = collect_all("altair")

datas = [
    ("app.py", "."),
    ("handwriting_studio", "handwriting_studio"),
    ("fonts", "fonts"),
    ("samples", "samples"),
]
datas += streamlit_data + altair_data

a = Analysis(
    ["desktop_launcher.py"],
    pathex=[],
    binaries=streamlit_binaries + altair_binaries,
    datas=datas,
    hiddenimports=streamlit_hidden + altair_hidden + [
        "docx",
        "PIL",
        "PIL.Image",
        "PIL.ImageDraw",
        "PIL.ImageFont",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Handwriting Print Studio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Handwriting Print Studio",
)

