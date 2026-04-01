---
name: project-read
description: >
  讀取專案狀態、規劃文件、連結的 repos 與 tasks。
  Trigger: "看專案", "查 {project名}", "project 狀態", "read project",
  或 AI 執行前需要了解某 project 時自動叫用
argument-hint: [slug-or-name]
layer: 2
type: crud
---

# Project Read

$$\text{ProjectRead} = \text{SlugResolve} \to \text{Read} \to \text{Render} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{kebab-case}(\text{args}[0])$$

$$\sim(\text{args}[0] \text{ 已提供}) \to \text{列出所有} \texttt{.ai-core/projects/*/PROJECT.md} \text{讓使用者選擇}$$

$$\text{列出格式}: \{slug\} \mid \{name\} \mid \{status\} \mid \{latest\_version\}$$

## Step 2: Read（並行）

$$\text{Read} = \text{ProjectMd} \;\&\; \text{PlansList} \;\&\; \text{ResearchList}$$

$$\text{ProjectMd} = \text{Read}(\texttt{.ai-core/projects/\{slug\}/PROJECT.md})$$

$$\text{PlansList} = \text{Glob}(\texttt{.ai-core/projects/\{slug\}/plans/*.formula.md})$$

$$\text{ResearchList} = \text{Glob}(\texttt{.ai-core/projects/\{slug\}/research/*.formula.md})$$

## Step 3: Render

顯示結構化摘要，包含以下區塊：

$$\text{Render} = \text{Identity} + \text{Version} + \text{Branch} + \text{Tech} + \text{Relations} + \text{Docs}$$

**Identity 區塊**：

```
[{status}] {name}  ({slug})
描述：{description}
URL：  {url | "—"}
本機：{local_path | "—"}
```

**Version 區塊**：

$$\text{Version} = \{latest\_version,\; latest\_released\_at,\; total\_releases\}$$

```
版本：{latest_version | "尚無版本"}
發佈：{latest_released_at | "—"}  總計：{total_releases} releases
```

**Branch 區塊**：

$$\text{Branch} = \{default\_branch\} + \{branches\}$$

```
主分支：{default_branch}
分支：  {branches | "—"}
```

**Tech 區塊**：

```
語言：{language | "—"}
Tags：{tags | "—"}
```

**Relations 區塊**：

$$\text{Relations} = related\_projects + related\_repos + related\_tasks + related\_schedules$$

```
關聯 Projects：{related_projects | "—"}
關聯 Repos：   {related_repos | "—"}
關聯 Tasks：   {related_tasks | "—"}
關聯 Schedules：{related_schedules | "—"}
```

**Docs 區塊**：

```
Plans（{n} 份）：
  - {plans/*.formula.md 列表}

Research（{m} 份）：
  - {research/*.formula.md 列表}
```

## Step 4: Confirm（slug 不存在時）

$$\sim(\texttt{.ai-core/projects/\{slug\}/} \exists) \to \text{提示：}$$

```
找不到 project: {slug}
→ 使用 project-create {slug} 建立新專案
```
