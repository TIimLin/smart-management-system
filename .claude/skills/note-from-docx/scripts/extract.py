#!/usr/bin/env python3
"""
note-from-docx: extract structured content from .docx / .doc files.
Outputs JSON consumed by convert.py.

Usage:
    python3 extract.py <docx-path>                  # no image export
    python3 extract.py <docx-path> <image-dir>      # export images to dir
"""
import sys
import json
import subprocess
from pathlib import Path

NS  = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DML = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


# ---------------------------------------------------------------------------
# Image collection
# ---------------------------------------------------------------------------

def collect_images(doc, image_dir):
    """
    Pre-scan all image relationships in document order.
    Exports image bytes to image_dir if provided (dir created on first write).
    Returns {rel_id: {fig_index, ext, name}}.
    """
    images = {}
    fig_index = 0

    for rel_id, rel in doc.part.rels.items():
        if "image" not in rel.reltype.lower():
            continue

        fig_index += 1
        blob = rel.target_part.blob
        ext  = rel.target_part.content_type.split("/")[-1].lower()
        ext  = {"jpeg": "jpg", "x-wmf": "wmf", "x-emf": "emf"}.get(ext, ext)

        fig_name = f"fig_{fig_index}.{ext}"

        if image_dir:
            img_path = Path(image_dir) / fig_name
            img_path.parent.mkdir(parents=True, exist_ok=True)
            img_path.write_bytes(blob)

        images[rel_id] = {"fig_index": fig_index, "ext": ext, "name": fig_name}

    return images


def get_para_image_rids(para_elem):
    """Return all r:embed rIds for images embedded in a paragraph element."""
    rids = []
    for blip in para_elem.iter(f"{{{DML}}}blip"):
        rid = blip.get(f"{{{REL}}}embed")
        if rid:
            rids.append(rid)
    # deduplicate, preserving order
    seen = set()
    result = []
    for r in rids:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result


# ---------------------------------------------------------------------------
# Block builders
# ---------------------------------------------------------------------------

def para_to_blocks(para, images_map):
    """Convert a python-docx Paragraph to a list of block dicts."""
    # Images override everything else for this paragraph
    rids = get_para_image_rids(para._element)
    image_blocks = []
    for rid in rids:
        if rid in images_map:
            img = images_map[rid]
            image_blocks.append({
                "type":      "image",
                "fig_index": img["fig_index"],
                "ext":       img["ext"],
                "name":      img["name"],
                "caption":   para.text.strip(),
            })
    if image_blocks:
        return image_blocks

    text = para.text.strip()

    if not text:
        return [{"type": "blank"}]

    # Horizontal rule paragraph (all same separator chars)
    stripped_chars = set(text.replace(" ", ""))
    if len(stripped_chars) == 1 and stripped_chars.pop() in ("-", "_", "─", "—", "*"):
        return [{"type": "hr"}]

    # Heading via Word style
    style = para.style.name if para.style else ""
    if style.startswith("Heading "):
        try:
            level = min(int(style.split(" ")[1]), 6)
        except (ValueError, IndexError):
            level = 2
        return [{"type": "heading", "level": level, "text": text}]

    # List item
    numPr = para._element.find(f".//{{{NS}}}numPr")
    if numPr is not None:
        ilvl = numPr.find(f"{{{NS}}}ilvl")
        indent = int(ilvl.get(f"{{{NS}}}val", 0)) if ilvl is not None else 0
        return [{"type": "list_item", "text": text,
                 "list_type": "unordered", "indent": indent}]

    # Regular paragraph — capture inline runs for bold/italic/code
    runs = []
    for run in para.runs:
        if run.text:
            is_code = (run.font.name or "").lower() in (
                "courier new", "consolas", "courier", "lucida console",
                "monaco", "menlo", "source code pro",
            )
            runs.append({
                "text":   run.text,
                "bold":   bool(run.bold),
                "italic": bool(run.italic),
                "code":   is_code,
            })

    return [{"type": "paragraph", "text": text, "runs": runs}]


def table_to_block(table):
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
        rows.append(cells)
    return {"type": "table", "data": rows}


# ---------------------------------------------------------------------------
# Main extraction logic
# ---------------------------------------------------------------------------

def extract_docx(docx_path, image_dir=None):
    try:
        from docx import Document
        from docx.table import Table as DocxTable
        from docx.text.paragraph import Paragraph as DocxPara
    except ImportError:
        return {"error": "python-docx not installed. Run: pip install python-docx"}

    try:
        doc = Document(docx_path)
    except Exception as e:
        return {"error": f"Failed to open document: {e}"}

    cp = doc.core_properties
    result = {
        "format":    "docx",
        "metadata":  {
            "title":    cp.title    or "",
            "author":   cp.author   or "",
            "created":  str(cp.created)  if cp.created  else "",
            "modified": str(cp.modified) if cp.modified else "",
        },
        "blocks":     [],
        "has_images": False,
        "image_count": 0,
        "fallback":   False,
        "image_dir":  image_dir,
    }

    images_map = collect_images(doc, image_dir)
    result["has_images"]  = bool(images_map)
    result["image_count"] = len(images_map)

    for child in doc.element.body:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag

        if local == "p":
            para   = DocxPara(child, doc)
            blocks = para_to_blocks(para, images_map)
            result["blocks"].extend(blocks)

        elif local == "tbl":
            table = DocxTable(child, doc)
            result["blocks"].append(table_to_block(table))

        # sectPr and other elements are intentionally skipped

    # Trim trailing blanks
    while result["blocks"] and result["blocks"][-1].get("type") == "blank":
        result["blocks"].pop()

    return result


def extract_doc_fallback(doc_path):
    """Fallback for legacy .doc: python-doc2txt → antiword → error."""
    # Try doc2txt (pip install doc2txt)
    try:
        from doc2txt import extract_text
        text = extract_text(doc_path)
        blocks = [
            {"type": "paragraph", "text": line.strip(), "runs": []}
            for line in text.splitlines() if line.strip()
        ]
        return _fallback_result(blocks)
    except (ImportError, Exception):
        pass

    # Try antiword (external binary)
    try:
        proc = subprocess.run(
            ["antiword", doc_path],
            capture_output=True, text=True, timeout=30
        )
        if proc.returncode == 0:
            blocks = [
                {"type": "paragraph", "text": line.strip(), "runs": []}
                for line in proc.stdout.splitlines() if line.strip()
            ]
            return _fallback_result(blocks)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return {
        "error": (
            "Cannot process .doc file. "
            "Install python-docx (handles most .doc), "
            "or antiword for legacy binary .doc files."
        )
    }


def _fallback_result(blocks):
    return {
        "format":     "doc",
        "metadata":   {"title": "", "author": "", "created": "", "modified": ""},
        "blocks":     blocks,
        "has_images": False,
        "image_count": 0,
        "fallback":   True,
        "image_dir":  None,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: extract.py <docx-path> [image-dir]"}))
        sys.exit(1)

    doc_path  = sys.argv[1]
    image_dir = sys.argv[2] if len(sys.argv) >= 3 else None

    if not Path(doc_path).exists():
        print(json.dumps({"error": f"File not found: {doc_path}"}))
        sys.exit(1)

    ext = Path(doc_path).suffix.lower()

    if ext in (".docx", ".docm"):
        result = extract_docx(doc_path, image_dir)
    elif ext == ".doc":
        # python-docx handles many .doc files; fall back if it fails
        result = extract_docx(doc_path, image_dir)
        if "error" in result:
            result = extract_doc_fallback(doc_path)
    else:
        # Unknown extension — try docx anyway
        result = extract_docx(doc_path, image_dir)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
