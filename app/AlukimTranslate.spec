# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('menubar_icon.png', '.')],
    hiddenimports=[
        'rumps',
        'groq',
        'httpx',
        'anyio',
        'certifi',
        'sqlite3',
        'Quartz',
        'CoreFoundation',
        'objc',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', '_tkinter', 'pynput'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Prekladac',
    debug=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='Prekladac',
)

app = BUNDLE(
    coll,
    name='Prekladac.app',
    icon=None,
    bundle_identifier='sk.alukim.prekladac',
    info_plist={
        'CFBundleName': 'Prekladac',
        'CFBundleDisplayName': 'Prekladac',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': True,
        'NSAccessibilityUsageDescription': 'Prekladač potrebuje Accessibility pre globálne skratky.',
        'NSScreenCaptureUsageDescription': 'Prekladač potrebuje Screen Recording pre OCR.',
        'NSAppleEventsUsageDescription': 'Prekladač zobrazuje dialógy.',
    },
)
