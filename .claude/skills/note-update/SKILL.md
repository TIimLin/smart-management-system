---
name: note-update
description: >
  Update content or frontmatter of an existing note under .ai-core/notes/.
  Use when user says "更新筆記", "修改", "補充", "補全 frontmatter", "fix frontmatter",
  or when a note has missing/incorrect fields. Absorbs note-frontmatter duties.
argument-hint: "[filepath]"
---

# Note Update

$$\text{NoteUpdate} = \text{TargetResolve} \to (\text{Read} \;\&\; \text{Stat}) \to \text{ModeDetect} \to \text{MergeWrite} \to \text{Confirm}$$

## Step 1: TargetResolve

$$\text{Target} = \text{args} \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

## Step 2: 讀取（並行）

$$\text{Read}(\text{target}) \;\&\; \text{Bash:stat}(\text{target})$$

## Step 3: ModeDetect

$$\text{Mode} = \text{content} \mid \text{frontmatter} \mid \text{both}$$

- "補充內容", "修改內文" → `content`
- "補齊 frontmatter", "缺少欄位", "fix frontmatter" → `frontmatter`
- 無明確指定 → 詢問使用者

## Step 4: MergeWrite

### Frontmatter 更新（`frontmatter` | `both` mode）

Schema 參考 `.claude/skills/note-create/references/frontmatter-schema.formula.md`。

$$\text{Merge} = \text{原有欄位保留} + \text{缺少必填欄位補齊} + \texttt{modified} = \text{今天}$$

使用 `Edit` 工具整塊替換 `---...---` 區塊：

```
old_string: {原有完整 ---...--- 區塊}
new_string: {合併後完整 ---...--- 區塊}
```

### Content 更新（`content` | `both` mode）

使用 `Edit` 工具精準替換，保留未修改部分。

## Step 5: Confirm

```
✅ Note updated

File:   {filepath}
Mode:   {content | frontmatter | both}
Added:  {新增的欄位或內容摘要}
Kept:   {保留的欄位清單}
```
