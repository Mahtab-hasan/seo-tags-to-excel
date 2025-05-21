#!/usr/bin/env bash

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright browsers..."
python -m playwright install chromium

echo "✅ Build script completed."
