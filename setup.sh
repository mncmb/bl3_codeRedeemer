#!/bin/bash
if [ ! -d "bin" ]; then
    python3 -m venv .
fi
source bin/activate
echo
echo "Current python binary in use"
which python
echo
pip3 install -r requirements.txt