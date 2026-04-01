---
name: agent-read
description: >
  Read an agent's formula output (.md) and execution log (.log) from
  .ai-core/tasks/{task-name}/agents/. Auto-trigger on "agent 輸出",
  "planning 寫了什麼", "execution 結果", "read agent", "看一下 planning",
  "看一下 execution", "agent 跑完了嗎", "agent 狀態".
argument-hint: "[task-name] [agent-name]"
---

# Agent Read

$$\text{AgentRead} = \text{Locate} \to \text{Parse}(\text{*.md} + \text{*.log}) \to \text{Display}$$

## Step 1: Locate

$$\text{AgentDir} = \texttt{.ai-core/tasks/\{task\}/agents/}$$

$$(\text{agent-name 已指定}) \to \text{直接讀取 agents/\{name\}.\{md, log\}}$$

$$\sim(\text{agent-name}) \to \text{列出 agents/*.md 供選擇}$$

$$\sim(\text{AgentDir 存在}) \to \text{提示：先用 agent-create 建立 agent}$$

## Step 2: Parse

$$\text{FormulaOutput} = \text{Read}(\texttt{agents/\{name\}.md})(\text{完整內容})$$

$$\text{LogHighlights} = \text{Read}(\texttt{agents/\{name\}.log})(\text{最後 20 行})$$

## Step 3: Display

```
📄 Agent: {name}  │  Task: {task-name}
Status: {frontmatter.status}  │  Created: {frontmatter.created}
─────────────────────────────────────────
Formula Output:
{agents/{name}.md 完整內容}

─────────────────────────────────────────
Recent Log (last 20 lines):
{agents/{name}.log tail -20}
```
