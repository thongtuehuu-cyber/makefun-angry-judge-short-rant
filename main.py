"""Angry Judge: The Short Rant Contest.

Writes one short, funny rant about a small everyday annoyance to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic: no network, no randomness, no reading outside the repo.
The rant is validated (1-400 chars, not only whitespace) before writing.
"""

import os
import sys

RANT = (
    "The self-checkout scanned my milk, weighed my soul, then froze on "
    "'unexpected item in the bagging area.' I moved nothing. I touched "
    "nothing. I just stood there, a grown adult, being publicly accused "
    "of theft by a machine I was doing unpaid labour for."
)

MAX_CHARS = 400


# Fail fast at import if the embedded rant ever drifts out of spec,
# so a bad edit can never silently ship an invalid entry.
assert 1 <= len(RANT) <= MAX_CHARS and RANT.strip(), "embedded rant out of spec"


def validate(text):
    """Raise ValueError unless text is a valid entry (1-400 chars, non-blank)."""
    if not isinstance(text, str):
        raise ValueError("rant must be text")
    if not text.strip():
        raise ValueError("rant must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError("rant is %d chars, over the 400-char cap" % len(text))
    return text


def write_entry(text, out_dir):
    validate(text)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back gate: the file on disk must be byte-identical to the rant.
    with open(path, "rb") as f:
        if f.read() != data:
            raise ValueError("read-back mismatch: entry.txt != rant")
    return path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        path = write_entry(RANT, out_dir)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(RANT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
