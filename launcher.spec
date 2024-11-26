# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        (
            "./.venv/Lib/site-packages/streamlit",
            "./streamlit"
        ),
        (
            "./.venv/Scripts/streamlit.exe",
            "./Scripts/"
        ),
        (
            "./.venv/Lib/site-packages/",
            "."
        ),
        (
            "./application",
            "./application"
        )
    ],
    hiddenimports=[
        "streamlit"
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
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
    upx=True,
    upx_exclude=[],
    name='launcher',
)