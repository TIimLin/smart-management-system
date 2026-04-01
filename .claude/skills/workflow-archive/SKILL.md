---
name: workflow-archive
description: >
  Archive a workflow from .ai-core/tasks/{task}/workflows/ by moving its .md and .log
  to workflows/archived/. User-only: "封存 workflow", "archive workflow",
  "這個 workflow 不需要了", "移除 workflow".
  Never auto-trigger — irreversible operation.
argument-hint: [task-name] [workflow-name]
disable-model-invocation: true
---

# Workflow Archive

$$\text{WorkflowArchive}(\text{task}, \text{name}) = \text{Locate} \to \text{AssignmentCheck} \to \text{Confirm}(\text{user}) \to \text{Move} \to \text{Done}$$

## Step 1: Locate

$$\text{Target} = \texttt{.ai-core/tasks/\{task\}/workflows/\{name\}.\{md, log\}}$$

$$\sim(\text{Target 存在}) \to \text{錯誤：workflow 不存在，用 workflow-read 確認}$$

$$(\text{已在 workflows/archived/}) \to \text{提示：此 workflow 已封存}$$

## Step 2: AssignmentCheck

$$\text{AssignedAgents} = \text{frontmatter.agents}$$

$$|\text{AssignedAgents}| > 0 \to \text{⚠️ \{N\} 個 agents 指派至此 workflow（\{names\}），封存不影響 agents，但關聯失效}$$

## Step 3: Confirm

```
⚠️  封存 Workflow：{name}
Task:    {task-name}
Type:    {type}    Status: {status}
Agents:  {agents list | 無}
Files:   workflows/{name}.md + workflows/{name}.log
→ 目標：workflows/archived/{name}.{md,log}
此操作不可逆（移動，非刪除）。確認封存？(y/N)
```

$$(\text{user} = N \mid \text{未回應}) \to \text{取消，不執行}$$

## Step 4: Move

```bash
mkdir -p ".ai-core/tasks/{task}/workflows/archived"
mv ".ai-core/tasks/{task}/workflows/{name}.md"  ".ai-core/tasks/{task}/workflows/archived/{name}.md"
mv ".ai-core/tasks/{task}/workflows/{name}.log" ".ai-core/tasks/{task}/workflows/archived/{name}.log"
```

## Step 5: Done

```
✅ Workflow archived: {name}
From: workflows/{name}.{md,log}
To:   workflows/archived/{name}.{md,log}
```
