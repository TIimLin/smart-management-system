#!/usr/bin/env python3
"""
fix_zhtw_terms.py — 修正 zh-TW 翻譯中的大陸用語，替換為台灣繁體中文標準用語。

此腳本在 `bench import-translations` 之後執行：
1. 使用 OpenCC s2twp 將簡體中文 CSV 翻譯轉為台灣繁體
2. 套用手動 TERM_MAP 修正 OpenCC 未處理的詞彙差異
"""

import sys

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

CSV_FILES = [
    f"{BENCH_APPS}/frappe/frappe/translations/zh-TW.csv",
    f"{BENCH_APPS}/erpnext/erpnext/translations/zh-TW.csv",
    f"{BENCH_APPS}/hrms/hrms/translations/zh-TW.csv",
    f"{BENCH_APPS}/healthcare/healthcare/translations/zh-TW.csv",
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


def fix_csv(filepath: str) -> int:
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
        # CSV format: "English source","Translation",
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
    for path in CSV_FILES:
        total += fix_csv(path)
    for path in PO_FILES:
        total += fix_po(path)
    print(f"\n完成！共修正 {total} 處用語。")


if __name__ == "__main__":
    main()
