---
name: task-read
description: >
  Read and display task status, current increment, agent formula outputs and
  execution logs from .ai-core/tasks/{task-name}/. Aggregates TASKLIST.json +
  TASK.md + agents/*.md + agents/*.log into a unified dashboard. Auto-trigger
  when user asks "任務狀態", "任務進度", "當前增量", "task status", "看一下任務",
  "planning 寫了什麼", "execution 跑到哪", "agent 有沒有跑完",
  or when supervisor needs to validate current task state before proceeding.
argument-hint: [task-name]
---

# Task Read

$$\text{TaskRead} = \text{Locate} \to \text{Aggregate}(\text{TASKLIST.json} + \text{TASK.md} + \text{agents/*.md} + \text{agents/*.log}) \to \text{Dashboard}$$

## Step 1: Locate

$$\text{TaskDir} = \texttt{.ai-core/tasks/\{task-name\}/}$$

$$(\text{args}[0] \text{ 存在}) \to \text{直接使用}$$

$$\sim(\text{args}[0]) \to \text{列出} \texttt{.ai-core/tasks/*/} \text{供選擇（排除 archived/）}$$

## Step 2: Aggregate（並行讀取）

$$\text{Progress} = \text{TASKLIST.json} \to \text{current\_index} / \text{total\_count} + \text{status}$$

$$\text{CurrentTask} = \text{TASKLIST.json}[\text{tasks}][\text{current\_index}]$$

$$\text{Description} = \text{TASK.md}(\text{業務描述} + \text{目標段落})$$

$$\text{AgentFormula} = \text{agents/*.md} \to \text{frontmatter.status} + \text{前 100 字（判斷輸出是否完整）}$$

$$\text{AgentLog} = \text{agents/*.log} \to \text{tail -5（判斷執行狀態：完成/中斷/錯誤）}$$

**為何兩者都需要**：

$$\text{*.md} = \text{公式輸出}(\text{結果}),\quad \text{*.log} = \text{執行軌跡}(\text{過程})$$

$$(\text{中斷情況}): \text{*.md 可能是半成品} \to \text{*.log 末行揭示中斷位置}$$

$$(\text{錯誤情況}): \text{*.md 可能為空} \to \text{*.log 末行揭示錯誤原因}$$

## Step 3: Dashboard

```
📋 Task: {task-name}
Status:  {status}  │  Progress: {current_index + 1}/{total_count}

Current Increment:
  {tasks[current_index]}

Agents:
  planning.md   [completed]  → WorkflowFormula = DataCollection → ...
  planning.log               → [2026-03-02T22:52] Stage 3/3 done. Output written.

  execution.md  [in_progress] → Step 1/4: Scaffold task dir ...（中斷）
  execution.log               → [2026-03-02T23:01] Error: cannot find TASK.md

Files: TASKLIST.json · TASK.md · agents/{N} files
```

$$(\text{*.log 不存在}) \to \text{顯示「log 未建立，agent 可能尚未執行」}$$

$$(\text{無 agents}) \to \text{提示：使用 agent-create 建立規劃者或執行者}$$
