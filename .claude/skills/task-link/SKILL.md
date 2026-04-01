---
name: task-link
description: >
  Establish dependency between two tasks in .ai-core/tasks/.
  Updates TASKLIST.json with blocks/blockedBy fields and injects [[雙向連結]]
  (Obsidian wikilink syntax: [[filename]]) into both TASK.md files for navigation.
  Trigger when user says "任務依賴", "A 要等 B 完成才能做", "task A depends on B",
  "link tasks", "task-link", "建立任務關聯".
argument-hint: [source-task] [target-task] [direction: blocks|depends-on]
user-invocable: true
layer: 2
type: crud
---

# Task Link

$$\text{TaskLink}(A, B) = \text{Locate} \to \text{DirectionResolve} \to \text{CycleCheck} \to \text{UpdateJson} \to \text{InjectLinks} \to \text{Confirm}$$

## Step 1: Locate

$$\text{A} = \texttt{.ai-core/tasks/\{source\}/TASKLIST.json}, \quad \text{B} = \texttt{.ai-core/tasks/\{target\}/TASKLIST.json}$$

$$\sim(\text{A 或 B 存在}) \to \text{錯誤：找不到任務，用 task-read 確認}$$

## Step 2: DirectionResolve

$$\text{direction} = \begin{cases} \text{A blocks B} & \text{"A 完成才能做 B" / "blocks"} \\ \text{A depends-on B} & \text{"A 等 B"（等同 B blocks A）} \end{cases}$$

$$\sim(\text{direction}) \to \text{詢問：A 完成後才能做 B？還是 A 要等 B 先完成？}$$

## Step 3: CycleCheck

$$\text{Cycle}(A \to B) = \exists\; \text{path}: B \xrightarrow{blocks^*} A \quad \text{（BFS/DFS 遞迴遍歷 blocks 鏈）}$$

$$\text{Cycle} = \text{True} \to \text{錯誤：循環依賴，無法建立}$$

## Step 4: UpdateJson（雙向）

$$\text{A.blocks} \mathrel{+}= [B], \quad \text{B.blockedBy} \mathrel{+}= [A]$$

## Step 5: InjectLinks（雙向）

$$\text{A.TASK.md} \mathrel{+}= \texttt{→ blocks: [[B/TASK.md]]}, \quad \text{B.TASK.md} \mathrel{+}= \texttt{← blockedBy: [[A/TASK.md]]}$$

## Step 6: Confirm

```
✅ Task link established
A: {source}  →blocks→  B: {target}
TASKLIST.json: A.blocks += [B] · B.blockedBy += [A]
TASK.md:       [[雙向連結]] injected（Obsidian wikilink syntax）
```
