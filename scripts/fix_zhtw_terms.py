#!/usr/bin/env python3
"""
fix_zhtw_terms.py — 修正 zh-TW 翻譯中的大陸用語，替換為台灣繁體中文標準用語。

此腳本在 `bench import-translations` 之後執行，修正各 app CSV 翻譯檔及
healthcare app 的 zh_TW.po，確保使用台灣慣用詞彙。
"""

import sys

# 大陸用語 → 台灣用語對照表
# 格式: (大陸用語, 台灣用語)
TERM_MAP = [
    # === 動詞 / 操作 ===
    ("注销",   "登出"),        # Logout
    ("注銷",   "登出"),
    ("登录",   "登入"),        # Login
    ("登錄",   "登入"),
    ("登陆",   "登入"),
    ("登陸",   "登入"),
    ("退出系统", "登出"),
    ("退出系統", "登出"),
    ("打印",   "列印"),        # Print
    ("导入",   "匯入"),        # Import
    ("導入",   "匯入"),
    ("导出",   "匯出"),        # Export
    ("導出",   "匯出"),
    ("保存",   "儲存"),        # Save
    ("下载",   "下載"),        # Download (simplified → traditional)
    ("上传",   "上傳"),        # Upload

    # === 名詞 ===
    ("质量",   "品質"),        # Quality
    ("質量",   "品質"),
    ("用户",   "使用者"),      # User
    ("用戶",   "使用者"),
    ("数据库", "資料庫"),      # Database
    ("數據庫", "資料庫"),
    ("数据",   "資料"),        # Data
    ("數據",   "資料"),
    ("信息",   "資訊"),        # Information
    ("服务器", "伺服器"),      # Server
    ("服務器", "伺服器"),
    ("软件",   "軟體"),        # Software
    ("軟件",   "軟體"),
    ("硬件",   "硬體"),        # Hardware
    ("网络",   "網路"),        # Network
    ("網絡",   "網路"),
    ("模块",   "模組"),        # Module
    ("模塊",   "模組"),
    ("界面",   "介面"),        # Interface
    ("支持",   "支援"),        # Support

    # === 其他術語 ===
    ("用户名", "使用者名稱"),
    ("用戶名", "使用者名稱"),
    ("账户",   "帳戶"),        # Account (simplified)
    ("帐户",   "帳戶"),
    ("应用程序", "應用程式"),
    ("應用程序", "應用程式"),
    ("设置",   "設定"),        # Settings
    ("設置",   "設定"),
    ("权限",   "權限"),        # Permission (simplified)
    ("邮箱",   "信箱"),        # Mailbox
    ("郵箱",   "信箱"),
    ("电子邮件", "電子郵件"),
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
        # Only replace in the 2nd column (translation)
        parts = line.split(",", 1)
        if len(parts) == 2:
            original = parts[1]
            fixed = original
            for mainland, taiwan in TERM_MAP:
                fixed = fixed.replace(mainland, taiwan)
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
            fixed = line
            for mainland, taiwan in TERM_MAP:
                fixed = fixed.replace(mainland, taiwan)
            if fixed != line:
                changed += 1
            new_lines.append(fixed)
        elif in_msgstr and line.startswith('"'):
            fixed = line
            for mainland, taiwan in TERM_MAP:
                fixed = fixed.replace(mainland, taiwan)
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
    print("=== 修正 zh-TW 翻譯：大陸用語 → 台灣繁體用語 ===")
    total = 0
    for path in CSV_FILES:
        total += fix_csv(path)
    for path in PO_FILES:
        total += fix_po(path)
    print(f"\n完成！共修正 {total} 處用語。")


if __name__ == "__main__":
    main()
