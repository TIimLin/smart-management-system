---
name: note-archive
description: >
  Archive a note or domain by moving it to .ai-core/notes/archived/yyMMdd/.
  User-only trigger: "封存筆記", "archive note", "這個不用了", "移到封存".
  Never auto-trigger — requires explicit user action.
argument-hint: [filepath | keyword]
disable-model-invocation: true
---

# Note Archive

$$\text{NoteArchive} = \text{TargetResolve} \to \text{UserConfirm} \to \text{ArchiveMove} \to \text{Confirm}$$

## Step 1: TargetResolve

$$\text{Target} = \text{args} \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

## Step 2: UserConfirm

```
⚠️  即將封存：{filepath}
確認？(y/N)
```

## Step 3: ArchiveMove

$$\text{ArchiveDir} = \texttt{.ai-core/notes/archived/\{yyMMdd\}/}$$

$$\sim(\text{dir 存在}) \to \texttt{mkdir -p .ai-core/notes/archived/\{yyMMdd\}/}$$

```bash
mv "{filepath}" ".ai-core/notes/archived/{yyMMdd}/{filename}"
```

## Step 4: Confirm

```
✅ Note archived

From: {original_path}
To:   .ai-core/notes/archived/{yyMMdd}/{filename}
```
