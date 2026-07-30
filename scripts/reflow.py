#!/usr/bin/env python3
"""Reflow prose in kramdown-rfc Markdown to a fixed width, idempotently.

Write the draft however you like: one long line per paragraph, ragged edits
pasted in, whatever. Then run this and the line breaks come out uniform again.

    python scripts/reflow.py                       # the draft, in place
    python scripts/reflow.py README.md data/README.md
    python scripts/reflow.py --width 72 FILE
    python scripts/reflow.py --sentences FILE       # one sentence per line
    python scripts/reflow.py --check FILE          # exit 1 if reflow needed

Two layouts are supported. Fixed-width wrapping is the default. One sentence
per line (`--sentences`) is the better choice for documents under review: an
edit to one sentence touches one line, so the diff shows what changed rather
than a whole reflowed paragraph. It is the convention used for the drafts in
these repositories.

Running it twice produces no further change, so it is safe in a pre-commit
hook or a CI check.

What is deliberately left alone, because reflowing it would break the
document:

  * the YAML front matter, up to the first `--- abstract` / `--- middle` marker
  * those section markers themselves
  * ATX headings (`#`, `##`, ...)
  * fenced code blocks, and their contents verbatim
  * indented blocks of four spaces or more (artwork, ABNF, examples)
  * table rows (any line starting with `|`)
  * kramdown block attributes and directives (`{:...}`, `{::...}`)
  * reference definitions (`[foo]: http://...`)
  * HTML comments and any line that is a bare URL

What is reflowed: ordinary paragraphs, list items (with their hanging indent
preserved), and block quotes (with their `>` prefix preserved).

Tokens that must not be split across lines are kept atomic: `{{xref}}`,
`{{{unicode}}}`, inline code spans in backticks, and Markdown links whose
text and target would otherwise be separated.
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_WIDTH = 78
DEFAULT_TARGET = "draft-sastry-spacerg-space-research-infra-typology.md"

SECTION_MARKER = re.compile(r"^---\s+\w")
HEADING = re.compile(r"^#{1,6}\s")
KRAMDOWN_ATTR = re.compile(r"^\s*\{:")
REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s")
FENCE = re.compile(r"^\s*(```|~~~)")
TABLE_ROW = re.compile(r"^\s*\|")
BULLET = re.compile(r"^(\s*)([-*+]|\d+[.)])(\s+)(.*)$")
QUOTE = re.compile(r"^(\s*>\s?)(.*)$")
BARE_URL = re.compile(r"^\s*<?https?://\S+>?\s*$")
HTML_COMMENT = re.compile(r"^\s*<!--")

# Atomic tokens: xrefs, inline code, and inline links.
ATOMIC = re.compile(
    r"\{\{\{.*?\}\}\}"       # {{{unicode}}}
    r"|\{\{.*?\}\}"          # {{xref}}
    r"|`[^`]*`"              # `code span`
    r"|\[[^\]]*\]\([^)]*\)"  # [text](target)
    r"|\[[^\]]*\]\[[^\]]*\]" # [text][ref]
)


def tokenise(text):
    """Split on whitespace, keeping atomic constructs in one piece.

    Done by substituting each construct for a whitespace-free sentinel before
    splitting, so that punctuation attached to a construct stays attached:
    `{{REGISTRY}}.` must remain one token, not `{{REGISTRY}}` plus `.`.
    """
    held = []

    def stash(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    masked = ATOMIC.sub(stash, text)
    tokens = masked.split()
    if not held:
        return tokens
    unmask = re.compile(r"\x00(\d+)\x00")
    return [unmask.sub(lambda m: held[int(m.group(1))], t) for t in tokens]


# Words ending in a period that do not end a sentence. Matched case-sensitively
# against the whitespace-delimited word preceding the candidate break.
ABBREV = {
    "e.g.", "i.e.", "cf.", "etc.", "vs.", "viz.", "al.", "ca.", "approx.",
    "resp.", "incl.", "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "St.", "Jr.",
    "Sr.", "Inc.", "Ltd.", "Co.", "Corp.", "U.S.", "U.K.", "U.N.", "Rev.",
}
# Abbreviations only when a number follows. "No." is "number" in "No. 3" but
# the word "No" in "Is it a plan? No. It is a filing."
NUMERIC_ABBREV = {
    "Fig.", "Figs.", "No.", "Nos.", "Sec.", "Secs.", "Ch.", "Eq.", "Eqs.",
    "Ref.", "Refs.", "Art.", "para.", "paras.", "pp.", "p.", "vol.", "ed.",
    "eds.",
}
# A sentence may begin with a capital, a digit, an opening quote or bracket,
# emphasis markers, or a masked atomic token (\x00 sentinel).
SENT_START = re.compile(r'^[A-Z0-9"“(\[*_\x00]')
INITIAL = re.compile(r"^[A-Z]\.$")
SENT_BREAK = re.compile(r'([.!?][")”\]]*)(\s+)')


def split_sentences(text):
    """One sentence per element. Operates on text whose atomic constructs have
    already been masked, so xrefs like {{I-D.foo-bar}} cannot be mistaken for
    sentence ends."""
    out, start = [], 0
    for m in SENT_BREAK.finditer(text):
        end = m.end(1)
        head = text[start:end]
        tail = text[m.end():]
        if not tail:
            continue
        prev_word = head.split()[-1] if head.split() else ""
        if prev_word in ABBREV or INITIAL.match(prev_word):
            continue
        if prev_word in NUMERIC_ABBREV and tail[:1].isdigit():
            continue
        if not SENT_START.match(tail):
            continue
        # A decimal such as "1. 5" cannot arise, but "Section 3. Then" can:
        # require that the char before the period is not a lone digit.
        if len(prev_word) >= 2 and prev_word[-2].isdigit() and len(prev_word) == 2:
            continue
        out.append(head.strip())
        start = m.end()
    remainder = text[start:].strip()
    if remainder:
        out.append(remainder)
    return out or ([text.strip()] if text.strip() else [])


def lay_out_sentences(text, first_prefix, rest_prefix):
    """One sentence per line, preserving any list or quote prefix."""
    held = []

    def stash(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    masked = ATOMIC.sub(stash, " ".join(text.split()))
    unmask = re.compile(r"\x00(\d+)\x00")
    lines = []
    for i, sent in enumerate(split_sentences(masked)):
        restored = unmask.sub(lambda m: held[int(m.group(1))], sent)
        lines.append((first_prefix if i == 0 else rest_prefix) + restored)
    return lines


def wrap(tokens, width, first_prefix, rest_prefix):
    """Greedy wrap. A token longer than the line is placed alone and allowed
    to overflow rather than being broken: URLs and xrefs must stay intact."""
    if not tokens:
        return [first_prefix.rstrip()] if first_prefix.strip() else []
    lines, cur, prefix = [], [], first_prefix
    for tok in tokens:
        if not cur:
            cur = [tok]
            continue
        if len(prefix) + len(" ".join(cur)) + 1 + len(tok) <= width:
            cur.append(tok)
        else:
            lines.append(prefix + " ".join(cur))
            prefix, cur = rest_prefix, [tok]
    lines.append(prefix + " ".join(cur))
    return lines


def reflow(text, width=DEFAULT_WIDTH, sentences=False):
    lines = text.split("\n")
    out, i, n = [], 0, len(lines)

    # 1. Front matter: copy verbatim up to the first `--- abstract`-style marker.
    if lines and lines[0].strip() == "---":
        out.append(lines[0])
        i = 1
        while i < n and not SECTION_MARKER.match(lines[i]):
            out.append(lines[i])
            i += 1

    # 2. Body.
    while i < n:
        line = lines[i]

        if not line.strip():
            out.append("")
            i += 1
            continue

        # Verbatim single lines.
        if (SECTION_MARKER.match(line) or HEADING.match(line)
                or KRAMDOWN_ATTR.match(line) or REF_DEF.match(line)
                or TABLE_ROW.match(line) or BARE_URL.match(line)
                or HTML_COMMENT.match(line) or line.startswith("    ")
                or line.startswith("\t")):
            out.append(line)
            i += 1
            continue

        # Fenced code: copy through the closing fence.
        if FENCE.match(line):
            out.append(line)
            i += 1
            while i < n:
                out.append(lines[i])
                closing = FENCE.match(lines[i])
                i += 1
                if closing:
                    break
            continue

        # Block quote: gather, strip prefixes, reflow, re-prefix.
        if QUOTE.match(line):
            marker = QUOTE.match(line).group(1)
            prefix = marker.rstrip() + " "
            body = []
            while i < n and QUOTE.match(lines[i]):
                body.append(QUOTE.match(lines[i]).group(2))
                i += 1
            joined = " ".join(body)
            out.extend(lay_out_sentences(joined, prefix, prefix) if sentences
                       else wrap(tokenise(joined), width, prefix, prefix))
            continue

        # List item: reflow with a hanging indent aligned under the text.
        m = BULLET.match(line)
        if m:
            indent, marker, gap, first = m.groups()
            first_prefix = indent + marker + gap
            rest_prefix = " " * len(first_prefix)
            body = [first]
            i += 1
            # Continuation lines: indented further, not blank, not a new item.
            while i < n and lines[i].strip() and not BULLET.match(lines[i]) \
                    and not HEADING.match(lines[i]) and lines[i].startswith(" "):
                body.append(lines[i].strip())
                i += 1
            joined = " ".join(body)
            out.extend(lay_out_sentences(joined, first_prefix, rest_prefix)
                       if sentences
                       else wrap(tokenise(joined), width, first_prefix, rest_prefix))
            continue

        # Ordinary paragraph.
        body = []
        while i < n and lines[i].strip() and not (
                HEADING.match(lines[i]) or SECTION_MARKER.match(lines[i])
                or KRAMDOWN_ATTR.match(lines[i]) or TABLE_ROW.match(lines[i])
                or FENCE.match(lines[i]) or BULLET.match(lines[i])
                or QUOTE.match(lines[i]) or lines[i].startswith("    ")):
            body.append(lines[i].strip())
            i += 1
        joined = " ".join(body)
        out.extend(lay_out_sentences(joined, "", "") if sentences
                   else wrap(tokenise(joined), width, "", ""))

    result = "\n".join(out)
    return result.rstrip("\n") + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help=f"default: {DEFAULT_TARGET}")
    ap.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    ap.add_argument("--sentences", action="store_true",
                    help="one sentence per line instead of wrapping to --width")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if any file would change")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    paths = [Path(f) for f in args.files] or [root / DEFAULT_TARGET]

    changed = []
    for p in paths:
        if not p.is_file():
            print(f"no such file: {p}", file=sys.stderr)
            return 2
        before = p.read_text()
        after = reflow(before, args.width, args.sentences)
        if before == after:
            print(f"unchanged  {p}")
            continue
        changed.append(p)
        if args.check:
            print(f"NEEDS REFLOW  {p}")
        else:
            p.write_text(after)
            how = "one sentence per line" if args.sentences else f"width {args.width}"
            print(f"reflowed   {p}  ({how})")

    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
