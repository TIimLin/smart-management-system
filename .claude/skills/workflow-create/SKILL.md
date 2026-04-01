---
name: workflow-create
description: >
  Create a workflow protocol under .ai-core/tasks/{task}/workflows/.
  Workflows define agent collaboration: sequencing, data flow, gate conditions.
  Types: solo (single-agent execution protocol) or multi-agent (orchestration).
  Discovers workflow-role-* templates dynamically from .claude/skills/.
  Trigger on "建立 workflow", "create workflow", "定義協作流程",
  "設計 agent 協作", "規劃執行順序", "agent 協作協議", "多 agent 調度",
  "workflow 建立", "orchestrate agents".
argument-hint: "[task-name] [workflow-name] [type: solo|multi-agent]"
disable-model-invocation: false
---

# Workflow Create

$$\text{WorkflowCreate}(\text{task}, \text{name}, \text{type}) = \text{Resolve} \to \text{TypeSelect} \to \text{RoleLoad} \to \text{Scaffold} \to \text{Confirm}$$

## Step 1: Resolve

$$\text{TaskDir} = \texttt{.ai-core/tasks/\{task\}/}$$

$$\sim(\text{TaskDir 存在}) \to \text{錯誤：先用 task-create 建立任務}$$

$$(\texttt{workflows/\{name\}.md} \text{ 已存在}) \to \text{詢問：覆蓋 or 取消？}$$

## Step 2: TypeSelect

$$\text{type} \in \{\text{solo},\; \text{multi-agent}\}$$

$$\sim(\text{type 已指定}) \to \text{詢問：solo（單 agent 執行協議）or multi-agent（多 agent 調度）？}$$

$$\text{solo}: \text{定義單一 agent 的執行脈絡與輸出契約}$$

$$\text{multi-agent}: \text{orchestrates} \geq 2 \text{ agents，含順序} + \text{資料流向} + \text{Gate 條件}$$

## Step 3: RoleLoad

$$\text{AvailableRoles} = \text{Glob}(\texttt{.claude/skills/workflow-role-*/SKILL.md}) \to \text{動態枚舉}$$

$$(\text{AvailableRoles} \neq \emptyset) \to \text{列出供選擇（含 bare：不套用角色模板）}$$

$$(\text{AvailableRoles} = \emptyset) \to \text{使用 bare 模板，跳過}$$

## Step 4: Scaffold

```bash
mkdir -p ".ai-core/tasks/{task}/workflows"
```

建立 `workflows/{name}.md`：

```markdown
---
created: {today ISO 8601 +08:00}
task: {task-name}
name: {name}
type: {solo | multi-agent}
agents: []
status: pending
---

# {name} Workflow

$$\text{Pipeline} = {待定義協作順序與資料流向}$$

## 協作協議

{待填寫}

## 閘道條件（Gate Conditions）

{待填寫}
```

建立 `workflows/{name}.log`：

```
[{timestamp}] Workflow {name} created · type: {type} · task: {task-name}
```

## Step 5: Confirm

```
✅ Workflow created: {name}
Task:   {task-name}
Type:   {type}
Role:   {role | bare}
Files:  workflows/{name}.md + workflows/{name}.log

→ 編輯 Pipeline 公式定義協作順序
→ 使用 workflow-link 將 agents 指派到此 workflow
```
