---
name: note-to-canvas
description: >
  Convert a markdown note (*.md or *.formula.md) to a self-contained interactive
  HTML report for executive/team presentation. Output is plain-language繁體中文,
  no LaTeX symbols. Saved as SAME-NAME .html in .ai-core/notes/{domain}/resources/.
  Trigger when user says "canvas", "互動圖", "html 圖", "note-to-canvas",
  "轉成 canvas", "做成互動頁面", "視覺化這個筆記", "報告給主管看", "給團隊看".
argument-hint: "[filepath | keyword]"
user-invocable: true
layer: 5
type: conversion
disable-model-invocation: false
---

# Note To Canvas

$$\text{NoteToCanvas} = \text{SourceResolve} \to \text{CheckExisting} \to \text{TypeDetect} \to \text{CanvasGen} \to \text{Write} \to \text{LinkUpdate} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{OutputPath} = \texttt{.ai-core/notes/\{domain\}/resources/\{stem\}.html}$$

例：`.ai-core/notes/work/references/AI Design.md` → `.ai-core/notes/work/resources/AI Design.html`

## Step 2: CheckExisting

$$(\texttt{resources/\{stem\}.html} \exists) \to \text{詢問：覆蓋或跳過？}$$

## Step 3: TypeDetect

$$\text{VisualType} \in \{nodeGraph,\; timeline,\; hierarchy,\; dashboard\}$$

## Step 4: CanvasGen

$$(\texttt{.ai-core/notes/*/resources/*.html} \exists) \to \text{Scan} \to \text{StyleAlign},\quad \sim\exists \to \text{UseDefault}$$

$$\text{Layout} = [\text{Header}] \to [\text{ExecutiveSummary}] \to [\text{Sections}(\text{VisualType})] \to [\text{Footer} \leftarrow \text{原始筆記}]$$

$$\text{Style} = \begin{cases}
bg & \texttt{\#0f172a} \\
header & \texttt{\#1e3a5f} \to \texttt{\#2d6a9f} \\
card & \{bg: \texttt{\#1e293b},\; border: \texttt{\#334155},\; radius: 12px\} \\
accent & \{\texttt{\#38bdf8},\; \texttt{\#34d399},\; \texttt{\#f59e0b}\} \\
font & \{body: 15px,\; title: 20px,\; summary: 17px,\; family: \text{system-ui}\}
\end{cases}$$

$$\text{Language} = \text{繁中口語} \times \sim\text{LaTeX} \times \text{formula} \xrightarrow{\text{翻譯}} \text{白話},\quad \text{ExecutiveSummary} \leq 4\text{ sentences}$$

$$\text{Tech} = \text{zero-CDN} \times \text{CSS/JS-inline} \times \{hover,\; accordion,\; responsive\}$$

## Step 5: Write

$$\texttt{resources/\{stem\}.html} = \text{CSS + JS 內嵌自包含 HTML}$$

## Step 6: LinkUpdate（雙向）

$$\text{md frontmatter}: \texttt{canvas: "resources/\{stem\}.html"}$$

$$\text{html}: \texttt{<a href="../references/\{stem\}.md">← 原始筆記</a>}$$

## Step 7: Confirm

```
✅ Canvas created
Source: {source}  Output: .ai-core/notes/{domain}/resources/{stem}.html
Type: {visual_type}  Links: md ↔ html（雙向）
```
