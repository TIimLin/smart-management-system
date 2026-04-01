---
name: repo-code-clear
description: >
  刪除 .ai-core/repos/{slug}/.cache/code/ 釋放磁碟空間。REPO.md 和 research/ 不受影響。
  Trigger: "清除 repo 代碼", "刪除 clone", "repo-code-clear {slug}", "清空 {repo名} 快取"
argument-hint: "[slug]"
disable-model-invocation: true
layer: 5
---

# Repo Code Clear

$$\text{RepoCodeClear} = \text{SlugResolve} \to \text{CacheCheck} \to \text{ConfirmCheck} \to \text{Clear} \to \text{Confirm}$$

$$\text{不可逆警告}: \text{此 skill 執行刪除，disable-model-invocation = true，僅限 user 手動觸發}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供 repo slug"})$$

$$\sim(\texttt{.ai-core/repos/\{slug\}/REPO.md} \;\exists) \to \text{錯誤：找不到 repo，用 repo-sort 確認 slug}$$

## Step 2: CacheCheck

$$\text{CacheExist} = \begin{cases} \exists\;\texttt{.ai-core/repos/\{slug\}/.cache/code/} & \to \text{繼續} \\ \nexists\;\texttt{.ai-core/repos/\{slug\}/.cache/code/} & \to \text{提示：快取不存在，無需清除} \end{cases}$$

## Step 3: ConfirmCheck

$$\text{ConfirmCheck} = \text{顯示警告} + \text{等待使用者確認}$$

```
警告：即將刪除 .ai-core/repos/{slug}/.cache/code/

受影響：.cache/code/（git clone 代碼，不可復原）
不受影響：REPO.md、research/、snapshots/

確認刪除？（輸入 yes 繼續）
```

$$\text{user 未確認} \to \text{中止操作，不執行刪除}$$

## Step 4: Clear

$$\text{Clear} = \texttt{rm -rf .ai-core/repos/\{slug\}/.cache/code/}$$

$$\text{刪除範圍}: \texttt{.cache/code/}（\text{僅代碼目錄，.cache/ 父目錄保留}）$$

## Step 5: Confirm

$$\text{Confirm} = \text{顯示已釋放} + \text{提示可用 repo-code-fetch 重新取得}$$

```
已清除代碼快取

slug:   {slug}
已刪除: .ai-core/repos/{slug}/.cache/code/
保留:   REPO.md、research/、snapshots/

→ 執行 repo-code-fetch {slug} 重新 clone 代碼
```
