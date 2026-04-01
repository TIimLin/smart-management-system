# Commit Format

$$\text{CommitMsg} = \text{Title} + \text{Body}$$

## Type 分類

$$\text{Type} = add \mid fix \mid update \mid refactor \mid remove$$

| Type | 用途 |
|------|------|
| `add` | 新增功能、模組、檔案 |
| `fix` | 修正問題 |
| `update` | 改善或調整既有功能 |
| `refactor` | 重構，不影響外部行為 |
| `remove` | 刪除功能或檔案 |

## Title 規則

$$\text{Title} = \text{SameType}(\text{,join}) \mid \text{DiffType}(\text{;join})$$

- **功能層級**：列舉主要功能/修復，不窮舉檔案名（細節放 body）
- 對照 `git log main --oneline -5`，確保風格與現有 commit 一致
- 相同 type 用逗號串接：`fix: X, Y`
- 不同 type 用分號分隔：`add: X; fix: A, B; remove: C; refactor: D`
- **禁止**加版本號前綴（`v6:` 等），永遠直接用 type 開頭

## Body 規則

$$\text{Body} = \sum_i \text{"-"} + \text{ type: description}$$

- 每條異動獨立一行，`- {type}: {description}` 格式
- 具體技術描述（**禁用** "various changes"、"minor updates"、"improvements" 等模糊詞）
- 同類型多條可合併：`- add: X, Y, Z`

## 完整格式

```
{type}: {change1}, {change2}; {type}: {change3}

- {type}: {concrete description}
- {type}: {concrete description}
- ...
```

## 範例

```
add: squash-release formula redesign; refactor: commit-format extracted to references

- add: SKILL.md rewritten with Formula-Contract notation (148→70 lines)
- add: references/commit-format.formula.md for on-demand loading
- refactor: workflow steps compressed to formula expressions
- remove: disable-model-invocation non-standard field
```
