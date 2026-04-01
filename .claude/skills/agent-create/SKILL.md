---
name: agent-create
description: >
  Create an agent instance under .ai-core/tasks/{task-name}/agents/.
  Discovers available roles dynamically from .claude/skills/agent-role-*/SKILL.md.
  Core roles: planning (技術規劃公式), execution (程式實作).
  Trigger on "建立 agent", "create agent", "開始規劃", "開始執行",
  "跑一下 planning", "跑一下 execution", or when applying any thinking role to a task.
argument-hint: [task-name] [role]
disable-model-invocation: false
---

# Agent Create

$$\text{AgentCreate}(\text{task}, \text{role}) = \text{Resolve} \to \text{FileScaffold} \to \text{RoleLoad} \to \text{RoleExecution}$$

## Step 1: Resolve

$$\text{TaskDir} = \texttt{.ai-core/tasks/\{task\}/}$$

$$\sim(\text{TaskDir 存在}) \to \text{錯誤：先用 task-create 建立任務}$$

$$\text{Available Roles} = \text{Glob}(\texttt{.claude/skills/agent-role-*/SKILL.md}) \to \text{動態枚舉}$$

$$(\text{role 未指定}) \to \text{列出 Available Roles 供選擇}$$

$$(\texttt{agents/\{role\}.md} \text{ 已存在}) \to \text{詢問：覆蓋 or 附加？}$$

## Step 2: FileScaffold

建立 `agents/{role}.md`：

```markdown
---
created: {today ISO 8601 +08:00}
task: {task-name}
role: {role}
status: in_progress
---

# {Role} Agent Output

{Agent 執行後填入}
```

建立 `agents/{role}.log`：

```
[{timestamp}] Agent {role} created for task: {task-name}
```

## Step 3: RoleLoad

$$\text{讀取} \texttt{.claude/skills/agent-role-\{role\}/SKILL.md} \text{（及 references/*.formula.md）}$$

$$\text{將角色的思維模式、輸出規範載入當前上下文}$$

## Step 4: RoleExecution

$$(\text{role} = \text{planning}) \to \text{依 agent-role-planning 規範：分析 TASK.md} \to \text{生成 WorkflowFormula + ImplementationFormula}$$

$$(\text{role} = \text{execution}) \to \text{依 agent-role-execution 規範：讀取 agents/planning.md} \to \text{實作程式碼}$$

$$(\text{其他 role}) \to \text{依對應 agent-role-\{role\} 規範執行}$$

執行過程：
- 公式輸出即時寫入 `agents/{role}.md`
- 進度日誌即時追加到 `agents/{role}.log`

```
✅ Agent created & running: {role}
Task:  {task-name}
Role:  {role}
Files: agents/{role}.md + agents/{role}.log
```
