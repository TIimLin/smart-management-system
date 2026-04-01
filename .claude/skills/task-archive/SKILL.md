---
name: task-archive
description: >
  Archive a completed task from .ai-core/tasks/{task-name}/ to
  .ai-core/tasks/archived/yyMMdd/{task-name}/. Destructive, always confirm
  before moving. Trigger on "封存任務", "完成任務", "archive task",
  "任務結束", "收尾任務", "task done".
argument-hint: "[task-name]"
disable-model-invocation: true
---

# Task Archive

$$\text{TaskArchive} = \text{Locate} \to \text{StatusCheck} \to \text{Confirm}(\text{user}) \to \text{Move} \to \text{Done}$$

## Step 1: Locate

$$\text{TaskDir} = \texttt{.ai-core/tasks/\{task-name\}/}$$

$$\sim(\text{TaskDir 存在}) \to \text{錯誤：找不到任務}$$

## Step 2: StatusCheck

$$\text{執行 task-read 顯示任務摘要}$$

$$(\text{status} \neq \texttt{completed}) \to \text{警告：任務尚未完成，確認仍要封存？}$$

## Step 3: Confirm

```
⚠️  封存任務：{task-name}

Status:   {status}
Progress: {current_index}/{total_count}
Agents:   {agent count} 個

目標路徑：.ai-core/tasks/archived/{yyMMdd}/{task-name}/
此操作不可逆（檔案移動，非刪除）。確認封存？(y/N)
```

$$(\text{user} = N \mid \text{未回應}) \to \text{取消，不執行}$$

## Step 4: Move

```bash
mkdir -p ".ai-core/tasks/archived/{yyMMdd}"
mv ".ai-core/tasks/{task-name}" ".ai-core/tasks/archived/{yyMMdd}/{task-name}"
```

## Step 5: Done

```
✅ Task archived: {task-name}
→ .ai-core/tasks/archived/{yyMMdd}/{task-name}/
```
