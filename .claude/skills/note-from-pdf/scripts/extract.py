#!/usr/bin/env python3
"""
note-from-pdf extraction script
Uses pdfplumber (primary) + pypdf (fallback)
"""
import sys
import json
from pathlib import Path


def detect_image_heavy(pages_data: list) -> bool:
    """Detect if PDF is primarily image-based"""
    total_chars = sum(len(p.get("text", "")) for p in pages_data)
    avg_chars = total_chars / len(pages_data) if pages_data else 0
    return avg_chars < 100


def extract_heading_hints(page) -> list:
    """Detect heading lines by comparing font size to body text (median size).
    Returns list of {text, level, size} where level 1/2/3 = H1/H2/H3."""
    try:
        words = page.extract_words(extra_attrs=["size"])
        if not words:
            return []

        from collections import Counter
        # Collect font sizes (ignore tiny fonts < 6pt, likely footnotes)
        sizes = [round(w.get("size", 0)) for w in words if w.get("size", 0) > 6]
        if not sizes:
            return []

        body_size = Counter(sizes).most_common(1)[0][0]
        if body_size == 0:
            return []

        # Group words into lines by top coordinate (2px buckets for tolerance)
        line_map: dict = {}
        for w in words:
            top_key = round(w.get("top", 0) / 2) * 2
            if top_key not in line_map:
                line_map[top_key] = {"texts": [], "max_size": 0.0}
            line_map[top_key]["texts"].append(w["text"])
            sz = w.get("size", 0.0)
            if sz > line_map[top_key]["max_size"]:
                line_map[top_key]["max_size"] = sz

        hints = []
        for top_key in sorted(line_map):
            entry = line_map[top_key]
            text = " ".join(entry["texts"]).strip()
            size = entry["max_size"]
            ratio = size / body_size if body_size else 1.0
            # Only mark as heading if noticeably larger than body
            if ratio >= 1.2 and text:
                level = 1 if ratio >= 1.5 else (2 if ratio >= 1.3 else 3)
                hints.append({
                    "text": text,
                    "level": level,
                    "size": round(size, 1),
                    "body_size": body_size
                })

        return hints
    except Exception:
        return []


def extract_with_pdfplumber(pdf_path: str) -> dict:
    try:
        import pdfplumber
    except ImportError:
        return {"error": "pdfplumber not installed. Run: pip install pdfplumber"}

    result = {"pages": [], "metadata": {}, "tables": []}

    with pdfplumber.open(pdf_path) as pdf:
        # Extract metadata
        result["metadata"] = {
            "pages": len(pdf.pages),
            "title": pdf.metadata.get("Title", ""),
            "author": pdf.metadata.get("Author", ""),
            "created": pdf.metadata.get("CreationDate", ""),
        }

        for i, page in enumerate(pdf.pages):
            page_data = {"page": i + 1, "text": "", "tables": [], "heading_hints": []}

            # Extract text
            text = page.extract_text()
            page_data["text"] = text or ""

            # Extract tables
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table:
                        page_data["tables"].append(table)
                        result["tables"].append({"page": i + 1, "data": table})

            # Extract heading hints via font size
            page_data["heading_hints"] = extract_heading_hints(page)

            result["pages"].append(page_data)

    return result


def extract_with_pypdf(pdf_path: str) -> dict:
    """Fallback extraction"""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return {"error": "Neither pdfplumber nor pypdf is installed."}

    result = {"pages": [], "metadata": {}, "tables": []}
    reader = PdfReader(pdf_path)

    result["metadata"] = {
        "pages": len(reader.pages),
        "title": reader.metadata.get("/Title", "") if reader.metadata else "",
        "author": reader.metadata.get("/Author", "") if reader.metadata else "",
        "created": reader.metadata.get("/CreationDate", "") if reader.metadata else "",
    }

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        result["pages"].append({"page": i + 1, "text": text, "tables": []})

    return result


def tables_to_markdown(tables: list) -> list:
    """Convert extracted tables to markdown format"""
    md_tables = []
    for table_info in tables:
        table = table_info.get("data", [])
        if not table or not table[0]:
            continue

        lines = []
        # Header row
        header = [str(cell or "").strip() for cell in table[0]]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")

        # Data rows
        for row in table[1:]:
            cells = [str(cell or "").strip() for cell in row]
            # Pad if needed
            while len(cells) < len(header):
                cells.append("")
            lines.append("| " + " | ".join(cells) + " |")

        md_tables.append({
            "page": table_info.get("page", 0),
            "markdown": "\n".join(lines)
        })

    return md_tables


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: extract.py <pdf-path>"}))
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not Path(pdf_path).exists():
        print(json.dumps({"error": f"File not found: {pdf_path}"}))
        sys.exit(1)

    # Try pdfplumber first, fallback to pypdf
    result = extract_with_pdfplumber(pdf_path)
    if "error" in result:
        result = extract_with_pypdf(pdf_path)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    # Detect image-heavy
    result["image_heavy"] = detect_image_heavy(result["pages"])

    # Convert tables to markdown
    result["tables_markdown"] = tables_to_markdown(result.get("tables", []))

    # Build full text
    full_text_parts = []
    for page in result["pages"]:
        if page["text"].strip():
            full_text_parts.append(page["text"])

    result["full_text"] = "\n\n".join(full_text_parts)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
