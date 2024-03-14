#!/usr/bin/env bash
set -e
set -u

# Create venv
python3 -m venv .venv

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install modules
pip install -r requirements.txt

# Deactivate venv
deactivate

