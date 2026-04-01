---
name: schedule-archive
description: >
  Archive a schedule period from .ai-core/schedule/{period}/ to
  .ai-core/schedule/archived/yyMMdd/{period}/. User-only trigger.
  Trigger when user says "封存排程", "archive schedule", "這個 sprint 結束了".
  Never auto-trigger.
argument-hint: "[period-name]"
user-invocable: true
layer: 2
type: crud
disable-model-invocation: true
---

# Schedule Archive

$$\text{ScheduleArchive} = \text{Locate} \to \text{StatusCheck} \to \text{Confirm}(\text{user}) \to \text{Move} \to \text{Done}$$

## Step 1: Locate

$$\text{SourceDir} = \texttt{.ai-core/schedule/\{period\}/}$$

$$\sim(\text{SourceDir}) \to \text{錯誤：排程不存在}$$

## Step 2: StatusCheck

$$(\text{status} \neq \text{completed}) \to \text{警告：排程尚未完成，確認仍要封存？}$$

## Step 3: Confirm（user 明確確認後才執行）

```
⚠️  封存排程：{period}
Status: {status}  Task: 第 {current_index+1}/{total_count} 個（正在執行第幾個，共幾個）
→ 目標：.ai-core/schedule/archived/{yyMMdd}/{period}/
此操作不可逆（移動，非刪除）。確認封存？(y/N)
```

## Step 4: Move

```bash
mkdir -p .ai-core/schedule/archived/{yyMMdd}
mv .ai-core/schedule/{period} .ai-core/schedule/archived/{yyMMdd}/{period}
```

## Step 5: Done

```
✅ Schedule archived: {period}
→ .ai-core/schedule/archived/{yyMMdd}/{period}/
```
