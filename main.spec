# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('base3_1.db', '.'), ('bunker.png', '.'), ('bunker.ico', '.')],
    hiddenimports=['uvicorn', 'server', 'sozdat', 'connect', 'rules', 'okno4', 'okno5', 'okno6', 'okno7', 'okno8', 'okno9', 'okno10', 'left_window', 'right_window1', 'right_window2'],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bunker.png'],
)
