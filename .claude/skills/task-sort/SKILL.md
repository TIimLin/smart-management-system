---
name: task-sort
description: >
  List and sort all tasks under .ai-core/tasks/ with status, progress, and
  dependency overview. Shows which tasks are ready (unblocked) vs blocked.
  Trigger when user says "任務排序", "列出所有任務", "哪些任務可以開始",
  "task list", "task-sort", "task 有哪些", "看一下所有任務".
argument-hint: [sort-by: status|deps|date]
user-invocable: true
layer: 2
type: crud
---

# Task Sort

$$\text{TaskSort} = \text{ListAll} \to \text{ReadMeta} \to \text{Classify} \to \text{Display}$$

## Step 1: ListAll

$$\text{Tasks} = \{d \mid d \in \texttt{.ai-core/tasks/*/},\; d \neq \texttt{archived/}\}$$

## Step 2: ReadMeta（並行）

$$\forall t: \text{Meta}(t) = \text{TASKLIST.json} \to \{status,\; blocks,\; blockedBy,\; current\_index,\; total\_count,\; created\}$$

## Step 3: Classify

$$\text{ReadyToStart}(t) = (t.status = \text{pending}) \land (t.blockedBy = \emptyset \lor \forall b: b.status = \text{completed})$$

$$\text{sort-by} = \begin{cases} \text{status} & \text{in\_progress → pending-ready → pending-blocked → completed（預設）} \\ \text{deps} & \text{拓撲排序，無依賴優先} \\ \text{date} & \text{created 升冪} \end{cases}$$

## Step 4: Display

```
📋 Tasks Overview  ({N} tasks)

🔄 In Progress (N)
  ▸ {task}  [{current}/{total}]  {tasks[current]}

⏳ Pending – Ready (N)
  ▸ {task}  [{total} increments]

🚫 Pending – Blocked (N)
  ▸ {task}  ← waiting: {blockedBy[]}

✅ Completed (N)
  ▸ {task}
```
