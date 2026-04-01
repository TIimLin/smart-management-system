---
name: note-to-notebooklm
description: >
  Convert a markdown note to a NotebookLM-ready package: {scope}.prompt.md
  under references/{stem}/note-to-notebooklm/ + auto-collected source files under resources/{stem}/note-to-notebooklm/.
  Trigger when user says "notebooklm", "notebook lm", "準備 notebooklm",
  "轉成 notebooklm", "notebooklm 包", "生成 notebooklm prompt".
argument-hint: "[filepath | keyword] [scope: briefing|report|faq|podcast|summary]"
user-invocable: true
layer: 5
type: conversion
disable-model-invocation: false
---

# Note To NotebookLM

$$\text{NoteToNotebookLM} = \text{SourceResolve} \to \text{ScopeResolve} \to \text{Analyze} \to \text{PromptGen} \to \text{Write} \to \text{SourcesCollect} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{Source} = \text{args}[0] \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

$$\text{stem} = \text{source.stem} \quad \text{（去除副檔名）}$$

$$\text{PromptPath} = \text{source.dir} / \text{stem} / \texttt{note-to-notebooklm} / \texttt{\{scope\}.prompt.md}$$

$$\text{SourcesPath} = \text{source.domain\_resources} / \text{stem} / \texttt{note-to-notebooklm} / \quad \text{（.ai-core/notes/\{domain\}/resources/\{stem\}/note-to-notebooklm/）}$$

範例：`references/期中報告.md` →
- `references/期中報告/note-to-notebooklm/briefing.prompt.md`
- `resources/期中報告/note-to-notebooklm/`（自動收集的上傳檔）

## Step 2: ScopeResolve

$$\text{Scope} \in \{\text{briefing},\; \text{report},\; \text{faq},\; \text{podcast},\; \text{summary}\} \quad\leftarrow\quad \text{args}[1] \mid \text{Infer}(\text{H1} + \text{tags}) \mid \text{Ask}$$

$$(\text{PromptPath} \exists) \to \text{詢問：覆蓋或跳過？}$$

## Step 3: Analyze

$$\text{Structure} = \text{H1} + \text{H2[]} + \text{frontmatter}(\text{tags},\; \text{related},\; \text{note\_type})$$

$$\text{Files} = \underbrace{\{P_\text{source}\}}_{\text{必要}} \cup \underbrace{\text{frontmatter.related}}_{\text{建議}} \cup \underbrace{\text{[[wikilinks]]}}_{\text{選用}} \cup \underbrace{\text{dir\_context}}_{\text{補充（|\text{Files}|<5 時）}},\quad |\text{Files}| \leq 20$$

## Step 4: PromptGen

$$\text{Prompt} = \text{Purpose} + \text{Audience} + \text{Format}(\text{scope}) + \text{Language} + \text{KeySections}(\text{H2}) + \text{Constraints}$$

$$\text{Format}(\text{scope}) = \begin{cases}
\text{N slides, section headers, 3–5 bullets/slide} & \text{briefing} \\
\text{structured document with TOC, H2 per section} & \text{report} \\
\text{N Q\&A pairs, question first, concise answer} & \text{faq} \\
\text{conversational script, two hosts, natural dialogue} & \text{podcast} \\
\leq 400\text{ words, bullet points, key metrics first} & \text{summary}
\end{cases}$$

## Step 5: Write

```markdown
---
note_type: notebooklm-prompt
source: {source_filepath}
scope: {scope}
sources_dir: resources/{stem}/
created: {今天 ISO 8601 +08:00}
modified: {今天 ISO 8601 +08:00}
---

# {scope} Prompt：{H1 title}

## 💬 Generation Prompt

> 複製以下 Prompt，貼入 NotebookLM 的 Chat 欄位

{crafted prompt}
```

## Step 6: SourcesCollect

$$\text{resources/\{stem\}/note-to-notebooklm/} = \text{reset} \to \text{copy}(P \in \text{Files} \mid P \exists)$$

- 重建 `resources/{stem}/note-to-notebooklm/`（先清空再複製，確保每次同步最新）
- 僅複製實際存在的檔案，缺失的 skip 並提示

## Step 7: Confirm

```
✅ NotebookLM package ready

Prompt:  references/{stem}/note-to-notebooklm/{scope}.prompt.md
Sources: resources/{stem}/note-to-notebooklm/  ({N} files)

→ 打開 resources/{stem}/note-to-notebooklm/ 拖入 NotebookLM，貼上 Prompt 生成
```
