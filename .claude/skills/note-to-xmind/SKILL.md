---
name: note-to-xmind
description: >
  Convert a markdown note (*.md or *.formula.md) to XMind mind map description,
  saved as SAME-NAME .xmind.md in the SAME directory as the source.
  Filename stem: topic.formula.md → topic.xmind.md (strip .formula from filename only).
  Formula content is NOT removed — LaTeX is translated to plain-language xmind nodes.
  Best for hierarchical notes. Trigger when user says "心智圖", "xmind",
  "轉成心智圖", "mind map 版", "*.xmind.md", or when note has clear H1/H2/H3.
argument-hint: "[filepath | keyword]"
user-invocable: true
layer: 5
type: conversion
disable-model-invocation: false
---

# Note To XMind

$$\text{NoteToXMind} = \text{SourceResolve} \to \text{CheckExisting} \to \text{StructureCheck} \to \text{XMindGen} \to \text{Write} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{stem} = \begin{cases} \texttt{topic} & \text{source} = \texttt{topic.md} \\ \texttt{topic} & \text{source} = \texttt{topic.formula.md} \text{（去除 .formula 部分）} \end{cases}$$

$$\text{OutputPath} = \text{source.dir} / \text{stem} + \texttt{.xmind.md}$$

## Step 2: CheckExisting

$$(\texttt{*.xmind.md} \exists) \to \text{詢問：覆蓋或跳過？}$$

## Step 3: StructureCheck

$$\sim\text{Hierarchical}(\text{source}) \to \text{警告：建議改用 note-to-mermaid}$$

## Step 4: XMindGen

$$\text{Root} = \text{H1}, \quad \text{Branch}_i = \text{H2}, \quad \text{Sub}_{ij} = \text{H3/條目}, \quad \text{Leaf} = \text{細節}$$

$$\text{source\_type} = \texttt{formula.md} \Rightarrow \text{LaTeX} \xrightarrow{\text{翻譯}} \text{白話繁中 xmind nodes},\quad \sim\text{保留符號}$$

## Step 5: Write

```markdown
---
note_type: xmind
source: {source_filepath}
source_type: {formula | markdown}
xmind_root: {H1}
---
# Root：{H1}
## Branch 1：{H2}
- Sub 1.1：{重點}
```

## Step 6: Confirm

```
✅ XMind created: {stem}.xmind.md  Root: {H1}  Branches: {N}
```
