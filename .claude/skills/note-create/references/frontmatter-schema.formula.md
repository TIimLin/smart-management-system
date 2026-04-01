# Note Frontmatter Schema（.formula/notes/ 版）

> 適用於所有 `.formula/notes/{domain}/references/*.md` 筆記。

## 必填欄位

| 欄位 | 格式 | 說明 |
|------|------|------|
| `created` | ISO 8601 `+08:00` | 建立時間（匯入時用 `stat Modify` 時間） |
| `modified` | ISO 8601 `+08:00` | 修改時間（每次更新必須更新此欄位） |
| `tags` | `[tag1, tag2]` | lowercase-kebab，3–8 個 |
| `source_system` | 見下表 | 來源追溯 |
| `note_type` | 見下表 | 筆記類型 |

### source_system 值

$$\text{source\_system} = \text{manual} \mid \text{web} \mid \text{ai-generated} \mid \text{eagle} \mid \text{notion} \mid \text{pdf} \mid \text{docx} \mid \text{xlsx} \mid \text{html} \mid \text{unknown}$$

### note_type 值

$$\text{note\_type} = \text{permanent} \mid \text{literature} \mid \text{fleeting} \mid \text{MOC} \mid \text{memory}$$

- `permanent`：個人洞察、長青知識
- `literature`：文獻、深度研究報告
- `fleeting`：速記、待整理
- `MOC`：Map of Content，索引目錄
- `memory`：專用於 `.formula/memory/`（notes 不用）

## 選填欄位

| 欄位 | 格式 | 說明 |
|------|------|------|
| `related` | `[[note1]], [[note2]]` | 雙向連結 |
| `canvas` | `"[[resources/name.html]]"` | HTML Canvas 視覺化 |
| `para_type` | `resource \| project \| area \| archive` | PARA 分類（可選，向後相容） |

## 最小範本

```yaml
---
created: 2026-03-02T10:00:00+08:00
modified: 2026-03-02T10:00:00+08:00
tags: [topic-tag]
source_system: manual
note_type: permanent
---
```

## 完整範本

```yaml
---
created: 2026-03-02T10:00:00+08:00
modified: 2026-03-02T10:00:00+08:00
tags: [ai-core, formula-contract, skills]
source_system: manual
note_type: permanent
related: [[other-note]], [[another-note]]
canvas: "[[resources/my-note.html]]"
para_type: resource
---
```

## Merge 規則（note-update 用）

$$\text{Merge} = \text{原有欄位值保留} + \text{缺少必填欄位補齊} + \texttt{modified} = \text{今天}$$

絕不覆蓋使用者已填寫的欄位值，只補缺少的。
