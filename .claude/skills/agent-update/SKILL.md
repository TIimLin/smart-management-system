---
name: agent-update
description: >
  Update an agent's formula output in .ai-core/tasks/{task-name}/agents/{name}.md.
  Use when refining planning formulas, correcting execution output, or appending
  new stages. Trigger on "更新 agent", "修正 planning", "補充 execution",
  "update agent", "agent 寫錯了", "重寫 agent", "agent 需要調整".
argument-hint: "[task-name] [agent-name]"
disable-model-invocation: false
---

# Agent Update

$$\text{AgentUpdate} = \text{Locate} \to \text{AgentRead} \to \Delta\text{content} \to \text{Write} + \text{Log}$$

## Step 1: Locate

$$\text{Target} = \texttt{.ai-core/tasks/\{task\}/agents/\{name\}.md}$$

$$\sim(\text{Target 存在}) \to \text{錯誤：agent 不存在，先用 agent-create 建立}$$

## Step 2: AgentRead（先讀後改）

$$\text{載入現有內容供 AI 理解後再修改}$$

## Step 3: Δcontent

$$\Delta = \text{user 指定的修改範圍} \in \{\text{追加}, \text{替換特定段落}, \text{全部重寫}\}$$

$$\text{frontmatter.modified} = \text{today ISO 8601 +08:00}$$

$$\text{frontmatter.status} = \text{視情況更新}(\text{in\_progress} \mid \text{completed})$$

## Step 4: Write + Log

$$\text{Write}: \texttt{agents/\{name\}.md} \leftarrow \Delta\text{content}$$

$$\text{Log}: \texttt{agents/\{name\}.log} \mathrel{+}= \texttt{[\{timestamp\}] Updated: \{change\_summary\}}$$

```
✅ Agent updated: {name}
Task:    {task-name}
Change:  {change_summary}
Status:  {new status}
```
