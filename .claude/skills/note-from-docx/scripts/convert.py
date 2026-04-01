#!/usr/bin/env python3
"""
note-from-docx: verbatim JSON → Markdown converter.

Takes the JSON produced by extract.py (via stdin or file) and outputs a
faithful, lossless Markdown representation.  No AI summarisation — zero
omission policy.

Rules:
  - Heading levels come directly from Word Heading styles (authoritative).
  - Bold / italic / inline-code runs are preserved.
  - Tables are rendered as Markdown tables.
  - List items respect indent level.
  - Images are rendered as ![caption](image_prefix/fig_N.ext).
  - Consecutive blank lines are collapsed to one.

Usage:
    python3 convert.py <extracted.json>                  # stdout
    python3 convert.py <extracted.json> <image-prefix>   # with image path prefix
    extract.py ... | python3 convert.py -                # pipe
    extract.py ... | python3 convert.py - <image-prefix> # pipe + prefix
"""

import sys
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Inline run rendering
# ---------------------------------------------------------------------------

def runs_to_markdown(runs: list) -> str:
    """Convert a list of run dicts to inline Markdown."""
    if not runs:
        return ""
    parts = []
    for run in runs:
        text   = run.get("text", "")
        bold   = run.get("bold", False)
        italic = run.get("italic", False)
        code   = run.get("code", False)

        if code:
            text = f"`{text}`"
        if bold and italic:
            text = f"***{text}***"
        elif bold:
            text = f"**{text}**"
        elif italic:
            text = f"*{text}*"

        parts.append(text)

    return "".join(parts)


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------

def table_to_markdown(data: list) -> str:
    """Convert a 2-D list to a Markdown table string."""
    if not data or not data[0]:
        return ""

    # Normalise column count
    col_count = max(len(row) for row in data)
    rows = [row + [""] * (col_count - len(row)) for row in data]

    header = [str(c) for c in rows[0]]
    lines  = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * col_count) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------

def convert(data: dict, image_prefix: str = "") -> str:
    blocks   = data.get("blocks", [])
    fallback = data.get("fallback", False)

    parts: list[str] = []

    if fallback:
        parts.append(
            "> ⚠️ 此檔案為舊格式（.doc），"
            "僅支援純文字提取，不含圖片與樣式。"
        )
        parts.append("")

    prev_type = None

    for block in blocks:
        btype = block.get("type", "")

        # ── blank ──────────────────────────────────────────────────────────
        if btype == "blank":
            if prev_type not in (None, "blank"):
                parts.append("")

        # ── heading ────────────────────────────────────────────────────────
        elif btype == "heading":
            level = max(1, min(block.get("level", 2), 6))
            text  = block.get("text", "")
            if prev_type not in (None, "blank"):
                parts.append("")
            parts.append(f"{'#' * level} {text}")
            parts.append("")

        # ── paragraph ──────────────────────────────────────────────────────
        elif btype == "paragraph":
            runs = block.get("runs", [])
            text = block.get("text", "")
            line = runs_to_markdown(runs) if runs else text
            parts.append(line)

        # ── list_item ──────────────────────────────────────────────────────
        elif btype == "list_item":
            indent    = block.get("indent", 0)
            list_type = block.get("list_type", "unordered")
            text      = block.get("text", "")
            bullet    = "-" if list_type == "unordered" else "1."
            parts.append(f"{'  ' * indent}{bullet} {text}")

        # ── table ──────────────────────────────────────────────────────────
        elif btype == "table":
            if prev_type not in (None, "blank"):
                parts.append("")
            parts.append(table_to_markdown(block.get("data", [])))
            parts.append("")

        # ── image ──────────────────────────────────────────────────────────
        elif btype == "image":
            fig_index = block.get("fig_index", 1)
            ext       = block.get("ext", "png")
            caption   = block.get("caption", "") or f"Figure {fig_index}"
            fig_name  = f"fig_{fig_index}.{ext}"
            img_path  = f"{image_prefix}/{fig_name}" if image_prefix else fig_name

            if prev_type not in (None, "blank"):
                parts.append("")
            parts.append(f"![{caption}]({img_path})")
            parts.append("")

        # ── hr ─────────────────────────────────────────────────────────────
        elif btype == "hr":
            if prev_type not in (None, "blank"):
                parts.append("")
            parts.append("---")
            parts.append("")

        prev_type = btype

    # Collapse consecutive blank lines to one
    result_lines: list[str] = []
    blank_run = 0
    for line in parts:
        if line == "":
            blank_run += 1
            if blank_run == 1:
                result_lines.append(line)
        else:
            blank_run = 0
            result_lines.append(line)

    return "\n".join(result_lines).strip()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "-":
        raw          = sys.stdin.read()
        image_prefix = args[1] if len(args) >= 2 else ""
    else:
        json_path = Path(args[0])
        if not json_path.exists():
            print(f"Error: file not found: {json_path}", file=sys.stderr)
            sys.exit(1)
        raw          = json_path.read_text(encoding="utf-8")
        image_prefix = args[1] if len(args) >= 2 else ""

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"Error from extractor: {data['error']}", file=sys.stderr)
        sys.exit(1)

    print(convert(data, image_prefix))


if __name__ == "__main__":
    main()
