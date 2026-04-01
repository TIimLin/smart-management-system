---
name: note-sort
description: >
  List and organize notes under .ai-core/notes/ by domain, tags, date, keyword,
  or priority quadrant. AI may auto-trigger to browse the knowledge base before
  answering questions, checking duplicates before note-create, or prioritizing
  by importance×urgency quadrant. Also user-invocable.
  Trigger on "列出筆記", "知識庫概況", "整理筆記", "相關筆記有哪些",
  "sort notes", "筆記清單", "有沒有相關筆記", or when AI needs to scan
  available knowledge to improve response quality.
argument-hint: [filter: domain|tag|keyword|quadrant]
---

# Note Sort

$$\text{NoteSort} = \text{Scan} \to \text{Index} \to \text{Group}(\text{mode}) \to \text{Display}$$

## Step 1: Scan

$$\text{Files} = \text{Glob}(\texttt{.ai-core/notes/**/references/*.md},\; \text{exclude: archived/})$$

## Step 2: Index

$$\text{每個檔案提取}: \text{domain} + \text{tags} + \text{created} + \text{modified} + \text{note\_type} + \text{related count} + \text{file\_suffix}$$

$$\text{file\_suffix} = \begin{cases} \texttt{.formula.md} & \text{公式化衍生} \\ \texttt{.mermaid.md} & \text{圖表衍生} \\ \texttt{.xmind.md} & \text{心智圖衍生} \\ \texttt{.md} & \text{主體筆記} \end{cases}$$

## Step 3: Group（依 mode）

$$\text{Mode} = \begin{cases} \text{domain} & \text{按領域分組（預設）} \\ \text{tag} & \text{按 tags 分組} \\ \text{keyword} & \text{全文搜尋後分組} \\ \text{date} & \text{按建立時間排序} \\ \text{quadrant} & \text{按重要 \times 緊急四象限分類} \end{cases}$$

**quadrant 模式**（AI 自主排查時最有價值）：

$$\text{Importance} = f(\text{related count} + \text{note\_type=permanent} + \text{tags 覆蓋度})$$

$$\text{Urgency} = f(\text{modified 近期} + \text{fleeting type} + \text{上下文相關度})$$

$$\text{Quadrant} = \begin{cases} \text{Q1: 重要且緊急} & \to \text{優先閱讀} \\ \text{Q2: 重要不緊急} & \to \text{深度參考} \\ \text{Q3: 緊急不重要} & \to \text{快速瀏覽} \\ \text{Q4: 不重要不緊急} & \to \text{略過} \end{cases}$$

## Step 4: Display

**note_type 兩個維度說明**：

$$\text{note\_type（frontmatter）} \neq \text{file\_suffix（檔名）}$$

$$\text{note\_type} = \begin{cases} \text{permanent} & \text{你自己的洞察、長青知識（主觀沉澱）} \\ \text{literature} & \text{外部文獻、研究報告、匯入資料（客觀參考）} \\ \text{fleeting} & \text{速記、待整理} \\ \text{MOC} & \text{目錄索引頁} \end{cases}$$

同一個主題可同時有多個 file\_suffix：`API-Design.md` + `API-Design.formula.md` + `API-Design.mermaid.md`，三者共享相同的 `note_type`。

```
📚 Knowledge Base  [{mode}]

{domain: work}  ({N} notes)
  [permanent]   API-Design.md              2026-03-01  tags: [api, design]
  [permanent]   API-Design.formula.md      2026-03-01  ← .formula.md 衍生
  [literature]  Effective-Java.md          2026-02-15  tags: [java, book]
  [literature]  Effective-Java.mermaid.md  2026-02-15  ← .mermaid.md 衍生

{domain: learning}  ({N} notes)
  ...

─────────────────────────────────────────────────────
Summary: {N} notes total

  By note_type:  permanent {N}  ·  literature {N}  ·  fleeting {N}  ·  MOC {N}
  By file type:  .md {N}  ·  .formula.md {N}  ·  .mermaid.md {N}  ·  .xmind.md {N}
```
