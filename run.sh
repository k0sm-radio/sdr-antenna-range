#!/bin/bash
# Convenience script: regenerate pluto.py from the GRC flowgraph, patch in
# the async message connection GRC doesn't generate for embedded Python
# blocks, then run it. Works from any directory and on macOS or Linux.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

grcc pluto-antenna-range.grc
python3 fix_msg_connection.py
python3 pluto.py
