#!/usr/bin/env bash

# Install system dependencies needed for Playwright browsers
apt-get update && apt-get install -y \
  libgtk-4-1 \
  libgraphene-1.0-0 \
  libgstgl-1.0-0 \
  libgstcodecparsers-1.0-0 \
  libavif15 \
  libenchant-2-2 \
  libsecret-1-0 \
  libmanette-0.2-0 \
  libgles2

# Install dependencies (if not using Poetry)
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps