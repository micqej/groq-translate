# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'rumps',
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'groq',
        'groq._client',
        'httpx',
        'anyio',
        'certifi',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'sqlite3',
        'json',
        'threading',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AlukimTranslate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AlukimTranslate',
)

app = BUNDLE(
    coll,
    name='AlukimTranslate.app',
    icon=None,
    bundle_identifier='sk.alukim.translate',
    info_plist={
        'CFBundleName': 'AlukimTranslate',
        'CFBundleDisplayName': 'AlukimTranslate',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': True,  # menu bar only app, no Dock icon
        'NSAccessibilityUsageDescription': 'AlukimTranslate potrebuje Accessibility pre globálne klávesové skratky.',
        'NSScreenCaptureDescription': 'AlukimTranslate potrebuje Screen Recording pre OCR funkciu.',
    },
)
