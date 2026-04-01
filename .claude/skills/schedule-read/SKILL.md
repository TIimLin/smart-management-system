---
name: schedule-read
description: >
  Read and display a schedule period's task list and progress from
  .ai-core/schedule/{period}/TASKLIST.json with visual progress bar.
  Trigger when user says "看排程", "時程進度", "sprint 狀態", "schedule-read",
  "排程跑到哪", or when checking project timeline.
argument-hint: "[period-name]"
user-invocable: true
layer: 2
type: crud
---

# Schedule Read

$$\text{ScheduleRead} = \text{Locate} \to \text{Read} \to \text{Dashboard}$$

## Step 1: Locate

$$(\text{args}[0]) \to \texttt{.ai-core/schedule/\{period\}/TASKLIST.json}$$

$$\sim(\text{args}[0]) \to \text{列出 .ai-core/schedule/*/ 供選擇（排除 archived/）}$$

$$\sim(\text{TASKLIST.json}) \to \text{錯誤：排程不存在，用 schedule-create 建立}$$

## Step 2: Read

$$\text{Data} = \{period,\; tasks[],\; current\_index,\; total\_count,\; status,\; created\}$$

## Step 3: Dashboard

```
📅 Schedule: {period}  [{status}]  Created: {created}
Progress: {current_index}/{total_count}  ████████░░ {pct}%

Tasks:
  ✅  1. {task 1}
  ▶   2. {task 2}  ← current
  ⬜  3. {task 3}

→ schedule-update advance  推進到下一個任務
```
