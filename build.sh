#!/bin/bash
# Build script for Network AI Agent on Linux/macOS
# This script creates an executable and installer

set -e

echo ""
echo "========================================================="
echo "Network AI Agent - Build Script"
echo "========================================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or later"
    exit 1
fi

echo "[1/3] Installing build dependencies..."
pip install -r requirements-build.txt

echo "[2/3] Building executable..."
python3 build_installer.py

echo ""
echo "========================================================="
echo "Build Complete!"
echo "========================================================="
echo ""
echo "Output Files:"
echo "  - Executable: dist/NetworkAIAgent/NetworkAIAgent"
echo ""
echo "Configuration:"
echo "  1. Copy .env.example to .env"
echo "  2. Add your OpenAI API key to .env"
echo "  3. Update config/config.yaml with your device settings"
echo "  4. Run: ./dist/NetworkAIAgent/NetworkAIAgent"
echo ""
