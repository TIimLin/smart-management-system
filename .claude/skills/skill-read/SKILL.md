---
name: skill-read
description: >
  Read and display skill details or list all skills sorted by Layer 0-5.
  Mode detail: show full SKILL.md of a specific skill.
  Mode list: dynamic scan of all active skills by layer with trigger summary.
  Trigger when user says "看 skill", "列出所有 skill", "skill-read",
  "有哪些 skill", "這個 skill 怎麼用".
argument-hint: "[skill-name | --list] [--layer=0-5] [--type=crud|role|conversion|contract|tool]"
user-invocable: true
layer: 4
type: crud
---

# Skill Read

$$\text{SkillRead} = \text{ModeDetect} \to \text{Read} \to \text{Display}$$

## Step 1: ModeDetect

$$\text{Mode} = \begin{cases} \text{detail} & \text{args}[0] \text{ 為 skill 名稱} \\ \text{list} & \text{--list 旗標或無 args} \end{cases}$$

## Step 2: Read

$$\text{detail}: \text{Read}(\texttt{.claude/skills/\{name\}/SKILL.md}) + \text{Glob}(\texttt{references/}) + \text{Glob}(\texttt{scripts/})$$

$$\text{list}: \text{Glob}(\texttt{.claude/skills/*/SKILL.md},\; \overline{\texttt{archived/}}) \to \text{Parse}(frontmatter:\; name,\; layer,\; type)$$

$$\text{list} \Rightarrow \text{動態掃描},\quad \sim\text{寫死 skill 名稱}$$

## Step 3: Display

$$\text{detail}: \text{Output}(SKILL.md) + \text{Exists}(\texttt{references/}) \to \text{List} + \text{Exists}(\texttt{scripts/}) \to \text{List}$$

$$\text{list}: \text{Group}_{layer \in [0,5]}(\text{skills}) \to \text{FromFrontmatter}$$

```
🛠 Skills  ({N} active · {M} archived)

Layer 0 — Constitutional Contracts
  {name}  [auto]  {description 摘要}

Layer 1 — Knowledge
  ...

Layer 2 — Planning
  ...

Layer 3 — Orchestration
  ...

Layer 4 — Meta-management
  ...

Layer 5 — Single-purpose Tools
  ...

Archived: {M} → .claude/skills/archived/
```
