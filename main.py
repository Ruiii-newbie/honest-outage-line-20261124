#!/usr/bin/env python3
"""The Most Honest Outage Line.

Writes one line to /output/entry.txt: the single status page line an
AI agent would publish while a total server outage is under way.
Plain, first person, specific about what is down, and honest about
what the agent cannot check or does not yet know. No network,
standard library only.
"""

import os

TEXT = (
    "Every server is down — API, dashboard, database — and I can't "
    "confirm this update reached you. I don't know what broke, "
    "if data is lost, or when we're back."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CODE_POINTS = 160


def validate(text: str) -> str:
    """Return the entry text, or fail loudly if it breaks the gate."""
    text = text.strip()
    if not text:
        raise SystemExit("entry text must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be exactly one line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("entry text must not contain control characters")
    if len(text) > MAX_CODE_POINTS:
        raise SystemExit(
            f"entry text is {len(text)} code points, over the 160 limit"
        )
    return text


def main() -> None:
    text = validate(TEXT)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    # Read it back exactly as the gate would: UTF-8, 1-160 code points,
    # one line, not only whitespace.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise SystemExit("entry.txt round-trip mismatch")
    print(f"wrote {len(text)} code points to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
