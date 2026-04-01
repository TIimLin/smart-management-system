---
name: note-read
description: >
  Search and read notes from .ai-core/notes/ knowledge base. Auto-trigger when user
  references a topic that may exist in notes, asks "找筆記", "有沒有筆記", "搜尋",
  "查一下", or needs context from knowledge base before answering a question.
---

# Note Read

$$\text{NoteRead} = \text{QueryParse} \to \text{Search} \to \text{Rank} \to \text{Display} \to \sim(\text{found}) \to \text{suggest}(\text{note-create})$$

## Step 1: QueryParse

$$\text{Query} = \text{keywords} + \text{domain?} + \text{tags?} + \text{date\_range?}$$

從使用者請求提取：主題關鍵字、domain 限定（可選）、tag 過濾（可選）。

## Step 2: Search（並行）

$$\text{Search} = \text{GlobAll} \;\&\; \text{GrepFrontmatter} \;\&\; \text{GrepContent}$$

```
Glob:  .ai-core/notes/**/*.md
Grep frontmatter: tags, note_type 過濾
Grep content: 關鍵字全文搜尋
```

排除 `archived/` 目錄。

## Step 3: Rank

$$\text{Rank} = \text{exact title match} > \text{tag match} > \text{content match}$$

## Step 4: Display

$$(\text{單一結果}) \to \text{Read 完整內容展示}$$

$$(\text{多個結果}) \to \text{列出清單} \to \text{詢問展開哪一個}$$

$$(\text{無結果}) \to \text{回報「未找到」} \to \text{建議 note-create}$$

```
Found: {N} notes matching "{query}"

1. .ai-core/notes/{domain}/references/{filename}.md
   Tags: {tags} | Type: {note_type} | Modified: {date}
   Preview: {first 100 chars of content}
```
