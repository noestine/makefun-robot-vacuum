#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse.

Writes exactly one line to /output/entry.txt: the excuse a robot
vacuum gives for missing a spot. The gate requires UTF-8 text of
1 to 120 characters, a single line, not only whitespace.

Standard library only, offline, deterministic: the same line every run.
"""

import os

# The excuse, in the vacuum's own voice. 82 characters, one line.
EXCUSE = (
    "I skipped that spot because the dust bunny unionized, "
    "and I respect a picket line."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 120


def validate_line(line):
    """Check a candidate entry line against the gate rules.

    Returns True when the line is valid, otherwise raises ValueError.
    """
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_LENGTH:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_LENGTH)
        )
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return True


def write_entry(line, path=OUTPUT_PATH):
    """Validate the line and write it (no trailing newline) to path."""
    validate_line(line)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)


def main():
    write_entry(EXCUSE)


if __name__ == "__main__":
    main()
