---
name: project-code-link
description: >
  建立或更新 .ai-core/projects/{slug}/.cache/code symlink 指向 local_path（本機 repo 路徑），讓 AI 可直接讀取本機代碼。
  Trigger: "連結本機 repo", "project-code-link {slug}", "設定 local_path", "讓 AI 讀我的本地代碼 {project}"
argument-hint: "[slug] [local-path]"
layer: 5
---

# Project Code Link

$$\text{ProjectCodeLink} = \text{SlugResolve} \to \text{PathResolve} \to \text{ValidateLocal} \to \text{LinkCreate} \to \text{FrontmatterUpdate} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供 project slug"})$$

$$\sim(\texttt{.ai-core/projects/\{slug\}/PROJECT.md} \;\exists) \to \text{錯誤：找不到 project，用 project-sort 確認 slug}$$

## Step 2: PathResolve

$$\text{local\_path} = \begin{cases} \text{args}[1] & \exists\;\text{args}[1] \\ \text{Read}(PROJECT.md).\text{frontmatter.local\_path} & \text{args}[1] = \varnothing \;\land\; local\_path \neq \text{""} \\ \text{Ask}(\text{"請提供本機 repo 絕對路徑"}) & \text{args}[1] = \varnothing \;\land\; local\_path = \text{""} \end{cases}$$

$$\text{路徑格式律}: local\_path = \text{絕對路徑（以 / 開頭）}$$

## Step 3: ValidateLocal

$$\text{Validate} = \texttt{git -C \{local\_path\} rev-parse --git-dir}$$

$$\text{ValidateResult} = \begin{cases} \text{成功（exit 0）} & \to \text{有效 git repo，繼續} \\ \texttt{local\_path} \;\nexists & \to \text{錯誤：路徑不存在} \\ \text{非 git repo（exit non-0）} & \to \text{警告：路徑存在但非 git repo，詢問是否繼續} \end{cases}$$

## Step 4: LinkCreate

$$\text{Link} = \begin{cases} \exists\;\texttt{.cache/code} & \to \texttt{rm -f .cache/code} \to \text{重建 symlink} \\ \nexists\;\texttt{.cache/code} & \to \text{直接建立 symlink} \end{cases}$$

$$\text{建立命令}: \texttt{ln -sf \{local\_path\} .ai-core/projects/\{slug\}/.cache/code}$$

$$\text{保留律}: \texttt{.cache/} \text{ 父目錄永遠保留；symlink 本身可由本 skill 重置}$$

## Step 5: FrontmatterUpdate

$$\text{FrontmatterUpdate} = \begin{cases} \text{args}[1] \;\exists & \to \text{更新 PROJECT.md frontmatter local\_path = args}[1] \\ \text{args}[1] = \varnothing & \to \text{跳過（local\_path 欄位維持原值）} \end{cases}$$

$$\text{更新目標}: \texttt{.ai-core/projects/\{slug\}/PROJECT.md}.\text{frontmatter.local\_path}$$

## Step 6: Confirm

$$\text{Confirm} = \text{顯示 symlink 結果} + \text{提示 AI 可透過 .cache/code/ 讀取本機代碼}$$

```
已建立代碼 symlink

slug:       {slug}
symlink:    .ai-core/projects/{slug}/.cache/code
指向:       {local_path}
local_path: {已更新 / 未變動}

→ AI 現在可透過 .ai-core/projects/{slug}/.cache/code/ 直接讀取本機代碼
→ 執行 project-read {slug} 查看專案狀態
```
