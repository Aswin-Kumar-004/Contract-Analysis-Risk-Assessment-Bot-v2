#!/bin/bash

# Contract Risk Bot - Installation Script
# For Linux/Mac

echo "🚀 Installing Contract Risk Bot..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
echo "✓ Python version: $python_version"

# Install requirements
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Download spaCy model
echo ""
echo "📥 Downloading spaCy English model..."
python3 -m spacy download en_core_web_sm

# Check API key
echo ""
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "To use AI features, set your API key:"
    echo "  export ANTHROPIC_API_KEY='your_key_here'"
    echo ""
    echo "Get your API key from: https://console.anthropic.com/"
    echo ""
else
    echo "✓ ANTHROPIC_API_KEY is configured"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run the app:"
echo "  streamlit run app.py"
echo ""
echo "Or for Windows:"
echo "  python -m streamlit run app.py"
echo ""
