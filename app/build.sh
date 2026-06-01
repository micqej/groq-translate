#!/bin/bash
# Build AlukimTranslate.app for macOS distribution

set -e

echo "🔨 Building AlukimTranslate..."

# Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build .app bundle
pyinstaller \
  --name "AlukimTranslate" \
  --windowed \
  --onedir \
  --icon=../web/public/icon.icns \
  --add-data "*.py:." \
  --hidden-import rumps \
  --hidden-import pynput \
  --hidden-import groq \
  --osx-bundle-identifier "sk.alukim.alukim-translate" \
  main.py

echo "✅ Build complete: dist/AlukimTranslate.app"

# Create DMG
if command -v create-dmg &> /dev/null; then
  create-dmg \
    --volname "AlukimTranslate" \
    --window-size 600 400 \
    --icon-size 128 \
    --app-drop-link 450 185 \
    "dist/AlukimTranslate.dmg" \
    "dist/AlukimTranslate.app"
  echo "✅ DMG: dist/AlukimTranslate.dmg"
else
  echo "ℹ️  Nainštaluj create-dmg pre .dmg balík: brew install create-dmg"
  # Simple zip fallback
  cd dist && zip -r AlukimTranslate.zip AlukimTranslate.app
  echo "✅ ZIP: dist/AlukimTranslate.zip"
fi
