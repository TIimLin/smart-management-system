---
name: task-update
description: >
  Update TASKLIST.json and/or TASK.md under .ai-core/tasks/{task-name}/.
  Two modes: (1) advance - move current_index forward and update status,
  (2) content - edit task description, requirements, or tasks list.
  Auto-trigger on "更新任務", "推進增量", "下一個增量", "update task",
  "advance increment", "標記完成", "更新進度", "任務寫錯了".
argument-hint: [task-name] [mode: advance|content]
disable-model-invocation: false
---

# Task Update

$$\text{TaskUpdate} = \text{Locate} \to \text{ModeSelect} \to \text{Apply}(\Delta) \to \text{Confirm}$$

## Step 1: Locate

$$\text{TaskDir} = \texttt{.ai-core/tasks/\{task-name\}/}$$

$$\sim(\text{TaskDir 存在}) \to \text{錯誤：找不到任務，建議 task-read 列出現有任務}$$

## Step 2: ModeSelect

$$\text{Mode} = \begin{cases} \text{advance} & \text{current\_index++，推進到下一個增量} \\ \text{content} & \text{修改 TASK.md 或 tasks[] 內容} \end{cases}$$

$$\sim(\text{mode 已指定}) \to \text{先執行 task-read 顯示現狀，再詢問：推進增量 or 編輯內容？}$$

## Step 3: Apply

**advance 模式**：

$$\text{TASKLIST.json}: \text{current\_index} \mathrel{+}= 1$$

$$(\text{current\_index} < \text{total\_count}) \to \text{status} = \texttt{in\_progress}$$

$$(\text{current\_index} \geq \text{total\_count}) \to \text{status} = \texttt{completed},\; \text{提示可 task-archive}$$

**content 模式**：

$$\Delta\text{TASK.md} = \text{user 指定的修改範圍與內容}$$

$$\text{TASK.md.frontmatter.modified} = \text{today ISO 8601 +08:00}$$

## Step 4: Confirm

```
✅ Task updated: {task-name}

Mode:     {advance | content}
Progress: {current_index + 1}/{total_count}  [{status}]
Current:  {tasks[current_index] | "✅ 全部完成"}
```
