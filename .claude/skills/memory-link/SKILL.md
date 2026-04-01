---
name: memory-link
description: >
  Build bidirectional links for a memory entry: memory↔note or memory↔memory.
  Note must exist first as the knowledge foundation for full context.
  Auto-trigger after memory-create when related notes or memories exist.
  Trigger when user says "連結到筆記", "記憶之間連結", "這個記憶和XX有關".
argument-hint: [memory-filepath] [note-or-memory-filepath...]
---

# Memory Link

$$\text{MemoryLink} = \text{SourceResolve} \to \text{TargetResolve} \to \text{TypeCheck} \to \text{BiLinkAll} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{Source} \in \texttt{.ai-core/memory/**/*.md}$$

$$\text{Source} = \text{args}[0] \mid \text{memory-read}(\text{keyword}) \mid \text{Ask}$$

## Step 2: TargetResolve

$$\text{Targets} = \text{args}[1..] \mid \text{AutoDiscover} \mid \text{Ask}$$

$$\text{AutoDiscover}: \text{GrepKeywords}(\text{source.tags} + \text{source.title}) \to \texttt{.ai-core/notes/} \;\&\; \texttt{.ai-core/memory/}$$

排除：`archived/`、`source` 本身、已在 `related:` 中的。

## Step 3: TypeCheck

$$\text{LinkType}(T) = \begin{cases} \text{memory} \leftrightarrow \text{note} & T \in \texttt{.ai-core/notes/} \\ \text{memory} \leftrightarrow \text{memory} & T \in \texttt{.ai-core/memory/} \end{cases}$$

**前置條件**：`memory↔note` 連結要求 note 必須已存在（先用 note-create 建立）。

## Step 4: BiLinkAll

$$\text{BiLink}(M, T) = \text{FmUpdate}(M,\; \text{related} \mathrel{+}= [[T]]) \times \text{FmUpdate}(T,\; \text{related} \mathrel{+}= [[M]])$$

$$\text{BiLinkAll} = \prod_{T \in \text{Targets}} \text{BiLink}(\text{Source}, T)$$

## Step 5: Confirm

```
✅ Memory links created

Source: {memory_path}
Linked ({N}):
  → {target_1}  [{note | memory}]
  → {target_2}  [{note | memory}]
```
