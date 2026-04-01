---
name: skill-create
description: >
  Create a new skill directory scaffold under .claude/skills/{skill-name}/.
  Generates SKILL.md template by type (crud|role|conversion|contract|tool) with
  references/ and scripts/ directories. Validates entity CRUD completeness.
  Trigger when user says "建立新 skill", "新增 skill", "create skill",
  "skill-create", "我要做一個 skill".
argument-hint: [skill-name] [type: crud|role|conversion|contract|tool]
user-invocable: true
layer: 4
type: crud
disable-model-invocation: false
---

# Skill Create

$$\text{SkillCreate} = \text{EntityCheck} \to \text{NameResolve} \to \text{TypeSelect} \to \text{ConflictCheck} \to \text{Scaffold} \to \text{TemplateGen} \to \text{Confirm}$$

## Step 0: EntityCheck（僅 crud 型，Layer 1–4 實體操作）

$$\text{Missing} = \{create, read, update, archive, link, sort\} \setminus \{op \mid \texttt{.claude/skills/\{entity\}-\{op\}/} \exists\}$$

$$(\text{Missing} \neq \emptyset) \to \text{提示：建議完整設計 6 個原子 skills}$$

> conversion / tool / role / contract 型不適用（無實體 CRUD 語義）。

## Step 1: NameResolve

$$\text{Name} = \text{args}[0] \mid \text{Ask}$$

## Step 2: TypeSelect

$$\text{Type} \in \{crud,\; role,\; conversion,\; contract,\; tool\}$$

## Step 3: ConflictCheck

$$(\texttt{.claude/skills/\{name\}/} \exists) \to \text{警告 + 詢問}$$

## Step 4: Scaffold

只建立根目錄，子目錄按需延遲建立：

```bash
mkdir -p ".claude/skills/{name}"
```

$$\text{references/} = \text{有 formula 規範文件時才建立（crud/contract/conversion 型通常需要）}$$

$$\text{scripts/} = \text{有可執行腳本時才建立（通常為 crud 型的 archive/move 操作）}$$

## Step 5: TemplateGen

$$\text{crud}: \text{Pipeline Formula} + \text{Steps} + \text{Confirm}$$
$$\text{role}: \text{user-invocable: false} + \text{Mission} + \text{三不可缺}$$
$$\text{contract}: \text{Constitutional Laws} + \delta(\text{Contract})$$
$$\text{conversion}: \text{SourceResolve} \to \text{Gen} \to \text{Write} \to \text{Confirm}$$
$$\text{tool}: \text{目標公式} + \text{Steps}$$

模板骨架 → `references/skill-templates.formula.md`

## Step 6: Confirm

```
✅ Skill scaffolded
Path: .claude/skills/{name}/  Type: {type}
```

**crud 型額外顯示**：

```
Entity CRUD: {entity} has [{existing}], missing [{missing}]
```

```
→ 編輯 SKILL.md · skill-read {name} 驗證
```
