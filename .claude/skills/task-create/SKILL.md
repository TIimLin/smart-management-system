---
name: task-create
description: >
  Create a new task workspace under .ai-core/tasks/{task-name}/.
  Scaffolds TASKLIST.json, TASK.md, agents/ and references/ directories.
  Trigger when user says "建立任務", "新增 task", "開始新任務", "create task",
  or when starting a Formula-Contract automation workflow.
argument-hint: "[task-name]"
---

# Task Create

$$\text{TaskCreate} = \text{NameResolve} \to \text{ConflictCheck} \to \text{DirScaffold} \to \text{FileInit} \to \text{Confirm}$$

## Step 1: NameResolve

$$\text{Name} = \text{args}[0] \mid \text{Ask}$$

$$\text{format}: \text{kebab-case},\; \leq 40 \text{ 字元}$$

## Step 2: ConflictCheck

$$(\texttt{.ai-core/tasks/\{name\}/} \text{ 已存在}) \to \text{警告} + \text{詢問：繼續或取消？}$$

## Step 3: DirScaffold

```bash
mkdir -p ".ai-core/tasks/{name}/agents"
mkdir -p ".ai-core/tasks/{name}/references"
```

## Step 4: FileInit（並行）

**TASKLIST.json**：
```json
{
  "tasks": [],
  "current_index": 0,
  "total_count": 0,
  "task_name": "{name}",
  "created": "{today}",
  "status": "pending"
}
```

**TASK.md**（formula 形式）：
```markdown
---
created: {today}
modified: {today}
task_name: {name}
status: pending
---

# {Name}

$$\text{Task} = \text{BusinessIncrement} \to \text{PlanningAgent} \to \text{ExecutionAgent} \to \text{Delivery}$$

## 業務增量描述

{待填寫}

## 目標

{待填寫}
```

## Step 5: Confirm

```
✅ Task created

Path:      .ai-core/tasks/{name}/
Files:     TASKLIST.json + TASK.md
Dirs:      agents/ + references/

→ 編輯 TASK.md 填入業務描述
→ 使用 agent-role-planning 開始規劃
```
