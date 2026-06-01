#!/bin/bash
# Build GroqTranslate.app for macOS distribution

set -e

echo "🔨 Building GroqTranslate..."

# Install dependencies
pip3 install -r requirements.txt
pip3 install pyinstaller

# Build .app bundle
pyinstaller \
  --name "GroqTranslate" \
  --windowed \
  --onedir \
  --icon=../web/public/icon.icns \
  --add-data "*.py:." \
  --hidden-import rumps \
  --hidden-import pynput \
  --hidden-import groq \
  --osx-bundle-identifier "sk.alukim.groq-translate" \
  main.py

echo "✅ Build complete: dist/GroqTranslate.app"

# Create DMG
if command -v create-dmg &> /dev/null; then
  create-dmg \
    --volname "GroqTranslate" \
    --window-size 600 400 \
    --icon-size 128 \
    --app-drop-link 450 185 \
    "dist/GroqTranslate.dmg" \
    "dist/GroqTranslate.app"
  echo "✅ DMG: dist/GroqTranslate.dmg"
else
  echo "ℹ️  Nainštaluj create-dmg pre .dmg balík: brew install create-dmg"
  # Simple zip fallback
  cd dist && zip -r GroqTranslate.zip GroqTranslate.app
  echo "✅ ZIP: dist/GroqTranslate.zip"
fi
