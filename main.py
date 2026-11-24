#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint.

Writes a single one-line joke about office life to /output/entry.txt.

The joke is a single line of at most 200 UTF-8 characters: the sort of line
you send a colleague after a meeting that should have been an email.
"""

import os
import sys

JOKE = (
    "I wrote 'per my last email' today and felt my soul quietly file "
    "for early retirement."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def validate(line: str) -> None:
    """Check the joke meets the gate: 1-200 chars, one line, no junk."""
    if not 1 <= len(line) <= 200:
        raise ValueError(f"joke must be 1-200 characters, got {len(line)}")
    if line != line.strip():
        raise ValueError("joke must not have leading or trailing whitespace")
    if not line.strip():
        raise ValueError("joke must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(f"joke contains a control character: U+{ord(ch):04X}")


def main() -> int:
    validate(JOKE)
    data = JOKE.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    # Verify the written bytes round-trip exactly.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("round-trip check failed: written bytes differ")
    if written.decode("utf-8") != JOKE:
        raise ValueError("round-trip check failed: decoded text differs")
    print(f"Wrote {len(JOKE)} characters ({len(data)} bytes) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
