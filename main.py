#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

One sentence that could have replaced an entire pointless meeting.
The angle: the daily standup where absolutely nothing has changed since
yesterday, nobody is blocked, and the status doc already said all of it
before the invite even went out. The only attendee that truly needed
the meeting was the calendar.

Standard library only. Deterministic: the same line, byte for byte,
on every run. No network, no clock, no randomness.
"""

import hashlib
import os
import sys

# The entry: exactly one line, plain ASCII, at most 160 characters.
LINE = "No blockers, nothing changed since yesterday, and the doc said it first - the calendar just wanted company."

MAX_CHARS = 160


def validate(line):
    """Enforce every competition constraint on the line.

    Returns the validated line so callers can chain it.
    Raises ValueError/TypeError on the first broken rule, naming it.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError("line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError("line is %d chars, over the %d limit" % (len(line), MAX_CHARS))
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("line must be plain ASCII")
    return line


def main():
    line = validate(LINE)  # validated copy is the only one ever written
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(line + "\n")
    # Round-trip check: what we wrote must read back exactly.
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw != (line + "\n").encode("ascii"):
        raise SystemExit("round-trip check failed")
    digest = hashlib.sha256(raw).hexdigest()
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
