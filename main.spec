# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Dodajemy ffmpeg do paczki (folder 'ffmpeg/bin/ffmpeg')
datas = [
    ('ffmpeg/bin/ffmpeg', 'ffmpeg/bin'),  # (źródło, miejsce w strukturze .exe)
]

# Tworzymy analizę projektu
a = Analysis(
    ['main.py'],
    pathex=['.'],  # katalog źródłowy
    binaries=[
        ('/home/mrst4sio/./INF/Code/Python/yt_downloader/dist/yt_downloader/_internal/libpython3.12.so', '.'),
    ],
    datas=datas,
    hiddenimports=collect_submodules('yt_dlp'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='yt_downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Zmień na False jeśli chcesz ukryć konsolę (np. GUI)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='yt_downloader'
)
