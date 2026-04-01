---
name: workflow-sort
description: >
  List and display all workflows in a task grouped by type and status,
  with complexity (assigned agent count) as secondary sort key.
  User-only: "列出 workflow", "workflow 清單", "workflow-sort",
  "show workflows", "有哪些 workflow", "workflow 狀態概覽",
  "workflow 有幾個", "整理 workflow".
  Never auto-trigger — pure display, no gate check function.
argument-hint: "[task-name]"
disable-model-invocation: true
---

# Workflow Sort

$$\text{WorkflowSort}(\text{task}) = \text{Locate} \to \text{Enumerate} \to \text{Group} \to \text{StatusSort} \to \text{Display}$$

## Step 1: Locate

$$\text{WorkflowDir} = \texttt{.ai-core/tasks/\{task\}/workflows/}$$

$$\sim(\text{WorkflowDir 存在}) \vee (\texttt{workflows/*.md} = \emptyset) \to \text{提示：尚無 workflows，用 workflow-create 建立}$$

## Step 2: Enumerate

$$\text{Active} = \text{Glob}(\texttt{workflows/*.md}) \setminus \texttt{workflows/archived/*.md}$$

$$\text{Archived} = \text{Glob}(\texttt{workflows/archived/*.md})$$

$$\text{Complexity}(w) = |\text{w.frontmatter.agents}|$$

## Step 3: Group

$$\text{GroupOrder}: \text{multi-agent} \to \text{solo} \to \text{已封存}$$

$$\text{Group}(w) = \text{w.frontmatter.type}$$

## Step 4: StatusSort

$$\text{同 Group 內}: \text{in\_progress} \to \text{pending} \to \text{completed}$$

$$\text{同狀態內}: \text{Complexity}(w)\downarrow \text{（複雜度高者優先展示）}$$

## Step 5: Display

```
Task: {task-name}
Active: {N} workflows  │  Archived: {M} workflows
──────────────────────────────────────────────────
[multi-agent]  （跨 agent 協作調度）
  🔄 pipeline          in_progress  agents: 3  (planning→sese→execution)
  ⬜ research-flow     pending      agents: 2  (3w→mece)

[solo]  （單 agent 執行協議）
  ✅ exec-protocol     completed    agents: 1  (execution)
  ⬜ plan-context      pending      agents: 0  —

[已封存]  {M} 個
──────────────────────────────────────────────────
Dependencies:
  pipeline precedes deploy-workflow
  research-flow composes analysis-sub
```

圖示對照：`✅ completed`  `🔄 in_progress`  `⬜ pending`  `📦 archived`
