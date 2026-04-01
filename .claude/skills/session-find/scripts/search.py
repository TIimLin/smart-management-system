#!/usr/bin/env python3
"""
session-find search script

Usage:
  search.py <dir> --exact "phrase"         # Mode 1/2: exact substring (first 60 chars)
  search.py <dir> --keywords kw1 kw2 ...   # Mode 3: all-keywords intersection

Output (TSV): rank  session_id  mtime  snippet
"""

import argparse
import json
import os
import sys
from datetime import datetime


# ─── JSONL helpers ────────────────────────────────────────────────────────────

def read_text(filepath: str) -> str | None:
    """Read file as plain text (fast path)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def extract_user_messages(filepath: str) -> list[str]:
    """Full JSON decode — extracts all user message texts (fallback path)."""
    messages = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "user":
                    continue
                content = obj.get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    messages.append(content)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "")
                            if text.strip():
                                messages.append(text)
    except (OSError, UnicodeDecodeError):
        pass
    return messages


def find_snippet(text: str, target: str, context: int = 80) -> str:
    """Extract a snippet around the first occurrence of target in text."""
    idx = text.find(target)
    if idx == -1:
        return ""
    start = max(0, idx - 10)
    end = min(len(text), idx + context)
    return text[start:end].replace("\n", " ").strip()


# ─── Search modes ─────────────────────────────────────────────────────────────

def search_exact(files: list[str], phrase: str) -> list[tuple[str, str, str]]:
    """
    Mode 1/2: exact substring search.
    Fast path: plain-text `in` check.
    Fallback: full JSON decode (handles rare escape-sequence edge cases).
    Returns [(session_id, mtime, snippet), ...] sorted by mtime DESC.
    """
    target = phrase[:60]  # truncate for safety
    results = []

    for filepath in files:
        text = read_text(filepath)
        if text is None:
            continue

        # Fast path
        if target in text:
            snippet = find_snippet(text, target)
            mtime = _mtime(filepath)
            session_id = _session_id(filepath)
            results.append((session_id, mtime, snippet))
            continue

        # Fallback: JSON decode (handles \uXXXX or other escapes)
        messages = extract_user_messages(filepath)
        for msg in messages:
            if target in msg:
                snippet = find_snippet(msg, target)
                mtime = _mtime(filepath)
                session_id = _session_id(filepath)
                results.append((session_id, mtime, snippet))
                break

    return sorted(results, key=lambda r: r[1], reverse=True)


def search_keywords(files: list[str], keywords: list[str]) -> list[tuple[str, str, str]]:
    """
    Mode 3: all-keywords intersection.
    Fast path: plain-text `in` check for each keyword.
    Fallback: JSON decode if fast path misses.
    Returns [(session_id, mtime, snippet), ...] sorted by mtime DESC.
    """
    results = []

    for filepath in files:
        text = read_text(filepath)
        if text is None:
            continue

        # Fast path: all keywords present in raw text
        if all(kw in text for kw in keywords):
            snippet = find_snippet(text, keywords[0])
            mtime = _mtime(filepath)
            session_id = _session_id(filepath)
            results.append((session_id, mtime, snippet))
            continue

        # Fallback: JSON decode
        messages = extract_user_messages(filepath)
        combined = " ".join(messages)
        if all(kw in combined for kw in keywords):
            snippet = ""
            for msg in messages:
                if keywords[0] in msg:
                    snippet = find_snippet(msg, keywords[0])
                    break
            mtime = _mtime(filepath)
            session_id = _session_id(filepath)
            results.append((session_id, mtime, snippet))

    return sorted(results, key=lambda r: r[1], reverse=True)


def list_all(files: list[str]) -> list[tuple[str, str, str]]:
    """No args: list all sessions sorted by mtime DESC."""
    results = []
    for filepath in sorted(files, key=os.path.getmtime, reverse=True):
        results.append((_session_id(filepath), _mtime(filepath), ""))
    return results


# ─── Utilities ────────────────────────────────────────────────────────────────

def _session_id(filepath: str) -> str:
    return os.path.basename(filepath).removesuffix(".jsonl")


def _mtime(filepath: str) -> str:
    return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="session-find search script")
    parser.add_argument("dir", help="~/.claude/projects/{folder}/")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--exact", metavar="PHRASE", help="exact substring search (Mode 1/2)")
    group.add_argument("--keywords", nargs="+", metavar="KW", help="all-keywords intersection (Mode 3)")
    parser.add_argument("--include-self", action="store_true", help="include current session (newest file) in results")
    args = parser.parse_args()

    directory = os.path.expanduser(args.dir)

    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}", file=sys.stderr)
        sys.exit(2)

    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".jsonl")
    ]

    if not files:
        print("NO_SESSIONS", file=sys.stderr)
        sys.exit(3)

    # SelfExclusion: exclude the newest file (= current session) unless --include-self
    if not args.include_self and len(files) > 1:
        newest = max(files, key=os.path.getmtime)
        files = [f for f in files if f != newest]

    if args.exact:
        results = search_exact(files, args.exact)
    elif args.keywords:
        results = search_keywords(files, args.keywords)
    else:
        results = list_all(files)

    if not results:
        print("NO_MATCH")
        sys.exit(0)

    for rank, (session_id, mtime, snippet) in enumerate(results, 1):
        print(f"{rank}\t{session_id}\t{mtime}\t{snippet}")


if __name__ == "__main__":
    main()
