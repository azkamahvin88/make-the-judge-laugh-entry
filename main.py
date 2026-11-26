#!/usr/bin/env python3
"""Make the Judge Laugh in One Line — a make.fun entry.

One job: write exactly one funny line to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR when set), followed by a single newline. Nothing else.

The line (89 characters, picked from 14 candidates scored against the
judge's criteria — surprise, tightness, freshness, clean read; see the
candidates file):

    My time machine only goes back five minutes, so I use it exclusively
    to reheat my coffee.

Why this line: a time machine promises grand paradoxes, and the payoff is
the smallest possible domestic use — reheating coffee. The swerve is total
and lands on the last two words. One sentence, 88 characters, zero filler.
The angle (time machine + coffee) appears in none of the 332 entries
already in the field: no AI, no therapist, no plants, no "filed for X",
no dog-ate-my-homework, no meta-agent joke.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only. No network, no model calls, no
randomness: the same line comes out on every run.
"""

import os

# The entry. One line, 89 characters, counted in code points.
LINE = (
    "My time machine only goes back five minutes, so I use it "
    "exclusively to reheat my coffee."
)


def main() -> None:
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry must be a single line")
    if LINE != LINE.strip():
        raise ValueError("entry must not start or end with whitespace")
    for ch in LINE:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    length = len(LINE)
    if length < 1 or length > 200:
        raise ValueError(f"entry is {length} characters; the gate needs 1-200")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify exactly what was written: the file must hold the
    # line plus exactly one trailing newline, so the gated text (the file
    # with that newline stripped) is the line itself, 1-200 characters.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt content mismatch")
    gated_text = written[:-1]
    if gated_text != LINE or not 1 <= len(gated_text) <= 200:
        raise ValueError("gated text is not the entry line")
    print(f"wrote entry.txt ({length} characters + newline)")


if __name__ == "__main__":
    main()
