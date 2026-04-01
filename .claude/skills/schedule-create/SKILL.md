---
name: schedule-create
description: >
  Create a new schedule period under .ai-core/schedule/{period}/ with TASKLIST.json and TASK.md.
  Dynamically scans all existing docs/ subdirectories for project context to
  generate task breakdown. Trigger when user says "建立排程", "規劃時程",
  "新增 sprint", "create schedule", "規劃 {period}", "開始排程規劃".
argument-hint: "[period-name: e.g. 1week, 1month, mvp-phase1]"
user-invocable: true
layer: 2
type: crud
disable-model-invocation: false
---

# Schedule Create

$$\text{ScheduleCreate} = \text{PeriodResolve} \to \text{ConflictCheck} \to \text{DocsRead} \to \text{TaskGen} \to \text{Scaffold} \to \text{Confirm}$$

## Step 1: PeriodResolve

$$\text{Period} = \text{args}[0] \mid \text{Ask}, \quad \text{format: kebab-case 完全自定義}$$

## Step 2: ConflictCheck

$$(\texttt{.ai-core/schedule/\{period\}/} \text{ 已存在}) \to \text{警告 + 詢問}$$

## Step 3: DocsRead（動態掃描，並行）

$$\text{Context} = \{d \mid d \in \texttt{docs/*/},\; d \text{ 存在}\}$$

$$\sim(\texttt{docs/} \text{ 存在}) \to \text{錯誤：docs/ 不存在，無法生成排程}$$

## Step 4: TaskGen（AI 生成）

$$\text{Tasks} = \text{LLM}(\text{Context},\; \text{Period}) \to \{tasks[],\; total\_count\}$$

$$\text{TaskConstraint} = \{len \in [20, 60]\text{字},\; \text{foundation} \prec \text{feature},\; \text{atomic} \times \text{period-completable}\}$$

## Step 5: Scaffold

$$\texttt{TASKLIST.json} = \{tasks:[],\; current\_index:0,\; total\_count:N,\; period,\; created:\text{ISO},\; status:\text{active}\}$$

$$\texttt{TASK.md} = \text{Expand}(tasks[0])$$

## Step 6: Confirm

```
✅ Schedule created
Period: {period}  Path: .ai-core/schedule/{period}/  Tasks: {N}
→ schedule-read 查看 · schedule-update 推進
```
