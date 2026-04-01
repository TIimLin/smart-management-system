---
name: note-from-docx
description: >
  Extract content from a Word document (.docx, .doc) and create a corresponding
  .md note in .ai-core/notes/{domain}/references/.
  Copies the source file to resources/ with same-name mapping.
  Images are exported to resources/{stem}/ subdirectory (only created if images exist).
  Uses python-docx for .docx; falls back to python-doc2txt / antiword for legacy .doc.
  Trigger on "從 Word 建立筆記", "import Word", "Word 轉 md", "docx 轉 md",
  "Word 匯入", "*.docx → *.md", "把這個 Word 整理成筆記", "word 檔轉筆記".
argument-hint: [docx-path] [domain]
user-invocable: true
layer: 5
type: conversion
disable-model-invocation: false
---

# Note From Docx

$$\text{NoteFromDocx} = \text{Locate} \to \text{Extract} \to \text{Convert} \to \text{Save} \to \text{ResourceLink} \to \text{Confirm}$$

## Step 1: Locate

$$\text{DocxFile} = \text{args}[0] \mid \text{Ask},\quad \text{Ext} \in \{.docx,\; .doc\}$$

$$\text{Domain} = \text{args}[1] \mid \text{ContentInfer} \mid \text{Ask}(\{work,\; learning,\; life,\; spirit,\; \text{其他}\})$$

$$\text{OutputDir} = \texttt{.ai-core/notes/\{domain\}/references/}$$

$$\text{ResourceDir} = \texttt{.ai-core/notes/\{domain\}/resources/}$$

## Step 2: Extract + Convert（原文轉換，嚴禁摘要）

```bash
python3 ".claude/skills/note-from-docx/scripts/extract.py" \
  "{docx-path}" \
  ".ai-core/notes/{domain}/resources/{stem}/note-from-docx" \
  2>/dev/null \
  | python3 ".claude/skills/note-from-docx/scripts/convert.py" - "../resources/{stem}/note-from-docx"
```

$$\text{HeadingSource} = \begin{cases}
\texttt{Heading 1/2/3} \text{ 樣式} & \to \#\; /\; \#\#\; /\; \#\#\# \\
\text{Bold 短行} \leq 80\text{ 字元} & \to \text{fallback 推斷} \\
\text{普通段落} & \to \text{原樣保留}
\end{cases}$$

$$(.doc \text{ fallback}) \to \text{提示：舊格式，僅純文字，不含圖片與樣式}$$

**絕對禁止**：
- ❌ 摘要（summarize）
- ❌ 改寫（paraphrase）
- ❌ 刪減（omit）任何內容
- ❌ 重新排列段落或章節順序

## Step 3: Save

frontmatter 依 `note-create/references/frontmatter-schema.formula.md` 規範：

```markdown
---
created: {Word metadata created | stat Modify | today，ISO 8601 +08:00}
modified: {today ISO 8601 +08:00}
tags: [{domain}, {inferred-topic-tags}]
source_system: docx
note_type: literature
related: [[resources/{stem}{ext}]]
---

# {Title}

> 來源：{original_filename}  |  作者：{author | 不詳}  |  格式：{.doc | .docx}

{converted markdown content}
```

保存至 `references/{stem}.md`

## Step 4: ResourceLink

```bash
# 主檔同名映射（平層，維持 references ↔ resources 對應關係）
cp "{docx-path}" ".ai-core/notes/{domain}/resources/{stem}{ext}"

# 圖片目錄：僅在 extract 實際輸出圖片時才存在
# resources/{stem}/note-from-docx/ 由 extract.py 按需建立（無圖片則不建立）
```

$$\text{同名映射}: \text{resources/A.docx} \leftrightarrow \text{references/A.md} \quad \text{（平層，不變）}$$

$$\text{圖片 subdirectory}: \text{resources/A/note-from-docx/fig\_N.png} \quad \text{（工具專屬目錄，按需建立）}$$

## Step 5: Confirm

```
✅ Docx imported

Note:     .ai-core/notes/{domain}/references/{stem}.md
Resource: .ai-core/notes/{domain}/resources/{stem}{ext}
Format:   {.doc | .docx}  |  Fallback: {yes | no}
Images:   {N} exported to resources/{stem}/note-from-docx/ | none
```
