---
name: project-link
description: >
  建立 project 與其他實體（project/repo/task/schedule）的雙向連結，
  寫入雙方 frontmatter 的 related_* 欄位。
  Trigger: "連結專案", "link project {slug} 到 {target}", "專案關聯 {repo/task}", "project 使用了 {repo}"
argument-hint: [slug] [target-type] [target-slug]
layer: 2
---

# Project Link

$$\text{ProjectLink} = \text{SlugResolve} \to \text{TargetResolve} \to \text{Read} \to \text{DuplicateCheck} \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供來源 project slug"})$$

$$\sim(\texttt{.ai-core/projects/\{slug\}/PROJECT.md} \;\exists) \to \text{錯誤：找不到 project，用 project-sort 確認 slug}$$

## Step 2: TargetResolve

$$\text{target\_type} = \text{args}[1] \in \{project,\; repo,\; task,\; schedule\} \mid \text{Ask}(\text{"目標類型？"})$$

$$\text{target\_slug} = \text{args}[2] \mid \text{Ask}(\text{"目標 slug？"})$$

$$\text{Entry 對照}: \begin{cases} project & \to PROJECT.md \\ repo & \to REPO.md \\ task & \to TASK.md \\ schedule & \to TASK.md \end{cases}$$

$$\text{target\_path} = \begin{cases} \texttt{.ai-core/projects/\{target\_slug\}/PROJECT.md} & \text{project} \\ \texttt{.ai-core/repos/\{target\_slug\}/REPO.md} & \text{repo} \\ \texttt{.ai-core/tasks/\{target\_slug\}/TASK.md} & \text{task} \\ \texttt{.ai-core/schedule/\{target\_slug\}/TASK.md} & \text{schedule} \end{cases}$$

$$\sim(\text{target\_path} \;\exists) \to \text{錯誤：找不到目標實體}$$

## Step 3: Read（並行）

$$\text{Read}(\texttt{.ai-core/projects/\{slug\}/PROJECT.md}) \parallel \text{Read}(\text{target\_path})$$

$$\text{提取}: \text{來源}.related\_\{type\}s + \text{目標}.related\_projects$$

## Step 4: DuplicateCheck

$$\text{src\_link} = \texttt{[[../../\{type\}s/\{target\_slug\}/\{Entry\}.md]]}$$

$$\text{dst\_link} = \texttt{[[../../projects/\{slug\}/PROJECT.md]]}$$

$$\text{src\_link} \in \text{來源}.related\_\{type\}s \;\lor\; \text{dst\_link} \in \text{目標}.related\_projects$$
$$\Rightarrow \text{警告：連結已存在，跳過寫入}$$

## Step 5: Write（雙方）

$$\text{Write}_{來源}: PROJECT.md.\text{related\_\{type\}s} \mathrel{+}= \left[\texttt{[[../../\{type\}s/\{target\_slug\}/\{Entry\}.md]]}\right]$$

$$\text{Write}_{目標}: \text{target\_doc}.related\_projects \mathrel{+}= \left[\texttt{[[../../projects/\{slug\}/PROJECT.md]]}\right]$$

$$\text{LinkLaw}: \text{link}(project, B) \to \begin{cases} B.related\_projects \ni \texttt{[[../../projects/\{slug\}/PROJECT.md]]} \\ project.related\_\{type\}s \ni \texttt{[[../../\{type\}s/\{B.slug\}/\{Entry\}.md]]} \end{cases}$$

## Step 6: Confirm

```
✅ Project link established

來源:  .ai-core/projects/{slug}/PROJECT.md
目標:  {target_path}

雙向連結已寫入：
  來源 related_{type}s += [[../../{type}s/{target_slug}/{Entry}.md]]
  目標 related_projects += [[../../projects/{slug}/PROJECT.md]]
```
