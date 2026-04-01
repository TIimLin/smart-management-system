---
name: schedule-update
description: >
  Update progress or content in .ai-core/schedule/{period}/TASKLIST.json.
  Mode advance: mark current done, move to next, update TASK.md.
  Mode content: edit task descriptions or reorder.
  Trigger when user says "推進排程", "完成這個任務", "schedule 下一步",
  "排程寫錯了", "修改排程任務".
argument-hint: [period-name] [mode: advance|content]
user-invocable: true
layer: 2
type: crud
disable-model-invocation: false
---

# Schedule Update

$$\text{ScheduleUpdate} = \text{Locate} \to \text{ModeSelect} \to \text{Apply}(\Delta) \to \text{Confirm}$$

## Step 1: Locate

$$\sim(\texttt{.ai-core/schedule/\{period\}/} \text{ 存在}) \to \text{錯誤，建議 schedule-read 列出}$$

## Step 2: ModeSelect

$$\text{Mode} = \begin{cases} \text{advance} & \text{current\_index++} \\ \text{content} & \text{修改 tasks[] 內容} \end{cases}$$

$$\sim(\text{mode}) \to \text{先 schedule-read，再詢問}$$

## Step 3: Apply

$$\text{IsLast}(t) = (current\_index = total\_count - 1)$$

$$\text{advance}(t) = \begin{cases}
\text{IsLast} & \to status = \text{completed},\; \texttt{TASK.md} = \text{"✅ 全部完成"},\; \text{提示可 schedule-archive} \\
\neg\text{IsLast} & \to current\_index \mathrel{+}= 1,\; \texttt{TASK.md} = tasks[current\_index]
\end{cases}$$

$$\text{content}: \Delta\text{tasks}[] = \text{user 指定修改}$$

## Step 4: Confirm

```
✅ Schedule updated: {period}
Mode: {advance|content}  Progress: {new}/{total}  [{status}]
Current: {tasks[current_index] | "✅ 全部完成"}
```
