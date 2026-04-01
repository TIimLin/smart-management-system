---
name: memory-archive
description: >
  Archive a memory entry by moving it to .ai-core/memory/archived/yyMMdd/.
  Removes the entry from MEMORY.json index.
  User-only trigger: "封存記憶", "archive memory", "這個記憶不用了".
argument-hint: [filepath | topic-keyword]
disable-model-invocation: true
---

# Memory Archive

$$\text{MemoryArchive} = \text{TargetResolve} \to \text{UserConfirm} \to \text{ArchiveMove} \to \text{IndexRemove} \to \text{Confirm}$$

## Step 1: TargetResolve

$$\text{Target} = \text{args} \mid \text{memory-read}(\text{keyword}) \mid \text{Ask}$$

## Step 2: UserConfirm

```
⚠️  即將封存：{filepath}
確認？(y/N)
```

## Step 3: ArchiveMove

$$\text{ArchiveDir} = \texttt{.ai-core/memory/archived/\{yyMMdd\}/}$$

```bash
mkdir -p ".ai-core/memory/archived/{yyMMdd}/"
mv "{filepath}" ".ai-core/memory/archived/{yyMMdd}/{filename}"
```

## Step 4: IndexRemove

$$\text{Read}(\texttt{.ai-core/memory/MEMORY.json}) \to \text{remove entry where file = target} \to \text{total} -= 1 \to \text{update updated} \to \text{Write}(\texttt{.ai-core/memory/MEMORY.json})$$

## Step 5: Confirm

```
✅ Memory archived

From:     {original_path}
To:       .ai-core/memory/archived/{yyMMdd}/{filename}
MEMORY.json 已移除該條目
```
