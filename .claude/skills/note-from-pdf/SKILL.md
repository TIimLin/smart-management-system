---
name: note-from-pdf
description: >
  Extract content from a PDF file and create a corresponding .md note in
  .ai-core/notes/{domain}/references/. Moves the PDF to resources/ with
  same-name mapping. Uses Python pdfplumber for extraction.
  Trigger on "從 PDF 建立筆記", "import PDF", "PDF 轉 md",
  "PDF 匯入", "*.pdf → *.md", "把這個 PDF 整理成筆記".
argument-hint: "[pdf-path] [domain]"
disable-model-invocation: false
---

# Note From PDF

$$\text{NoteFromPDF} = \text{Locate} \to \text{Extract} \to \text{TypeDetect} \to \text{Draft} \to \text{Save} \to \text{ResourceLink} \to \text{Confirm}$$

## Step 1: Locate

$$\text{PDF} = \text{args}[0] \mid \text{Ask}$$

$$\text{Domain} = \text{args}[1] \mid \text{ContentInfer} \mid \text{Ask}(\{\text{work, learning, life, spirit, 其他}\})$$

$$\text{OutputDir} = \texttt{.ai-core/notes/\{domain\}/references/}$$

$$\text{ResourceDir} = \texttt{.ai-core/notes/\{domain\}/resources/}$$

## Step 2: Extract

參考 `references/pdf-formats.formula.md` 的格式策略。

```bash
python3 ".claude/skills/note-from-pdf/scripts/extract.py" "{pdf-path}"
```

$$\text{提取}: \text{文字內容} + \text{metadata}(\text{title, author, pages, created\_date})$$

$$(\text{image-heavy 偵測}) \to \text{提示：此 PDF 主要為圖片，提取品質可能有限}$$

## Step 3: TypeDetect（PDF 內容類型）

$$\text{ContentType} = \begin{cases} \text{article/report} & \to \text{note\_type: literature} \\ \text{slide/presentation} & \to \text{note\_type: literature，保留標題層次} \\ \text{manual/spec} & \to \text{note\_type: literature，保留章節} \\ \text{mixed/unknown} & \to \text{note\_type: literature} \end{cases}$$

## Step 4: Convert（原文轉換，嚴禁摘要）

$$\text{Convert} = \text{extract.py} \to \text{JSON} \xrightarrow{\text{convert.py}} \text{verbatim Markdown}$$

執行轉換腳本（確定性轉換，不經 AI 改寫）：

```bash
python3 ".claude/skills/note-from-pdf/scripts/extract.py" "{pdf-path}" 2>/dev/null \
  | python3 ".claude/skills/note-from-pdf/scripts/convert.py" -
```

**轉換規則（convert.py 內建）**：
- 每頁開頭插入 `<!-- Page N -->`（品質驗證錨點）
- 標題偵測：優先用 `heading_hints`（font-size），fallback 用文字規律（數字章節、短行）
- 表格：`tables_markdown` 轉為 markdown table，插入對應頁尾
- 縮排區塊：自動包入 ` ``` `
- 重複頁首/頁尾（連續 ≥3 頁相同文字）：略過
- **其餘所有文字原樣保留，零刪減**

**絕對禁止（AI 介入時同樣適用）**：
- ❌ 摘要（summarize）
- ❌ 改寫（paraphrase）
- ❌ 刪減（omit）任何內容
- ❌ 重新排列段落或章節順序

## Step 5: Save

frontmatter 依 `note-create/references/frontmatter-schema.formula.md` 規範：

```markdown
---
created: {PDF metadata created_date | stat Modify | today，ISO 8601 +08:00}
modified: {today ISO 8601 +08:00}
tags: [{domain}, {inferred-topic-tags}]
source_system: pdf
note_type: literature
related: [[resources/{stem}.pdf]]
---

# {Title}

> 來源：{original_pdf_filename}  |  {pages} 頁  |  作者：{author | 不詳}

{structured summary}
```

保存至 `references/{stem}.md`

## Step 6: ResourceLink

```bash
mkdir -p ".ai-core/notes/{domain}/resources"
cp "{pdf-path}" ".ai-core/notes/{domain}/resources/{stem}.pdf"
```

$$\text{同名映射}: \text{resources/A.pdf} \leftrightarrow \text{references/A.md}$$

## Step 7: Confirm

```
✅ PDF imported

Note:     .ai-core/notes/{domain}/references/{stem}.md
Resource: .ai-core/notes/{domain}/resources/{stem}.pdf
Pages:    {N}  |  Extraction: {quality: good | limited (image-heavy)}
Type:     {note_type}  |  Source: {source_system: pdf}
```
