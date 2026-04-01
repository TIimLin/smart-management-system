---
name: workflow-read
description: >
  Read a workflow definition (.md) and execution log (.log) from
  .ai-core/tasks/{task}/workflows/. Shows assigned agents and their statuses.
  Auto-trigger on "workflow 內容", "看 workflow", "workflow 定義",
  "read workflow", "workflow 協議是什麼", "哪些 agent 在這個 workflow",
  "workflow 執行到哪", "workflow 狀態", "workflow 跑到哪了".
argument-hint: [task-name] [workflow-name]
---

# Workflow Read

$$\text{WorkflowRead}(\text{task}, \text{name}) = \text{Locate} \to \text{Parse} \to \text{AgentStatus} \to \text{Display}$$

## Step 1: Locate

$$\text{WorkflowDir} = \texttt{.ai-core/tasks/\{task\}/workflows/}$$

$$(\text{name 已指定}) \to \text{直接讀取 workflows/\{name\}.\{md, log\}}$$

$$\sim(\text{name}) \to \text{Glob}(\texttt{workflows/*.md}) \to \text{列出供選擇}$$

$$\sim(\texttt{workflows/*.md}) \to \text{提示：尚無 workflows，用 workflow-create 建立}$$

## Step 2: Parse

$$\text{Protocol} = \text{Read}(\texttt{workflows/\{name\}.md})$$

$$\text{RecentLog} = \text{Read}(\texttt{workflows/\{name\}.log})(\text{最後 20 行})$$

## Step 3: AgentStatus

$$\text{AssignedAgents} = \text{frontmatter.agents}$$

$$\forall a \in \text{AssignedAgents} \to \text{Read}(\texttt{agents/\{a\}.md}).\text{frontmatter.status}$$

## Step 4: Display

```
📋 Workflow: {name}  │  Task: {task-name}
Type:    {type}      │  Status: {status}
Created: {created}   │  Agents: {N}
─────────────────────────────────────────
Protocol:
{workflows/{name}.md 完整內容}

─────────────────────────────────────────
Assigned Agents:
  ✅ {agent1}: completed    🔄 {agent2}: in_progress   ...
  （尚無指派 agents）

Recent Log (last 20 lines):
{workflows/{name}.log tail-20}
```
