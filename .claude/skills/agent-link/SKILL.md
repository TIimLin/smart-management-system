---
name: agent-link
description: >
  Establish explicit collaboration relationships between agents in
  .ai-core/tasks/{task}/agents/ via frontmatter fields.
  Link types: depends_on (dst reads src before starting),
  informs (src output feeds dst), validates (src is quality gate for dst).
  Trigger on "planning 要先跑才能 execution", "agent 依賴",
  "建立 agent 關聯", "link agents", "agent 協作圖", "agent 依賴鏈",
  "execution 依賴 planning", "sese 驗證 execution", "agent 串起來".
argument-hint: [task-name] [src] [type] [dst]
disable-model-invocation: false
---

# Agent Link

$$\text{AgentLink}(\text{src}, \text{type}, \text{dst}) = \text{LocateBoth} \to \text{ValidateType} \to \text{MutateFrontmatter}(src \leftrightarrow dst) \to \text{Log}$$

## Step 1: LocateBoth

$$\text{AgentDir} = \texttt{.ai-core/tasks/\{task\}/agents/}$$

$$\text{Src} = \texttt{agents/\{src\}.md},\quad \text{Dst} = \texttt{agents/\{dst\}.md}$$

$$\sim(\text{src 存在} \wedge \text{dst 存在}) \to \text{錯誤：列出現有 agents 供確認}$$

## Step 2: ValidateType

$$\text{type} \in \{\texttt{depends\_on},\; \texttt{informs},\; \texttt{validates}\}$$

| type | 語意 | 典型用法 |
|------|------|---------|
| `depends_on` | dst 執行前必須讀 src 的輸出 | `execution depends_on planning` |
| `informs` | src 的輸出餵給 dst 作為輸入 | `mece informs planning` |
| `validates` | src 是 dst 的品質閘道 | `sese validates execution` |

$$(\text{type 未指定或不合法}) \to \text{展示三種類型，請使用者選擇}$$

## Step 3: MutateFrontmatter

$$\text{src.md frontmatter 追加（或更新）：}$$

```yaml
informs: [{dst}, ...existing]       # type = informs
validates: [{dst}, ...existing]     # type = validates
# type = depends_on 時 src 不修改
```

$$\text{dst.md frontmatter 追加（或更新）：}$$

```yaml
depends_on: [{src}, ...existing]    # type = depends_on or informs
validated_by: [{src}, ...existing]  # type = validates
```

$$(\text{關係已存在}) \to \text{跳過，提示：此關聯已建立}$$

## Step 4: Log

$$\text{兩份 .log 各追加：} [\text{timestamp}]\ \text{AgentLink: \{src\} --\{type\}--> \{dst\}}$$

```
✅ Agent linked

{src} --{type}--> {dst}
Task: {task-name}
```
