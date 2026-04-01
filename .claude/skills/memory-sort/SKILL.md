---
name: memory-sort
description: >
  List and organize memory entries under .ai-core/memory/ by date, topic,
  relevance, or priority quadrant. AI may auto-trigger to scan accumulated
  memories before answering, recalling project history, or prioritizing
  what to surface in current context. Also user-invocable.
  Trigger on "列出記憶", "記憶清單", "sort memory", "整理記憶",
  "記憶時間線", "有哪些記憶", "記憶概況", or when AI needs to survey
  available memories to improve context accuracy.
argument-hint: "[filter: date|topic|tag|quadrant]"
---

# Memory Sort

$$\text{MemorySort} = \text{Scan} \to \text{TimelineIndex} \to \text{Group}(\text{mode}) \to \text{Display}$$

## Step 1: Scan

$$\text{Index} = \text{Read}(\texttt{.ai-core/memory/MEMORY.json})(\text{主索引，快速載入})$$

$$\text{Files} = \text{Glob}(\texttt{.ai-core/memory/\{yyMMdd\}/*.md},\; \text{exclude: archived/})(\text{fallback：補全 JSON 缺漏})$$

若 Glob 發現 JSON 中沒有記錄的檔案 → 提示使用者補跑 memory-create 或手動加入 MEMORY.json。

## Step 2: TimelineIndex

$$\text{每個 entry 提取}: \text{date} + \text{topic}(\text{from filename}) + \text{tags} + \text{importance}(\text{from JSON})$$

## Step 3: Group（依 mode）

$$\text{Mode} = \begin{cases}
\text{date} & \text{時間線（預設，newest first）} \\
\text{topic} & \text{按主題關鍵字分組} \\
\text{tag} & \text{按 tags 分組} \\
\text{quadrant} & \text{按重要 \times 緊急四象限分類}
\end{cases}$$

**quadrant 模式**：

$$\text{Importance}(m) = \text{MEMORY.json entry.importance}(\text{直接讀欄位，消除幻覺})$$

$$\text{Urgency}(m, ctx) = \text{TagOverlap}(m.tags,\; ctx.keywords) + \text{Recency}(m.date)(\text{動態計算})$$

$$\text{EffectiveRank}(m, ctx) = 0.5 \cdot \text{Importance} + 0.3 \cdot \text{TagOverlap} + 0.2 \cdot \text{Recency}$$

$$\text{Quadrant} = \begin{cases}
\text{Q1: 重要且緊急} & \to \text{立即載入} \\
\text{Q2: 重要不緊急} & \to \text{深度參考} \\
\text{Q3: 緊急不重要} & \to \text{快速瀏覽} \\
\text{Q4: 不重要不緊急} & \to \text{略過或 archive}
\end{cases}$$

## Step 4: Display

```
🧠 Memory Timeline  [{mode}]

2026-03-06  ({N} entries)
  090506-ai-core-next-wave-planning.md  ★5  [AI-Core, workflow]
             → AI Core 下一波規劃：四大 Contracts、五大 Groups

2026-03-05  ({N} entries)
  ...

Summary: {N} total across {D} days  |  MEMORY.json last updated: {date}

→ memory-read 搜尋特定記憶
→ memory-archive 封存不再需要的記憶
```
