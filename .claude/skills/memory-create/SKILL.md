---
name: memory-create
description: >
  Capture key insights from conversation into .ai-core/memory/{yyMMdd}/{hhmmss}-{topic}.md.
  Auto-trigger after significant decisions, discoveries, design discussions, or when user says
  "記住", "記錄下來", "幫我記", "記憶一下". Also updates MEMORY.json index.
argument-hint: [topic]
---

# Memory Create

$$\text{MemoryCreate} = \text{InsightExtract} \to \text{PathResolve} \to \text{FrontmatterGen} \to \text{Write} \to \text{IndexUpdate} \to \text{Confirm}$$

> ⚠️ **路徑強制規則**：永遠寫入 `.ai-core/memory/{yyMMdd}/{hhmmss}-{topic}.md`（專案根目錄下）。
> 禁止寫入系統 auto-memory 路徑（`~/.claude/projects/...`），該路徑與本系統無關。

## Step 1: InsightExtract

從對話中提取：

$$\text{Insight} = \text{key\_decisions} + \text{context} + \text{conclusions} + \text{related\_topics}$$

以 formula 形式表達核心內容（極簡、精確、無冗餘）。

## Step 2: PathResolve

$$\text{Path} = \texttt{.ai-core/memory/\{yyMMdd\}/\{hhmmss\}-\{topic-kebab\}.md}$$

$$\text{topic-kebab}: \text{英文 kebab-case，}\leq 40 \text{ 字元}$$

$$\sim(\text{dir 存在}) \to \texttt{mkdir -p .ai-core/memory/\{yyMMdd\}/}$$

## Step 3: FrontmatterGen

參考 `references/memory-schema.formula.md`。

必填：`created`, `modified`, `tags`, `note_type: memory`, `context`

## Step 4: Write（formula 形式優先）

```markdown
---
{frontmatter}
---

## 核心公式

$$\text{主題} = \text{要素1} + \text{要素2}$$

## 關鍵決策

- 決策 1：...
- 決策 2：...

## 相關連結

- [[相關筆記]] — {關聯說明}
```

## Step 5: IndexUpdate

$$\text{Read}(\texttt{.ai-core/memory/MEMORY.json}) \to \text{PrependEntry} \to \text{Write}(\texttt{.ai-core/memory/MEMORY.json})$$

新 entry 插入 `entries` 陣列**最前面**（newest first）：

```json
{
  "file": "{yyMMdd}/{hhmmss}-{topic}.md",
  "date": "{YYYY-MM-DD}",
  "tags": [{從 frontmatter 複製}],
  "importance": {AI 依內容類型評估，1–5},
  "summary": "{一句話摘要}"
}
```

**importance 評分依據**：

$$\text{importance} = \begin{cases}
5 & \text{架構決策、系統設計變更、核心設計律} \\
4 & \text{使用者個性/偏好、里程碑規劃、個人重大危機} \\
3 & \text{工具/硬體決策、重要自動化流程設計} \\
2 & \text{常規任務背景、短期上下文} \\
1 & \text{暫時過渡資訊、很快就會過期的記憶}
\end{cases}$$

同步更新頂層欄位：`total += 1`，`updated = 今日 ISO 時間`

## Step 6: Confirm

```
✅ Memory created

Path:    .ai-core/memory/{yyMMdd}/{hhmmss}-{topic}.md
Topic:   {topic}
Tags:    {tags}
Importance: {1–5}
MEMORY.json 已更新（倒序，最新在最前）

→ 若有相關筆記，建議使用 memory-link 建立雙向連結
```
