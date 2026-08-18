#!/bin/bash

# Run local-only setup if it exists (won't exist on other machines/CI)
if [ -f "./local_setup.sh" ]; then
    source ./local_setup.sh
fi




python3 src/main.py
cd public && python3 -m http.server 8888