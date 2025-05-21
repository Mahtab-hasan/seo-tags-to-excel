# Marked as executable

#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (no root access required)
python -m playwright install
