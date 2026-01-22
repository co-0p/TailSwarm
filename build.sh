#!/bin/bash
set -euo pipefail

# Clean up
rm -rf site-packages tailswarm
# Install reqs to tmp directory
pip install --target ./site-packages -r tailswarm_src/requirements.txt
# Copy your entire project structure (including local modules)
cp -r ./tailswarm_src/* ./site-packages/  # Copies tailswarm.py + all local modules/packages
# Build pyz from site-packages dir
shiv \
  --site-packages ./site-packages/ \
  -e tailswarm:cli -o \
  "./tailswarm" \
  -p '/usr/bin/env python3' --compressed