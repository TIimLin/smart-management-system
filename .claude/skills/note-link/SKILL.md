---
name: note-link
description: >
  Build bidirectional links between notes in .ai-core/notes/. Two modes:
  (1) auto-discover: given one note, search ALL related notes and link them all.
  (2) explicit: link a specified set of notes together.
  Trigger when user says "找相關筆記並連結", "幫我建立連結", "自動連結",
  "link this note", or after writing a note to build the knowledge graph.
argument-hint: [filepath] [related-filepath...]
---

# Note Link

$$\text{NoteLink} = \text{ModeDetect} \to \text{SourceResolve} \to \text{RelatedFind?} \to \text{CandidateConfirm} \to \text{BiLinkAll} \to \text{Confirm}$$

## Step 1: ModeDetect

$$\text{Mode} = \begin{cases} \text{auto-discover} & \text{args} = [\text{single path}] \text{ 或 無 args} \\ \text{explicit} & \text{args} = [\text{path}_1, \text{path}_2, \ldots] \end{cases}$$

## Step 2: SourceResolve

$$\text{Source} = \text{args}[0] \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

## Step 3: RelatedFind（auto-discover mode）

$$\text{Candidates} = \text{GrepTags}(\text{source.tags}) \;\&\; \text{GrepKeywords}(\text{source.title}) \;\&\; \text{GrepContent}(\text{source.keywords})$$

範圍：`.ai-core/notes/**/*.md`，排除 `archived/`、`source` 本身、已在 `related:` 中的。

$$\text{Rank} = \text{tag overlap count} > \text{title keyword match} > \text{content match}$$

## Step 4: CandidateConfirm

展示候選清單，讓使用者確認（可多選、可全選）：

```
Found {N} related notes for: {source}

1. [✓] {path_1}  tags: {matching_tags}
2. [✓] {path_2}  tags: {matching_tags}
3. [ ] {path_3}  content match only

Link all? (Y) / Select (1,2...) / Cancel (n)
```

## Step 5: BiLinkAll

$$\text{BiLink}(A, B) = \text{FmUpdate}(A,\; \text{related} \mathrel{+}= [[B]]) \times \text{FmUpdate}(B,\; \text{related} \mathrel{+}= [[A]])$$

$$\text{BiLinkAll}(\text{Source}, \text{Targets}) = \prod_{T \in \text{Targets}} \text{BiLink}(\text{Source}, T)$$

使用 `Edit` 工具依序更新每個筆記的 frontmatter `related:` 欄位。

## Step 6: Confirm

```
✅ Note links created

Source: {source_path}
Linked ({N} notes):
  → {target_1}
  → {target_2}
  ...
```
