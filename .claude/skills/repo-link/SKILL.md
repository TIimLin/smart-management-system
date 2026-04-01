---
name: repo-link
description: >
  建立 repo 與其他實體（project/repo/task/schedule）的雙向連結，
  寫入雙方 frontmatter 的 related_* 欄位。
  Trigger: "連結 repo", "link repo {slug} 到 {target}", "repo 關聯 {project/task}"
argument-hint: [slug] [target-type] [target-slug]
layer: 1
---

# Repo Link

$$\text{RepoLink} = \text{SlugResolve} \to \text{TargetResolve} \to \text{Read} \to \text{DuplicateCheck} \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供來源 repo slug"})$$

$$\sim(\texttt{.ai-core/repos/\{slug\}/REPO.md} \;\exists) \to \text{錯誤：找不到 repo，用 repo-sort 確認 slug}$$

## Step 2: TargetResolve

$$\text{target\_type} = \text{args}[1] \in \{project,\; repo,\; task,\; schedule\} \mid \text{Ask}(\text{"目標類型？"})$$

$$\text{target\_slug} = \text{args}[2] \mid \text{Ask}(\text{"目標 slug？"})$$

$$\text{Entry 對照}: \begin{cases} project & \to PROJECT.md \\ repo & \to REPO.md \\ task & \to TASK.md \\ schedule & \to TASK.md \end{cases}$$

$$\text{target\_path} = \begin{cases} \texttt{.ai-core/projects/\{target\_slug\}/PROJECT.md} & \text{project} \\ \texttt{.ai-core/repos/\{target\_slug\}/REPO.md} & \text{repo} \\ \texttt{.ai-core/tasks/\{target\_slug\}/TASK.md} & \text{task} \\ \texttt{.ai-core/schedule/\{target\_slug\}/TASK.md} & \text{schedule} \end{cases}$$

$$\sim(\text{target\_path} \;\exists) \to \text{錯誤：找不到目標實體}$$

## Step 3: Read（並行）

$$\text{Read}(\texttt{.ai-core/repos/\{slug\}/REPO.md}) \parallel \text{Read}(\text{target\_path})$$

$$\text{提取}: \text{來源}.related\_\{type\}s + \text{目標}.related\_repos$$

## Step 4: DuplicateCheck

$$\text{src\_link} = \texttt{[[../../\{type\}s/\{target\_slug\}/\{Entry\}.md]]}$$

$$\text{dst\_link} = \texttt{[[../../repos/\{slug\}/REPO.md]]}$$

$$\text{src\_link} \in \text{來源}.related\_\{type\}s \;\lor\; \text{dst\_link} \in \text{目標}.related\_repos$$
$$\Rightarrow \text{警告：連結已存在，跳過寫入}$$

## Step 5: Write（雙方）

$$\text{Write}_{來源}: REPO.md.\text{related\_\{type\}s} \mathrel{+}= \left[\texttt{[[../../\{type\}s/\{target\_slug\}/\{Entry\}.md]]}\right]$$

$$\text{Write}_{目標}: \text{target\_doc}.related\_repos \mathrel{+}= \left[\texttt{[[../../repos/\{slug\}/REPO.md]]}\right]$$

$$\text{LinkLaw}: \text{link}(repo, B) \to \begin{cases} B.related\_repos \ni \texttt{[[../../repos/\{slug\}/REPO.md]]} \\ repo.related\_\{type\}s \ni \texttt{[[../../\{type\}s/\{B.slug\}/\{Entry\}.md]]} \end{cases}$$

## Step 6: Confirm

```
✅ Repo link established

來源:  .ai-core/repos/{slug}/REPO.md
目標:  {target_path}

雙向連結已寫入：
  來源 related_{type}s += [[../../{type}s/{target_slug}/{Entry}.md]]
  目標 related_repos   += [[../../repos/{slug}/REPO.md]]
```
