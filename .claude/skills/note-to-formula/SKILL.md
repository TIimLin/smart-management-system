---
name: note-to-formula
description: >
  Convert a natural language note (*.md) to LaTeX formula representation (*.formula.md).
  Creates a SAME-NAME .formula.md file in the SAME directory as the source.
  Trigger when user says "公式化", "轉成 formula", "formula 版", "幫我 formula 化",
  or when a .md note lacks a corresponding .formula.md.
argument-hint: "[filepath | keyword]"
disable-model-invocation: false
---

# Note To Formula

$$\text{NoteToFormula} = \text{SourceResolve} \to \text{CheckExisting} \to \text{FormulaGen} \to \text{Write} \to \text{FrontmatterUpdate} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{Source} = \text{args} \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

$$\text{OutputPath} = \text{source.dir} / \text{source.stem} + \texttt{.formula.md}$$

範例：`references/API Design.md` → `references/API Design.formula.md`（同目錄、同名）

## Step 2: CheckExisting

$$(\texttt{*.formula.md} \text{ 已存在}) \to \text{詢問：覆蓋還是跳過？}$$

## Step 3: FormulaGen

參考 `references/formula-gen.formula.md` 的生成規範。

核心指令（直接執行）：
> 閱讀 source 筆記全文，以純繁體中文 LaTeX 數學公式，用簡單・有效・系統・全面的方式分析和講解此主題。使用臺灣字詞與語法。繁中術語 + 數學運算符。大寫可運算函數，小寫特定值。

## Step 4: Write

```markdown
---
created: {今天}
modified: {今天}
tags: {source.tags}
note_type: formula
source: {source_filepath}
---

{generated LaTeX formula content}
```

## Step 5: FrontmatterUpdate（source 筆記）

$$\text{source.related} \mathrel{+}= [[\text{stem}\texttt{.formula.md}]]$$

## Step 6: Confirm

```
✅ Formula note created

Source:  {source_path}
Output:  {same_dir}/{stem}.formula.md
source.related: updated
```
