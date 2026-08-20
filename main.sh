#!/bin/bash

case "$1" in
    -h|-H|--help|--Help|--HELP)
        echo "Usage: ./main.sh [LAN=True]"
        echo "  LAN=True  Serve the site to devices on your local network"
        exit 0
        ;;
esac

# Run local-only setup if it exists (in this case, it disables IPv6, which is erronously being used while Tailscale is active, causing timeout failures with Bootdev servers)
#if [ -f "./local_setup.sh" ]; then
#    source ./local_setup.sh
#fi


python3 src/main.py

if [ "$1" = "LAN=True" ]; then
    python3 -m http.server 8888 --bind 0.0.0.0 --directory public
else
    python3 -m http.server 8888 --bind 127.0.0.1 --directory public
fi