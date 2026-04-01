---
name: repo-code-fetch
description: >
  clone 或 pull 最新代碼至 .ai-core/repos/{slug}/.cache/code/，供 AI 深度調研用。
  Trigger: "clone repo", "fetch repo 代碼", "下載 {repo名} 代碼", "repo-code-fetch {slug}", "我想看 {repo} 的源碼"
argument-hint: [slug]
layer: 5
---

# Repo Code Fetch

$$\text{RepoCodeFetch} = \text{SlugResolve} \to \text{UrlRead} \to \text{CacheCheck} \to \text{FetchOrPull} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供 repo slug"})$$

$$\sim(\texttt{.ai-core/repos/\{slug\}/REPO.md} \;\exists) \to \text{錯誤：找不到 repo，用 repo-sort 確認 slug}$$

## Step 2: UrlRead

$$\text{url} = \text{Read}(\texttt{.ai-core/repos/\{slug\}/REPO.md}).\text{frontmatter.url}$$

$$\text{url} = \text{""} \to \text{錯誤：REPO.md 未設定 url，請先執行 repo-update 填入 url 欄位}$$

## Step 3: CacheCheck

$$\text{CacheState} = \begin{cases} \nexists\;\texttt{.cache/code/} & \to \text{clone 模式} \\ \exists\;\texttt{.cache/code/.git} & \to \text{pull 模式} \\ \exists\;\texttt{.cache/code/（非 git）} & \to \text{警告：異常目錄，詢問清除後重新 clone} \end{cases}$$

## Step 4: FetchOrPull

$$\text{FetchOrPull} = \begin{cases} \text{clone 模式} & \to \texttt{git clone \{url\} .ai-core/repos/\{slug\}/.cache/code/} \\ \text{pull 模式} & \to \texttt{git -C .ai-core/repos/\{slug\}/.cache/code pull} \end{cases}$$

$$\text{clone 模式命令}: \texttt{git clone \{url\} .ai-core/repos/\{slug\}/.cache/code/}$$

$$\text{pull 模式命令}: \texttt{git -C .ai-core/repos/\{slug\}/.cache/code pull}$$

$$\text{保留律}: \texttt{.cache/code/} \text{ 永遠保留，直到 repo-code-clear 手動清除}$$

## Step 5: Confirm

$$\text{Confirm} = \text{顯示操作結果}(\text{模式},\; \text{最新 commit},\; \text{分支}) + \text{提示後續操作}$$

```
已完成代碼 {clone / pull}

slug:     {slug}
路徑:     .ai-core/repos/{slug}/.cache/code/
模式:     {clone / pull}
分支:     {branch}
最新 commit: {short-sha} {commit-message}

→ 執行 repo-update --sync-version 同步版本欄位至 REPO.md
→ 執行 repo-read {slug} 查看調研報告
```
