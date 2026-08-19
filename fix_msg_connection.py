#!/usr/bin/env python3
"""
fix_msg_connection.py

GNU Radio Companion (as of 3.10) does not generate msg_connect() calls for
embedded Python blocks, so the asynchronous message connection between
stream_to_msg_0 and audio_tone_gen_0 has to be patched into pluto.py after
every `grcc pluto-antenna-range.grc` regeneration.

This replaces the original fix_msg_connection.sh, which used GNU-sed-only
`sed -i` syntax (macOS ships BSD sed, which requires an explicit backup
suffix argument and has different multi-line append syntax) and a path
hardcoded to the original author's Ubuntu home directory. This version is
plain Python 3 - already a hard requirement for this project - and
resolves paths relative to its own location, so it works unmodified on
macOS, Linux, and Windows.

See README.md "Revision History" (v1.1) for details.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TARGET_FILE = SCRIPT_DIR / "pluto.py"

ANCHOR = "        self.connect((self.blocks_add_const_vxx_0, 0), (self.stream_to_msg_0, 0))"
MSG_CONNECT_MARKER = "msg_connect((self.stream_to_msg_0"
INSERTION = (
    "\n        \n"
    "        ##################################################\n"
    "        # Asynch Message Connections\n"
    "        ##################################################\n"
    "        self.msg_connect((self.stream_to_msg_0, 'msg_out'), (self.audio_tone_gen_0, 'db_in'))"
)


def main():
    if not TARGET_FILE.exists():
        print(
            f"Error: {TARGET_FILE} not found. Run 'grcc pluto-antenna-range.grc' first.",
            file=sys.stderr,
        )
        sys.exit(1)

    text = TARGET_FILE.read_text()

    if MSG_CONNECT_MARKER in text:
        print("Message connection already exists in pluto.py")
        return

    if ANCHOR not in text:
        print(
            "Error: could not find the expected connect() line in pluto.py.\n"
            "GRC's generated output may have changed shape - update ANCHOR in\n"
            "fix_msg_connection.py to match the new output.",
            file=sys.stderr,
        )
        sys.exit(1)

    text = text.replace(ANCHOR, ANCHOR + INSERTION, 1)
    TARGET_FILE.write_text(text)
    print("Message connection added to pluto.py")


if __name__ == "__main__":
    main()
