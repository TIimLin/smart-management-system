---
name: report-weekly
description: >
  掃描指定目錄下所有專案在各開會區間內的 git 歷史與檔案變更，
  每個開會日期對應一份進度報告，存至 .ai-core/notes/work/references/。
  Trigger: "週會進度", "AI 週會", "本週進度", "幫我整理進度",
  "weekly report", "整理這幾次的週報", "建立週報", "週進度",
  or any request to summarize project progress for one or more meeting dates.
  Output: N files → .ai-core/notes/work/references/{yyMMdd}-weekly-progress.md
argument-hint: "[meeting-dates...] [scan-path]"
disable-model-invocation: false
---

# Report Weekly

$$\text{WeeklyReport}(P,\;\mathcal{M}) = \text{Periods}(\mathcal{M}) \;\xrightarrow{\;\bigoplus\;}\; \text{ScanPeriod}(P,\;S,\;E) \;\to\; \text{Classify} \;\to\; \text{NoteWrite}^{|\mathcal{M}|}$$

## Step 1: ArgParse

$$P_{\text{default}} = \texttt{/mnt/c/Users/user/Documents/Yippine/Program}$$

$$\mathcal{M}_{\text{default}} = [\text{today}], \quad \text{today} = \text{Bash: date}(+\%Y\text{-}\%m\text{-}\%d)$$

```bash
TODAY=$(date +%Y-%m-%d)
```

$$\mathcal{M} = \begin{cases}
[\text{today}] & \text{未給日期參數} \\
[D_1, D_2, ..., D_n] & \text{使用者給定（格式：YYYY-MM-DD 或 MM/DD 或 MMDD，自動標準化）}
\end{cases}$$

$$P = \begin{cases}
\text{args 中含路徑的參數} & \text{有給} \\
P_{\text{default}} & \text{未給}
\end{cases}$$

## Step 2: Periods（核心演算法）

$$\mathcal{M}_{\text{sorted}} = \text{Sort}(\mathcal{M}, \text{ascending})$$

$$D_0 = D_1 - 7\text{d} \quad \text{（第一份報告的起始點預設往回 7 天）}$$

$$\text{Periods} = \{(D_{i-1},\;D_i)\}_{i=1}^{n} \quad \Rightarrow \quad |\mathcal{M}| \text{ 個日期} = |\mathcal{M}| \text{ 份報告}$$

範例：

$$\mathcal{M} = [0325] \;\Rightarrow\; 1 \text{ 份}:\;(0318 \to 0325)$$

$$\mathcal{M} = [0311, 0318, 0325] \;\Rightarrow\; 3 \text{ 份}:\;(0304{\to}0311),\;(0311{\to}0318),\;(0318{\to}0325)$$

$$\mathcal{M} = [0311, 0325] \;\Rightarrow\; 2 \text{ 份}:\;(0304{\to}0311),\;(0311{\to}0325)\quad\text{（間隔不等也正確）}$$

## Step 3: Discover

```bash
# 找出所有有意義的專案目錄（含 .git 或主要語言標記）
find "$SCAN_PATH" -maxdepth 1 -mindepth 1 -type d | sort
```

$$\mathcal{P} = \bigl\{p \mid p \in P/*,\;\exists\;(\texttt{.git} \;\|\; \texttt{package.json} \;\|\; \texttt{pyproject.toml} \;\|\; \texttt{*.py} \;\|\; \texttt{*.ts} \;\|\; \texttt{Makefile})\bigr\}$$

## Step 4: ScanPeriod（對每個 (S, E) 區間平行掃描）

$$\text{ScanPeriod}(P,\;S,\;E) = \bigoplus_{p \in \mathcal{P}}\bigl[\text{Git}(p,\;S,\;E) \;\|\; \text{Files}(p,\;S,\;E)\bigr]$$

```bash
# Git 掃描：取得 commit 列表
git -C "$project" log \
  --after="$S 00:00:00" --before="$E 23:59:59" \
  --oneline --no-merges 2>/dev/null

# 檔案變更掃描：排除常見雜訊目錄
find "$project" \
  -newer "$S_file" ! -newer "$E_file" \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -type f 2>/dev/null | head -20
```

## Step 5: Classify

$$\text{Classify}(p) = \begin{cases}
\text{active} & |\text{Git}(p)| > 0 \\
\text{files\_only} & |\text{Git}(p)| = 0 \;\land\; |\text{Files}(p)| > 0 \\
\text{idle} & \text{otherwise}
\end{cases}$$

## Step 6: Synthesize（AI 語意分析）

對每個 active / files_only 專案：
- 閱讀 commit messages → 用繁體中文摘要成「做了什麼、為什麼」
- 識別主要技術方向（新功能 / 修 bug / 重構 / 研究）
- 評估進度幅度（突破性進展 / 穩定推進 / 微調）

$$\text{Synthesize}(p) = \text{Commits} \to \text{NL}(\text{繁中摘要}) + \text{Type}(\text{功能|修復|重構|研究}) + \text{Momentum}(\text{高|中|低})$$

## Step 7: NoteWrite（每個 Dᵢ 一份）

$$\text{Path} = \texttt{.ai-core/notes/work/references/}\{yyMMdd(D_{i})\}\texttt{-weekly-progress.md}$$

**報告結構**：

```markdown
---
created: {D_i}T{time}+08:00
modified: {D_i}T{time}+08:00
tags: [週報, AI週會, 工作進度, {yyMM}]
source_system: ai-generated
note_type: fleeting
period: "{S} → {E}"
projects_active: {n}
projects_idle: {m}
---

# 週進度報告 {yyMMdd(D_i)}（{S_readable} → {E_readable}）

## 摘要列表（口頭報告用）

- **{project}**：{一句話進度}
- **{project}**：{一句話進度}
- ...（僅列 active + files_only）

---

## 詳細說明

### {project-name}（active）

**進度類型**：{功能開發|修復|重構|研究}
**本期 Commits（{n} 個）**：
- {hash} {date} {commit-message-繁中摘要}
- ...

**主要進展**：
{AI 語意摘要，2-4 句話}

**技術亮點**：{若有值得說的}

---

### {project-name}（files_only）

**有檔案變更但無 commit**
**異動檔案（前 10 個）**：...

---

## 靜止專案

以下專案本期無活動：{project1}, {project2}, ...

---

*生成時間：{today} | 掃描路徑：{P} | 掃描區間：{S} → {E}*
```

## Step 8: Confirm

```
✅ 週報生成完成

報告數量：{n} 份
掃描路徑：{P}
掃描專案：{total} 個（active: {a}, files_only: {f}, idle: {i}）

{i=1..n}
  [{Di}] .ai-core/notes/work/references/{yyMMdd}-weekly-progress.md
         區間：{Si} → {Di}｜活躍專案 {ai} 個

→ note-to-canvas 轉成互動報告｜note-to-xmind 轉成心智圖
```
