---
name: workflow-link
description: >
  Establish relationships involving workflows in .ai-core/tasks/{task}/.
  Mode A (assigns): add an agent to a workflow's scope — bidirectional update.
  Mode B (precedes): workflow-A must complete before workflow-B starts.
  Mode C (composes): workflow-A includes workflow-B as a sub-protocol.
  Trigger on "把 agent 加入 workflow", "assign agent to workflow",
  "workflow 關聯", "link workflow", "workflow 依賴",
  "A workflow 要等 B", "workflow 串接", "workflow 包含 agent",
  "建立 workflow agent 關係", "workflow-link".
argument-hint: [task-name] [source] [type: assigns|precedes|composes] [target]
disable-model-invocation: false
---

# Workflow Link

$$\text{WorkflowLink}(\text{src}, \text{type}, \text{dst}) = \text{Locate} \to \text{ValidateType} \to \text{MutateFrontmatter}(\text{src} \leftrightarrow \text{dst}) \to \text{Log}$$

## Step 1: Locate

$$\text{WorkflowDir} = \texttt{.ai-core/tasks/\{task\}/workflows/}$$

$$\text{type} = \text{assigns} \to \text{src} = \texttt{workflows/\{src\}.md},\; \text{dst} = \texttt{agents/\{dst\}.md}$$

$$\text{type} \in \{\text{precedes},\; \text{composes}\} \to \text{src, dst} \in \texttt{workflows/*.md}$$

$$\sim(\text{src 存在} \wedge \text{dst 存在}) \to \text{錯誤：列出現有 workflows / agents 供確認}$$

## Step 2: ValidateType

$$\text{type} \in \{\texttt{assigns},\; \texttt{precedes},\; \texttt{composes}\}$$

| type | 語意 | 典型用法 |
|------|------|---------|
| `assigns` | agent 加入 workflow 作用域 | `pipeline assigns execution` |
| `precedes` | src 完成後 dst 才能啟動 | `phase-1 precedes phase-2` |
| `composes` | src 包含 dst 為子協議 | `main composes sub-protocol` |

$$\sim(\text{type 合法}) \to \text{展示三種類型，請使用者選擇}$$

## Step 3: MutateFrontmatter

$$\text{type} = \text{assigns}:$$

$$\text{src.agents} \mathrel{+}= [\text{dst}],\quad \text{dst（agent）.belongs\_to} \mathrel{+}= [\text{src}]$$

$$\text{type} = \text{precedes}:$$

$$\text{src.precedes} \mathrel{+}= [\text{dst}],\quad \text{dst.depends\_on} \mathrel{+}= [\text{src}]$$

$$\text{type} = \text{composes}:$$

$$\text{src.composes} \mathrel{+}= [\text{dst}],\quad \text{dst.composed\_by} \mathrel{+}= [\text{src}]$$

$$(\text{關係已存在}) \to \text{跳過，提示：此關聯已建立}$$

## Step 4: Log

$$\text{src.log} \mathrel{+}= [\text{timestamp}]\; \text{WorkflowLink: src --\{type\}--> dst}$$

$$\text{type} = \text{assigns} \to \text{dst（agent）.log} \mathrel{+}= [\text{timestamp}]\; \text{assigned to workflow: src}$$

```
✅ Workflow linked

{src} --{type}--> {dst}
Task: {task-name}
```
