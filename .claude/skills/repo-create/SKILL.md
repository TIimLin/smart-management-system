---
name: repo-create
description: >
  建立新的開源 repo 調研條目（scaffold REPO.md + research/ + snapshots/ + .cache/），
  可選自動 git clone 並依調研骨架生成 research/overview.formula.md。
  Trigger: "調研 repo", "新增開源", "研究 {repo名}", "create repo", "調研 {url}"
argument-hint: [url-or-slug]
layer: 1
---

# Repo Create

$$\text{RepoCreate} = \text{SlugResolve} \to \text{ConflictCheck} \to \text{DirScaffold} \to \text{RepoMdInit} \to \text{ResearchInit} \to \text{CodeFetch}^{?} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{kebab-case}(\text{args}[0]),\; |\text{slug}| \leq 40$$

$$\text{Input} = \begin{cases} \text{URL} & \to \text{slug} = \text{kebab}(\text{path.last}),\; \text{name} = \text{path.last},\; \text{url} = \text{args}[0] \\ \text{slug} & \to \text{slug} = \text{args}[0],\; \text{name} = \text{args}[0],\; \text{url} = \text{""} \\ \varnothing & \to \text{Ask}(\text{url 或 slug？}) \end{cases}$$

$$\text{slug 格式律}: \text{lowercase},\; \text{hyphen-separated},\; \nexists\;\text{spaces},\; \nexists\;\text{special chars}$$

## Step 2: ConflictCheck

$$(\texttt{.ai-core/repos/\{slug\}/} \text{ 已存在}) \to \text{警告} + \text{詢問：繼續覆蓋 or 取消}$$

$$\sim\text{conflict} \to \text{proceed}$$

## Step 3: DirScaffold

$$\text{Scaffold} = \texttt{mkdir -p} \left\{ \begin{array}{l} \texttt{.ai-core/repos/\{slug\}/research} \\ \texttt{.ai-core/repos/\{slug\}/snapshots} \\ \texttt{.ai-core/repos/\{slug\}/.cache/code} \end{array} \right\}$$

$$\text{注意}: \texttt{.cache/code/} = \text{空目錄（預留 clone 位置，非立即 clone）}$$

## Step 4: RepoMdInit

建立 `REPO.md`（formula 格式，frontmatter 全欄位必填，空值依欄位型別填入）：

```yaml
---
name: "{name}"
slug: "{slug}"
description: ""
status: assess
url: "{url}"
stars: 0
license: ""
language: []
tags: []
checked_at: "{today}"
latest_version: ""
latest_released_at: ""
tracked_version: ""
version_lag: null
default_branch: ""
branches: []
related_projects: []
related_repos: []
related_tasks: []
related_schedules: []
---
```

$$\text{已知欄位}: \{name,\; slug,\; url,\; checked\_at = today\}$$

$$\text{空值律}: \text{string} \to \text{""} \mid \text{list} \to [] \mid \text{number} \to 0 \mid \text{nullable} \to null$$

body 加入：

$$\text{RepoMd} = \text{frontmatter} + \# \text{\{name\}} + \text{description placeholder}$$

## Step 5: ResearchInit

$$\text{ResearchInit} = \text{建立 research/overview.formula.md（依 repo-contract ResearchSkeleton）}$$

依 `repo-contract` 定義的 ResearchSkeleton 骨架建立 10 節：

$$\text{Sections} = \{3W, Market, TechStack, Architecture, DataFlow, UserFlow, API, CrossRef, Competitive, Decision\}$$

$$\text{填充策略} = \begin{cases} \text{已 clone} & \to \text{讀取 .cache/code/ 進行深度程式碼分析} \\ \text{未 clone} & \to \text{thought-sphere 自由分析 + 公開資訊推理} \end{cases}$$

各節以 formula + 繁體中文說明混排，AI 依現有資訊盡力填充，明確標示「待驗證」項目。

## Step 6: CodeFetch（optional）

$$\text{CodeFetch} = \text{詢問是否 git clone？}$$

$$\text{若是} \to \texttt{git clone \{url\} .ai-core/repos/\{slug\}/.cache/code}$$

$$\text{clone 後} \to \text{讀取 .cache/code/ 原始碼} \to \text{補充 research/overview.formula.md（更深入分析）}$$

$$\text{若否 / url 為空} \to \text{跳過，overview.formula.md 維持 thought-sphere 版本}$$

## Step 7: Confirm

$$\text{Confirm} = \text{顯示建立結果摘要}$$

```
已建立 repo 條目

slug:     {slug}
路徑:     .ai-core/repos/{slug}/
建立檔案: REPO.md
          research/overview.formula.md
建立目錄: snapshots/
          .cache/code/
clone:    {是 / 否}

→ 執行 repo-update --sync-version 取得最新版本資訊
→ 執行 repo-read {slug} 查看調研報告
```
