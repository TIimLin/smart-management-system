#!/bin/bash
# =============================================================================
# setup_i18n.sh — 繁體中文台灣翻譯初始化腳本
#
# 用途：clone 專案後執行一次，完整套用所有繁體中文（台灣）翻譯
#
# 使用方式（從專案根目錄執行）：
#   docker exec docker-backend-1 bash /home/frappe/frappe-bench/apps/healthcare/scripts/setup_i18n.sh
#
# 或使用 make 指令：
#   make setup-i18n
# =============================================================================

set -e

BENCH=/home/frappe/frappe-bench
APPS=$BENCH/apps
SCRIPTS=$APPS/healthcare/scripts
SITE=dev.localhost

echo "============================================================"
echo " 繁體中文（台灣）翻譯設定"
echo "============================================================"

# ------------------------------------------------------------------
# 步驟 1：套用 ERPNext zh_TW.po 翻譯（5,520 筆合併翻譯）
# ------------------------------------------------------------------
echo ""
echo "[1/5] 套用 ERPNext 繁體中文翻譯..."
python3 << 'PYEOF'
import json, polib, subprocess, sys

merged_path = '/home/frappe/frappe-bench/apps/healthcare/scripts/erpnext_zh_tw_merged.json'
po_path = '/home/frappe/frappe-bench/apps/erpnext/erpnext/locale/zh_TW.po'
tmp_path = '/tmp/erpnext_zh_TW_setup.po'

try:
    with open(merged_path, encoding='utf-8') as f:
        translations = json.load(f)
except FileNotFoundError:
    print(f'  [SKIP] 找不到合併翻譯檔：{merged_path}')
    sys.exit(0)

po = polib.pofile(po_path)
lookup = {e.msgid: e for e in po}
filled = 0

for msgid, msgstr in translations.items():
    if msgid in lookup:
        entry = lookup[msgid]
        if not entry.msgstr and msgstr:
            entry.msgstr = msgstr
            filled += 1
    else:
        entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
        po.append(entry)
        filled += 1

po.save(tmp_path)
subprocess.run(['cp', tmp_path, po_path], check=True)
print(f'  填入 {filled} 筆翻譯到 ERPNext zh_TW.po')
PYEOF

# ------------------------------------------------------------------
# 步驟 2：修正所有 app 的繁體中文用語（OpenCC + 台灣詞彙對照）
# ------------------------------------------------------------------
echo ""
echo "[2/5] 修正所有 app CSV/PO 用語（OpenCC 轉換 + 台灣詞彙）..."
python3 $SCRIPTS/fix_zhtw_terms.py

# ------------------------------------------------------------------
# 步驟 3：匯入 ERPNext 翻譯到資料庫
# ------------------------------------------------------------------
echo ""
echo "[3/5] 匯入 ERPNext 翻譯（約 10-15 分鐘）..."
cd $BENCH
bench --site $SITE import-translations zh-TW apps/erpnext/erpnext/locale/zh_TW.po
bench --site $SITE import-translations zh-TW apps/erpnext/erpnext/translations/zh-TW.csv

# ------------------------------------------------------------------
# 步驟 4：匯入 Frappe / HRMS 翻譯
# ------------------------------------------------------------------
echo ""
echo "[4/5] 匯入 Frappe / HRMS 翻譯..."
bench --site $SITE import-translations zh-TW apps/frappe/frappe/translations/zh-TW.csv
bench --site $SITE import-translations zh-TW apps/frappe/frappe/locale/zh_TW.po
bench --site $SITE import-translations zh-TW apps/hrms/hrms/translations/zh-TW.csv
bench --site $SITE import-translations zh-TW apps/hrms/hrms/locale/zh_TW.po

# ------------------------------------------------------------------
# 步驟 5：清除快取
# ------------------------------------------------------------------
echo ""
echo "[5/5] 清除快取..."
bench --site $SITE clear-cache

echo ""
echo "============================================================"
echo " 完成！請重新整理瀏覽器。"
echo " DB Translation fixtures 已在 bench migrate 時自動匯入。"
echo "============================================================"
