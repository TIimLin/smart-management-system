---
name: workflow-update
description: >
  Update a workflow protocol definition in .ai-core/tasks/{task}/workflows/{name}.md.
  Warns if the workflow has assigned agents or is in_progress.
  Trigger on "更新 workflow", "修改協作流程", "調整 workflow", "update workflow",
  "workflow 要改", "流程需要調整", "workflow 協議修正", "重定義 pipeline".
argument-hint: "[task-name] [workflow-name]"
disable-model-invocation: false
---

# Workflow Update

$$\text{WorkflowUpdate} = \text{Locate} \to \text{WorkflowRead} \to \text{ImpactCheck} \to \Delta\text{protocol} \to \text{Write} + \text{Log}$$

## Step 1: Locate

$$\text{Target} = \texttt{.ai-core/tasks/\{task\}/workflows/\{name\}.md}$$

$$\sim(\text{Target 存在}) \to \text{錯誤：workflow 不存在，先用 workflow-create 建立}$$

## Step 2: WorkflowRead

$$\text{載入現有 Protocol 供 AI 理解後再修改}$$

## Step 3: ImpactCheck

$$|\text{frontmatter.agents}| > 0 \to \text{⚠️ 此 workflow 已指派 agents，修改協議可能影響執行中任務}$$

$$\text{frontmatter.status} = \text{in\_progress} \to \text{⚠️ workflow 執行中，確認修改？}$$

## Step 4: Δprotocol

$$\Delta \in \{\text{追加內容},\; \text{替換指定段落},\; \text{全部重寫}\}$$

$$\text{frontmatter.modified} = \text{today ISO 8601 +08:00}$$

$$\text{frontmatter.status} = \text{視情況更新}(\text{pending} \mid \text{in\_progress} \mid \text{completed})$$

## Step 5: Write + Log

$$\text{Write}: \texttt{workflows/\{name\}.md} \leftarrow \Delta\text{protocol}$$

$$\text{Log}: \texttt{workflows/\{name\}.log} \mathrel{+}= \texttt{[\{timestamp\}] Updated: \{change\_summary\}}$$

```
✅ Workflow updated: {name}
Task:    {task-name}
Change:  {change_summary}
Status:  {new status}
Impact:  {N} assigned agents（須重讀 workflow 定義）
```
