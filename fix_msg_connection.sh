#!/bin/bash
# Compatibility shim - the real patching logic now lives in
# fix_msg_connection.py (plain Python 3, works identically on macOS,
# Linux, and Windows). This wrapper exists so anything that still calls
# ./fix_msg_connection.sh keeps working. See README.md "Revision History"
# (v1.1) for why this changed - the old version used GNU-sed-only syntax
# and a path hardcoded to the original author's machine, neither of which
# work on macOS.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/fix_msg_connection.py" "$@"
