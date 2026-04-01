---
name: memory-update
description: >
  Update content or metadata of an existing memory entry in .ai-core/memory/.
  Use when user says "更新記憶", "修改記憶", "補充那個記憶", or when a memory
  entry has outdated information that needs correction. Always refreshes MEMORY.json index.
argument-hint: "[filepath | topic-keyword]"
---

# Memory Update

$$\text{MemoryUpdate} = \text{TargetResolve} \to (\text{Read} \;\&\; \text{Stat}) \to \text{ModeDetect} \to \text{MergeWrite} \to \text{IndexRefresh} \to \text{Confirm}$$

## Step 1: TargetResolve

$$\text{Target} = \text{args} \mid \text{memory-read}(\text{keyword}) \mid \text{Ask}$$

## Step 2: 讀取（並行）

$$\text{Read}(\text{target}) \;\&\; \text{Bash:stat}(\text{target})$$

## Step 3: ModeDetect

**前置攔截**：使用者提到 importance / 重要性 → 直接執行 ImportanceUpdate，跳過後續步驟：

$$\text{ImportanceUpdate}: \text{Read}(\texttt{MEMORY.json}) \to \text{find entry where file = target} \to \text{update importance} \to \text{update updated} \to \text{Write}(\texttt{MEMORY.json})$$

**一般模式**：

$$\text{Mode} = \begin{cases}
\text{content} & \text{"補充內容", "修改"} \\
\text{frontmatter} & \text{"補齊欄位", "fix frontmatter"} \\
\text{both} & \text{無明確指定} \to \text{詢問使用者}
\end{cases}$$

## Step 4: MergeWrite

$$\texttt{modified} = \text{今天（必須更新）}$$

使用 `Edit` 工具精準修改，保留未修改部分。

## Step 5: IndexRefresh

$$(\text{summary 有變動}) \to \text{更新 MEMORY.json 對應 entry 的 summary}$$

$$(\text{tags 有變動}) \to \text{更新 MEMORY.json 對應 entry 的 tags}(\text{sync})$$

操作：`Read(MEMORY.json)` → find entry where `file` matches → update fields → `Write(MEMORY.json)` + 更新頂層 `updated`

## Step 6: Confirm

```
✅ Memory updated

File:   {filepath}
Mode:   {content | frontmatter | both | importance}
```
