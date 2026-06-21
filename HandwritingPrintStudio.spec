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

binaries = streamlit_binaries + altair_binaries
hiddenimports = streamlit_hidden + altair_hidden + [
    "docx",
    "PIL",
    "PIL.Image",
    "PIL.ImageDraw",
    "PIL.ImageFont",
]

a = Analysis(
    ["desktop_launcher.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
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

app = BUNDLE(
    coll,
    name="Handwriting Print Studio.app",
    icon=None,
    bundle_identifier="com.olegog777.handwritingprintstudio",
    version="0.2.1",
    info_plist={
        "CFBundleDisplayName": "Handwriting Print Studio",
        "CFBundleName": "Handwriting Print Studio",
        "CFBundleShortVersionString": "0.2.1",
        "CFBundleVersion": "3",
        "LSMinimumSystemVersion": "12.0",
        "NSHighResolutionCapable": True,
    },
)
