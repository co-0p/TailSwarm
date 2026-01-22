#!/bin/bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# Clean up
rm -rf site-packages tailswarm
# Install reqs to tmp directory
pip install --target ./site-packages -r requirements.txt
# Copy your entire project structure (including local modules)
cp -r ./* ./site-packages/  # Copies tailswarm.py + all local modules/packages
# Build pyz from site-packages dir
shiv \
  --site-packages ./site-packages/ \
  -e tailswarm:cli -o \
  "./tailswarm" \
  -p '/usr/bin/env python3' --compressed
# Clean up
rm -rf site-packages