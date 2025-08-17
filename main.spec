# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['F:\研究生\chemistry\high_energy_explosive'],
    binaries=[],
    datas=[],
    hiddenimports=[
    'material_pile.calc_box',
    'material_pile.calc_circular',
    'material_pile.calc_concentricball',
    'material_pile.calc_inner_circular',
    'material_pile.calc_mixed_circular',
    'material_pile.calc_net_ball',
    'micro.gui',
    'jwl.jwl_gui',
    'jwl.jwl_yt_final_gui',
    'water.bubble_gui',
    'water.energy_gui',
    'yt.plot_vx_gui'
],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
