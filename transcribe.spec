# -*- mode: python ; coding: utf-8 -*-

import os
import whisper

# Get the path to whisper assets
whisper_path = os.path.dirname(whisper.__file__)
assets_path = os.path.join(whisper_path, 'assets')

a = Analysis(
    ['transcribe.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('myth', 'myth'),
        (assets_path, 'whisper/assets')
    ],
    hiddenimports=[
        'whisper',
        'whisper.audio',
        'whisper.transcribe',
        'whisper.model',
        'torch',
        'torch.nn',
        'torchvision',
        'torchaudio',
        'pygame',
        'numpy',
        'pkg_resources',
        'tiktoken',
        'tqdm',
        'whisper.tokenizer'
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
    a.binaries,
    a.datas,
    [],
    name='transcribe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)