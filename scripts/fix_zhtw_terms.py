#!/usr/bin/env python3
"""
fix_zhtw_terms.py — 修正 zh-TW 翻譯中的大陸用語，替換為台灣繁體中文標準用語。

此腳本在 `bench import-translations` 之後執行：
1. 使用 OpenCC s2twp 將簡體中文 CSV 翻譯轉為台灣繁體
2. 套用手動 TERM_MAP 修正 OpenCC 未處理的詞彙差異
3. 從各 app 的 zh.po（簡體）補入 zh-TW CSV 中缺少的項目（避免簡體回落）
"""

import csv
import io
import os
import re

try:
    import opencc
    _converter = opencc.OpenCC("s2twp")  # Simplified → Traditional Taiwan (with phrase dict)

    def to_tw(text: str) -> str:
        return _converter.convert(text)

    OPENCC_AVAILABLE = True
except ImportError:
    OPENCC_AVAILABLE = False

    def to_tw(text: str) -> str:
        return text


# 手動詞彙對照（OpenCC 未轉換或轉換不完整的台灣用語）
# 格式: (來源詞, 台灣用語) — 在 OpenCC 之後套用
TERM_MAP = [
    # OpenCC 將 质量 → 質量，但台灣用語是品質
    ("質量",   "品質"),
    # 退出系統 / 退出系统 → 登出（OpenCC 轉成傳統但語意還是大陸用語）
    ("退出系統", "登出"),
    ("退出系统", "登出"),
    # 界面 → 介面（OpenCC 可能保留界面）
    ("界面",   "介面"),
    # 郵箱/邮箱 → 信箱
    ("郵箱",   "信箱"),
    ("邮箱",   "信箱"),
    # 帳號 → 帳戶（部分情境）
    ("帳號",   "帳戶"),
    # 應用程序 → 應用程式
    ("應用程序", "應用程式"),
    ("应用程序", "應用程式"),
    # 設置 → 設定
    ("設置",   "設定"),
    ("设置",   "設定"),
    # 數據 → 資料（OpenCC s2twp 有時保留數據）
    ("數據庫", "資料庫"),
    ("數據",   "資料"),
    # 資訊 overrides
    ("信息",   "資訊"),
]

BENCH_APPS = "/home/frappe/frappe-bench/apps"

# (app_name, zh_po_path, zh_TW_csv_path)
APP_CONFIGS = [
    ("frappe",     f"{BENCH_APPS}/frappe/frappe/locale/zh.po",
                   f"{BENCH_APPS}/frappe/frappe/translations/zh-TW.csv"),
    ("erpnext",    f"{BENCH_APPS}/erpnext/erpnext/locale/zh.po",
                   f"{BENCH_APPS}/erpnext/erpnext/translations/zh-TW.csv"),
    ("hrms",       f"{BENCH_APPS}/hrms/hrms/locale/zh.po",
                   f"{BENCH_APPS}/hrms/hrms/translations/zh-TW.csv"),
    ("healthcare", f"{BENCH_APPS}/healthcare/healthcare/locale/zh.po",
                   f"{BENCH_APPS}/healthcare/healthcare/translations/zh-TW.csv"),
]

PO_FILES = [
    f"{BENCH_APPS}/healthcare/healthcare/locale/zh_TW.po",
]


def apply_fixes(text: str) -> str:
    """Apply OpenCC s2twp conversion then manual Taiwan term overrides."""
    result = to_tw(text)
    for mainland, taiwan in TERM_MAP:
        result = result.replace(mainland, taiwan)
    return result


def parse_po_to_dict(filepath: str) -> dict:
    """Parse a .po file and return {msgid: msgstr} for non-empty translations."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    translations = {}
    # Match msgid / msgstr pairs (handles multi-line strings)
    entries = re.split(r'\n(?=msgid )', content)
    for entry in entries:
        msgid_match = re.search(r'^msgid\s+"((?:[^"\\]|\\.)*)"', entry, re.MULTILINE)
        msgstr_match = re.search(r'^msgstr\s+"((?:[^"\\]|\\.)*)"', entry, re.MULTILINE)
        if not msgid_match or not msgstr_match:
            continue
        msgid = msgid_match.group(1).replace('\\"', '"')
        msgstr = msgstr_match.group(1).replace('\\"', '"')
        if msgid and msgstr:  # skip empty msgid (header) and empty msgstr
            translations[msgid] = msgstr
    return translations


def read_csv_sources(filepath: str) -> set:
    """Return set of source strings already in the zh-TW CSV."""
    sources = set()
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 1)
                if parts:
                    # Remove surrounding quotes if present
                    src = parts[0].strip().strip('"')
                    sources.add(src)
    except FileNotFoundError:
        pass
    return sources


def fix_csv(filepath: str) -> int:
    """Fix existing zh-TW CSV entries using OpenCC + TERM_MAP."""
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  [SKIP] {filepath}")
        return 0

    changed = 0
    new_lines = []
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        # CSV format: source,translation[,context]
        # Only fix the 2nd column (translation)
        parts = line.split(",", 1)
        if len(parts) == 2:
            original = parts[1]
            fixed = apply_fixes(original)
            if fixed != original:
                changed += 1
            new_lines.append(parts[0] + "," + fixed)
        else:
            new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"  [CSV] Fixed {changed} entries → {filepath}")
    return changed


def backfill_from_zh_po(zh_po: str, zhtw_csv: str, app: str) -> int:
    """
    Pull entries from zh.po (simplified) that are MISSING from zh-TW CSV,
    convert them with OpenCC+TERM_MAP, and append to the zh-TW CSV.

    This prevents Frappe's parent-language fallback from leaking simplified
    Chinese into the zh-TW UI for untranslated strings.
    """
    if not os.path.exists(zh_po):
        print(f"  [SKIP backfill] {zh_po} not found")
        return 0

    zh_dict = parse_po_to_dict(zh_po)
    if not zh_dict:
        return 0

    existing_sources = read_csv_sources(zhtw_csv)
    added = 0

    new_entries = []
    for src, zh_trans in zh_dict.items():
        if src in existing_sources:
            continue
        tw_trans = apply_fixes(zh_trans)
        if tw_trans:
            # Escape commas in source/translation by quoting
            src_col = f'"{src}"' if "," in src or '"' in src else src
            tw_col = f'"{tw_trans}"' if "," in tw_trans or '"' in tw_trans else tw_trans
            new_entries.append(f"{src_col},{tw_col},\n")
            added += 1

    if new_entries:
        # Ensure the CSV file exists (create empty if needed)
        os.makedirs(os.path.dirname(zhtw_csv), exist_ok=True)
        with open(zhtw_csv, "a", encoding="utf-8") as f:
            f.writelines(new_entries)

    print(f"  [BACKFILL] Added {added} missing zh→zh-TW entries for {app}")
    return added


def fix_po(filepath: str) -> int:
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"  [SKIP] {filepath}")
        return 0

    changed = 0
    new_lines = []
    in_msgstr = False

    for line in lines:
        if line.startswith("msgstr "):
            in_msgstr = True
            fixed = apply_fixes(line)
            if fixed != line:
                changed += 1
            new_lines.append(fixed)
        elif in_msgstr and line.startswith('"'):
            fixed = apply_fixes(line)
            if fixed != line:
                changed += 1
            new_lines.append(fixed)
        else:
            in_msgstr = False
            new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"  [PO]  Fixed {changed} msgstr → {filepath}")
    return changed


def main():
    mode = "OpenCC s2twp + 手動詞彙" if OPENCC_AVAILABLE else "僅手動詞彙（請安裝 opencc-python-reimplemented）"
    print(f"=== 修正 zh-TW 翻譯：大陸用語 → 台灣繁體用語 [{mode}] ===")
    total = 0

    # Step 1: Fix existing zh-TW CSV entries
    print("\n--- 步驟1：修正現有 zh-TW CSV 用語 ---")
    for _app, _zh_po, zhtw_csv in APP_CONFIGS:
        total += fix_csv(zhtw_csv)

    # Step 2: Backfill missing entries from zh.po (prevents simplified fallback)
    print("\n--- 步驟2：從 zh.po 補入缺少的 zh-TW 翻譯（避免簡體中文回落） ---")
    for app, zh_po, zhtw_csv in APP_CONFIGS:
        total += backfill_from_zh_po(zh_po, zhtw_csv, app)

    # Step 3: Fix .po files
    print("\n--- 步驟3：修正 .po 檔案 ---")
    for path in PO_FILES:
        total += fix_po(path)

    print(f"\n完成！共修正/新增 {total} 處用語。")


if __name__ == "__main__":
    main()
