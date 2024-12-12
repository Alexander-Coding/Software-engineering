# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/images', 'assets/images'),
        ('assets/musics', 'assets/musics'),
        ('assets/sounds', 'assets/sounds'),
        ('src', 'src'),
        ('levels', 'levels'),
        ('save_data.json', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

from PyInstaller.utils.hooks import collect_all
datas, binaries, hiddenimports = collect_all('src')

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Super Mario-style',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='Super Mario-style',
)
