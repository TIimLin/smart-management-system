---
name: agent-sort
description: >
  List and display all agents in a task grouped by workflow phase and status,
  with Phase Gate check showing which agents are ready vs blocked by phase dependencies.
  AI may auto-trigger as agent-level pre-execution gate check: before running any agent
  in a Formula-Contract workflow, call agent-sort to verify prerequisite phases are complete.
  Also trigger on "列出 agents", "任務的 agents", "agent 清單", "有哪些 agents",
  "agent 狀態總覽", "agent overview", "show agents", "哪些 agent 跑過了",
  "任務進度", "agent 跑到哪了", "可以執行哪個 agent", "下一步跑哪個 agent",
  "phase 完成了嗎", "planning 好了沒".
argument-hint: [task-name]
---

# Agent Sort

$$\text{AgentSort}(\text{task}) = \text{Locate} \to \text{Enumerate} \to \text{PhaseGroup} \to \text{GateCheck} \to \text{Display}$$

## Step 1: Locate

$$\text{AgentDir} = \texttt{.ai-core/tasks/\{task\}/agents/}$$

$$\sim(\text{task 存在}) \to \text{錯誤：先用 task-create 建立任務}$$

$$\sim(\texttt{agents/*.md}) \to \text{提示：尚無 agents，用 agent-create 建立}$$

## Step 2: Enumerate

$$\text{Active} = \text{Glob}(\texttt{agents/*.md}) \setminus \texttt{agents/archived/*.md}$$

$$\text{Archived} = \text{Glob}(\texttt{agents/archived/*.md})$$

$$\text{PhaseOf}(\text{name}) = \begin{cases} \text{理解層} & \text{name} \in \{3w,\; mece,\; thought\text{-}sphere,\; react\} \\ \text{規劃層} & \text{name} = \text{planning} \\ \text{驗證層} & \text{name} \in \{sese,\; critic\} \\ \text{執行層} & \text{name} = \text{execution} \\ \text{其他} & \sim\text{以上} \end{cases}$$

## Step 3: PhaseGroup

$$\text{排列順序：理解層} \to \text{規劃層} \to \text{驗證層} \to \text{執行層} \to \text{其他} \to \text{已封存}$$

$$\text{同 Phase 內：completed} \to \text{in\_progress} \to \text{pending}$$

## Step 4: GateCheck（Phase Gate）

$$\text{PhaseChain}: \text{理解層} \xrightarrow{1} \text{規劃層} \xrightarrow{2} \begin{cases} \text{驗證層} \\ \text{執行層} \end{cases}$$

$$\text{PriorPhase}(p) = \begin{cases} \emptyset & p = \text{理解層} \lor p = \text{其他} \\ \text{理解層} & p = \text{規劃層} \\ \text{規劃層} & p \in \{\text{驗證層},\; \text{執行層}\} \end{cases}$$

$$\text{PhaseReady}(p) = \text{PriorPhase}(p) = \emptyset \;\lor\; \text{Agents}(\text{PriorPhase}(p)) = \emptyset \;\lor\; \forall a \in \text{Agents}(\text{PriorPhase}(p)):\; a.\text{status} = \text{completed}$$

$$\text{ReadyToRun}(a) = \text{PhaseReady}(\text{PhaseOf}(a))$$

$$\text{GateSummary} = \bigoplus_{p \in \text{Phases}} \left( p \xrightarrow{\text{PhaseReady}(p)} \begin{cases} \texttt{✅ READY} & \text{PhaseReady}(p) \\ \texttt{🚫 BLOCKED} & \sim\text{PhaseReady}(p) \end{cases} \right)$$

## Step 5: Display

```
Task: {task-name}
Active: {N} agents  │  Archived: {M} agents

[Phase Gate]
  理解層 → 規劃層 : ✅ READY  /  🚫 BLOCKED ← {阻塞原因}
  規劃層 → 驗證層 : ✅ READY  /  🚫 BLOCKED ← {阻塞原因}
  規劃層 → 執行層 : ✅ READY  /  🚫 BLOCKED ← {阻塞原因}
──────────────────────────────────────────────────

[理解層]
  ✅ 3w              completed   {modified}
  ✅ mece            completed   {modified}
  🔄 thought-sphere  in_progress {modified}

[規劃層]
  ⬜ planning        pending     —          🔒 blocked ← 理解層 未全部完成
  ⬜ planning        pending     —          ▶ ready to run

[驗證層]
  ⬜ sese            pending     —          🔒 blocked ← planning 未完成

[執行層]
  ⬜ execution       pending     —          🔒 blocked ← planning 未完成

[其他]  （自定義 agents）

[已封存]  {M} 個
──────────────────────────────────────────────────
Dependencies: {depends_on 鏈路，若 frontmatter 有記錄則展開}
```

圖示對照：`✅ completed`  `🔄 in_progress`  `⬜ pending`  `📦 archived`  `▶ ready to run`  `🔒 blocked`
