---
name: memory-read
description: >
  Search and retrieve memories from .ai-core/memory/. Auto-trigger when user
  references past conversation context, says "記得嗎", "之前我們", "上次說的",
  "回顧一下", "有沒有記憶", or when answering questions where past decisions
  or insights from previous sessions would improve accuracy.
---

# Memory Read

$$\text{MemoryRead} = \text{QueryParse} \to (\text{IndexScan} \;\&\; \text{FileSearch}) \to \text{Rank} \to \text{Display}$$

## Step 1: QueryParse

$$\text{Query} = \text{keywords} + \text{date\_range?} + \text{tags?}$$

從使用者請求或對話上下文提取搜尋意圖。

## Step 2: Search（並行）

$$\text{IndexScan}: \text{Read}(\texttt{.ai-core/memory/MEMORY.json}) \to \text{filter by tags} \mid \text{importance}$$

$$\text{FileSearch}: \text{Grep}(\text{keywords},\; \texttt{.ai-core/memory/**/*.md},\; \text{exclude: archived/})$$

IndexScan 直接對 JSON `entries` 做欄位過濾，無需解析 formula 格式。

## Step 3: Rank

$$\text{EffectiveRank}(m, ctx) = 0.5 \cdot \text{importance} + 0.3 \cdot \text{TagOverlap}(m.tags,\; ctx.keywords) + 0.2 \cdot \text{Recency}(m.date)$$

- `importance`：直接讀 MEMORY.json entry 欄位
- `TagOverlap`：m.tags 中有幾個出現在當前對話關鍵字
- `Recency`：越新越高，但不主導排序

## Step 4: Display

$$(\text{單一結果}) \to \text{Read 完整內容展示}$$

$$(\text{多個結果}) \to \text{列出清單} + \text{詢問展開哪一個}$$

$$(\text{無結果}) \to \text{回報「未找到」} + \text{建議 memory-create}$$

```
Found: {N} memories matching "{query}"

1. .ai-core/memory/{yyMMdd}/{hhmmss}-{topic}.md
   Tags: {tags} | Importance: {1–5} | Created: {date}
   Preview: {first 100 chars of content}
```
