#!/bin/bash
# GroqTranslate — jednoduchá inštalácia
set -e

echo ""
echo "⚡ GroqTranslate Inštalátor"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nie je nainštalovaný."
    echo "   Nainštaluj ho z: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION nájdený"

# Install dependencies
echo ""
echo "📦 Inštalujem závislosti..."
pip3 install -r "$(dirname "$0")/requirements.txt" --quiet

echo "✓ Závislosti nainštalované"
echo ""
echo "🚀 Spúšťam GroqTranslate..."
echo ""
echo "ℹ️  Pri prvom spustení:"
echo "   1. Povoľ Accessibility permission (pre skratky)"
echo "   2. Povoľ Screen Recording permission (pre OCR)"
echo "   3. Klikni na ⚡ v menu bare → Nastavenia → vlož Groq API kľúč"
echo ""

python3 "$(dirname "$0")/main.py"
