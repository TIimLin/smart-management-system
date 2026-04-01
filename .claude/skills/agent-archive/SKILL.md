---
name: agent-archive
description: >
  Archive an agent from .ai-core/tasks/{task}/agents/ by moving its .md and .log
  to agents/archived/. User-only trigger: "封存 agent", "archive agent",
  "這個 agent 不需要了", "移除 agent", "agent 結束了".
  Never auto-trigger — destructive operation.
argument-hint: [task-name] [agent-name]
disable-model-invocation: true
---

# Agent Archive

$$\text{AgentArchive}(\text{task}, \text{name}) = \text{Locate} \to \text{StatusCheck} \to \text{Confirm}(\text{user}) \to \text{Move} \to \text{Done}$$

## Step 1: Locate

$$\text{AgentDir} = \texttt{.ai-core/tasks/\{task\}/agents/}$$

$$\text{Target} = \texttt{agents/\{name\}.\{md, log\}}$$

$$\sim(\text{Target 存在}) \to \text{錯誤：agent 不存在，用 agent-read 確認現有 agents}$$

$$(\text{已在 agents/archived/}) \to \text{提示：此 agent 已封存}$$

## Step 2: StatusCheck

$$\text{顯示 frontmatter.status + 最後修改時間供使用者確認}$$

## Step 3: Confirm

```
⚠️  封存 Agent：{name}
Task:    {task-name}
Status:  {frontmatter.status}
Files:   agents/{name}.md + agents/{name}.log
→ 目標：agents/archived/{name}.{md,log}
此操作不可逆（移動，非刪除）。確認封存？(y/N)
```

$$(\text{user} = N \mid \text{未回應}) \to \text{取消，不執行}$$

## Step 4: Move

```bash
mkdir -p ".ai-core/tasks/{task}/agents/archived"
mv ".ai-core/tasks/{task}/agents/{name}.md"  ".ai-core/tasks/{task}/agents/archived/{name}.md"
mv ".ai-core/tasks/{task}/agents/{name}.log" ".ai-core/tasks/{task}/agents/archived/{name}.log"
```

## Step 5: Done

```
✅ Agent archived: {name}

From: agents/{name}.{md,log}
To:   agents/archived/{name}.{md,log}
```
