#!/usr/bin/env python3
"""
note-from-pdf: verbatim PDF → Markdown converter.

Takes the JSON produced by extract.py (via stdin or file arg) and outputs
a faithful, lossless Markdown representation.  No AI summarisation.

Rules:
  - Every page starts with <!-- Page N -->
  - Heading levels come from heading_hints (font-size based).
    Fallback: detect by text pattern (numbered chapter, short ALL-CAPS line).
  - Tables are rendered as Markdown tables.
  - Repeated headers/footers (same line on ≥ 3 consecutive pages) are dropped.
  - Everything else is reproduced verbatim.

Usage:
    python3 convert.py <extracted.json>          # write to stdout
    python3 convert.py <extracted.json> <out.md> # write to file
    extract.py ... | python3 convert.py -        # pipe mode
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Repeated-content detection (headers / footers)
# ---------------------------------------------------------------------------

def find_repeated_lines(pages: list, threshold: int = 3) -> set:
    """Return lines that appear on >= threshold pages (likely headers/footers)."""
    if len(pages) < threshold:
        return set()

    line_page_count: Counter = Counter()
    for page in pages:
        seen_this_page: set = set()
        for raw in page.get("text", "").splitlines():
            line = raw.strip()
            if line and line not in seen_this_page:
                line_page_count[line] += 1
                seen_this_page.add(line)

    repeated = {
        line for line, count in line_page_count.items()
        if count >= threshold and len(line) < 120
    }
    return repeated


# ---------------------------------------------------------------------------
# Heading detection
# ---------------------------------------------------------------------------

def build_heading_map(hints: list) -> dict:
    """Map stripped text → heading level from font-size hints."""
    result: dict = {}
    for h in hints:
        text = h.get("text", "").strip()
        level = h.get("level", 3)
        if text:
            result[text] = level
    return result


_NUMBERED_HEADING_RE = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2})*)\s+\S"   # e.g. "1.2 Title" or "03 Foo"
)
_ALPHA_HEADING_RE = re.compile(
    r"^[A-Z\u4e00-\u9fff][^\n]{0,60}$"  # short CJK/uppercase-start lines
)


def guess_heading_level_from_text(line: str) -> int | None:
    """Heuristic heading detection when no font-size hint is available.

    Returns 1/2/3 or None (= not a heading).
    """
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return None

    # Numbered: "1 Intro", "2.3 Foo", "03 Bar"
    m = _NUMBERED_HEADING_RE.match(stripped)
    if m:
        depth = m.group(1).count(".") + 1
        return min(depth, 3)

    # Short ALL-CAPS latin line (≤ 60 chars, no sentence-ending punctuation)
    if (stripped == stripped.upper()
            and re.search(r"[A-Z]", stripped)
            and not stripped.endswith((".", ",", ";", ":", "?", "!"))):
        return 2

    return None


# ---------------------------------------------------------------------------
# Table substitution
# ---------------------------------------------------------------------------

def build_table_map(tables_markdown: list) -> dict:
    """Map page_number → list of markdown table strings."""
    tm: dict = defaultdict(list)
    for entry in tables_markdown:
        tm[entry["page"]].append(entry["markdown"])
    return tm


def lines_contain_table_text(lines: list, table_md: str) -> bool:
    """Quick check: does the raw text block look like it contains table data?"""
    # If the table markdown has "|", assume the raw text is table-ish
    return "|" in table_md


# ---------------------------------------------------------------------------
# Per-page conversion
# ---------------------------------------------------------------------------

def convert_page(page_data: dict,
                 heading_map: dict,
                 repeated: set,
                 table_list: list) -> list:
    """Return a list of markdown lines for one page."""
    text: str = page_data.get("text", "")
    out: list = []

    # We track which tables have been emitted so we don't duplicate
    tables_emitted = [False] * len(table_list)

    raw_lines = text.splitlines()
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        stripped = line.strip()
        i += 1

        # Skip repeated header/footer lines
        if stripped in repeated:
            continue

        # Empty line → preserve paragraph break
        if not stripped:
            out.append("")
            continue

        # --- Heading resolution ---
        # 1. Font-size hints (authoritative)
        if stripped in heading_map:
            level = heading_map[stripped]
            out.append(f"{'#' * level} {stripped}")
            continue

        # 2. Text-pattern heuristic
        guessed = guess_heading_level_from_text(stripped)
        if guessed is not None:
            out.append(f"{'#' * guessed} {stripped}")
            continue

        # --- Code block detection (lines starting with spaces + code-ish chars) ---
        if line.startswith("    ") or line.startswith("\t"):
            # Collect consecutive indented lines
            block = [stripped]
            while i < len(raw_lines) and (raw_lines[i].startswith("    ")
                                          or raw_lines[i].startswith("\t")):
                block.append(raw_lines[i].strip())
                i += 1
            out.append("```")
            out.extend(block)
            out.append("```")
            continue

        # Plain text — verbatim
        out.append(stripped)

    # Append markdown tables at end of page (after body text)
    for idx, table_md in enumerate(table_list):
        if not tables_emitted[idx]:
            out.append("")
            out.append(table_md)
            tables_emitted[idx] = True

    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def convert(data: dict) -> str:
    pages = data.get("pages", [])
    tables_markdown = data.get("tables_markdown", [])
    table_map = build_table_map(tables_markdown)

    repeated = find_repeated_lines(pages, threshold=3)

    parts: list = []

    for page_data in pages:
        page_num = page_data["page"]
        hints = page_data.get("heading_hints", [])
        heading_map = build_heading_map(hints)

        parts.append(f"<!-- Page {page_num} -->")
        parts.append("")

        md_lines = convert_page(
            page_data,
            heading_map,
            repeated,
            table_map.get(page_num, [])
        )
        parts.extend(md_lines)
        parts.append("")

    return "\n".join(parts)


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "-":
        raw = sys.stdin.read()
    else:
        json_path = Path(args[0])
        if not json_path.exists():
            print(f"Error: file not found: {json_path}", file=sys.stderr)
            sys.exit(1)
        raw = json_path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"Error from extractor: {data['error']}", file=sys.stderr)
        sys.exit(1)

    result = convert(data)

    if len(args) >= 2:
        out_path = Path(args[1])
        out_path.write_text(result, encoding="utf-8")
        print(f"Written to {out_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
