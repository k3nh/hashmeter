#!/bin/bash

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install required libraries
uv pip install tdigest
uv pip install asyncio
uv pip install uvloop

# Deactivate the virtual environment
deactivate
