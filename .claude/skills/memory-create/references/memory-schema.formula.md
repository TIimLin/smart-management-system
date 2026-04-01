# Memory Frontmatter Schema（.formula/memory/ 版）

> 適用於所有 `.formula/memory/{yyMMdd}/{hhmmss}-{topic}.md` 記憶條目。

## 必填欄位

| 欄位 | 格式 | 說明 |
|------|------|------|
| `created` | ISO 8601 `+08:00` | 建立時間（對話發生時間） |
| `modified` | ISO 8601 `+08:00` | 修改時間 |
| `tags` | `[tag1, tag2]` | lowercase-kebab，3–6 個 |
| `note_type` | `memory`（固定值） | 標識為記憶條目 |
| `context` | 一句話 | 觸發此記憶的情境描述 |

## 選填欄位

| 欄位 | 格式 | 說明 |
|------|------|------|
| `related` | `[[note1]], [[note2]]` | 連結到 .formula/notes/ 的相關筆記 |
| `session` | 描述 | 對話 session 的簡短識別 |

## 最小範本

```yaml
---
created: 2026-03-02T10:00:00+08:00
modified: 2026-03-02T10:00:00+08:00
tags: [ai-core, skills-design]
note_type: memory
context: 討論 AI Core 第一波 Skills 設計的決策
---
```

## 完整範本

```yaml
---
created: 2026-03-02T10:00:00+08:00
modified: 2026-03-02T10:00:00+08:00
tags: [ai-core, formula-contract, skills-design]
note_type: memory
context: 確認第一波 Skills 設計方向：formula-contract + note-* + memory-create
related: [[260301 AI Core Skills 架構設計]]
session: 260302 AI Core Skills 設計會議
---
```

## 記憶條目內容結構

$$\text{MemoryEntry} = \text{FrontmatterGen} + \text{CoreFormula} + \text{KeyDecisions} + \text{RelatedLinks}$$

```markdown
## 核心公式

$$\text{主題} = \text{要素1} + \text{要素2}$$

## 關鍵決策

- 決策 1：說明
- 決策 2：說明

## 相關連結

- [[related-note]] — 關聯說明
```

## MEMORY.md 索引格式

$$\text{MEMORY.md} = \text{索引結構} + \sum_{d} \texttt{\{yyMMdd\}/\{hhmmss\}-\{topic\}.md} \to \text{摘要}$$

```markdown
$$\text{Memory} = \text{MEMORY.md}(\text{主記憶索引}) + \sum_{d} \frac{\text{日期}_d}{\text{時間戳-主題.md}}$$

$$\text{索引} = \left\{
\begin{array}{l}
\text{yyMMdd/hhmmss-topic.md} \to \text{一句話摘要} \\
\end{array}
\right.$$

$$\text{更新規則} = \text{memory-create} \to \text{新增條目} \to \text{同步更新此索引}$$
```
