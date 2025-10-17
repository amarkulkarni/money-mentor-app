#!/bin/bash
# MoneyMentor - Qdrant Setup Script (No Docker Required)

set -e

echo "============================================================"
echo "MoneyMentor - Qdrant Setup (Standalone Binary)"
echo "============================================================"
echo ""

# Detect architecture
ARCH=$(uname -m)
OS=$(uname -s)

echo "Detected system: $OS ($ARCH)"
echo ""

# Determine download URL
if [ "$OS" = "Darwin" ]; then
    if [ "$ARCH" = "arm64" ]; then
        echo "📥 Downloading Qdrant for Apple Silicon (M1/M2/M3)..."
        DOWNLOAD_URL="https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz"
    elif [ "$ARCH" = "x86_64" ]; then
        echo "📥 Downloading Qdrant for Intel Mac..."
        DOWNLOAD_URL="https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-apple-darwin.tar.gz"
    else
        echo "❌ Unsupported architecture: $ARCH"
        exit 1
    fi
elif [ "$OS" = "Linux" ]; then
    if [ "$ARCH" = "x86_64" ]; then
        echo "📥 Downloading Qdrant for Linux (x86_64)..."
        DOWNLOAD_URL="https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-musl.tar.gz"
    elif [ "$ARCH" = "aarch64" ]; then
        echo "📥 Downloading Qdrant for Linux (ARM64)..."
        DOWNLOAD_URL="https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-unknown-linux-musl.tar.gz"
    else
        echo "❌ Unsupported architecture: $ARCH"
        exit 1
    fi
else
    echo "❌ Unsupported OS: $OS"
    exit 1
fi

# Download
if [ -f "qdrant" ]; then
    echo "⚠️  Qdrant binary already exists. Remove it first if you want to re-download."
    echo ""
else
    curl -L "$DOWNLOAD_URL" -o qdrant.tar.gz
    echo "✅ Downloaded"
    echo ""
    
    # Extract
    echo "📦 Extracting..."
    tar xzf qdrant.tar.gz
    rm qdrant.tar.gz
    echo "✅ Extracted"
    echo ""
fi

# Make executable
chmod +x qdrant

echo "✅ Qdrant is ready!"
echo ""
echo "To start Qdrant:"
echo "  ./qdrant"
echo ""
echo "To run in background:"
echo "  nohup ./qdrant > qdrant.log 2>&1 &"
echo ""
echo "To check if running:"
echo "  curl http://localhost:6333"
echo ""
echo "To stop:"
echo "  pkill qdrant"
echo ""
echo "============================================================"

