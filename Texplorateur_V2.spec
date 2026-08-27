# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['Texplorateur_V2.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('customtkinter') + [
        # image.ico : repris ici pour l'icône de la fenêtre à l'exécution
        # (root.iconbitmap), en plus de son usage plus bas comme icône du
        # .exe lui-même — ce sont deux mécanismes séparés.
        ('image.ico', '.'),
        # Fichiers de traduction, sans quoi le sélecteur de langue de
        # Paramètres n'aurait rien à charger une fois l'app compilée.
        ('texplorateur/locales', 'texplorateur/locales'),
    ],
    hiddenimports=['openpyxl', 'customtkinter'],
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
    name='Texplorateur_V2',
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
    icon=['image.ico'],
)
