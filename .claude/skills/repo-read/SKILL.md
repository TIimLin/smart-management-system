---
name: repo-read
description: >
  讀取開源 repo 調研報告與評估結論。
  Trigger: "看 repo", "查 {repo名}", "讀取調研", "read repo", "repo 狀態",
  或 AI 執行前需要了解某 repo 時自動叫用
argument-hint: [slug-or-name]
layer: 1
---

# Repo Read

$$\text{RepoRead} = \text{SlugResolve} \to \text{Read} \to \text{Render} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \begin{cases} \text{args}[0] & \text{直接使用（kebab-case 轉換）} \\ \varnothing & \to \texttt{git ls-files .ai-core/repos/} \to \text{列出所有 repos 供選擇} \end{cases}$$

$$\text{模糊比對}: \text{args}[0] \text{ 可為 name 或 slug 的部分字串} \to \text{找最近似的 slug}$$

$$(\text{多個候選}) \to \text{列出清單讓使用者選擇} \quad (\text{唯一候選}) \to \text{直接使用}$$

## Step 2: Read

$$\text{Read} = \text{REPO.md}_{frontmatter + body} \;\&\; \text{research/*.formula.md}_{列出全部}$$

$$\text{並行讀取}: \begin{cases} \texttt{.ai-core/repos/\{slug\}/REPO.md} & \text{必讀} \\ \texttt{.ai-core/repos/\{slug\}/research/} & \text{列出所有 *.formula.md} \\ \texttt{.ai-core/repos/\{slug\}/snapshots/} & \text{列出所有 *.formula.md（若有）} \end{cases}$$

$$\text{讀取 research/overview.formula.md}（\text{若存在}）$$

## Step 3: Render

$$\text{Render} = \text{StatusBadge} + \text{Identity} + \text{VersionInfo} + \text{Tags} + \text{Decision} + \text{Relations} + \text{ResearchList}$$

顯示結構化摘要：

$$\text{StatusBadge}: status \in \{assess,\; trial,\; adopt,\; hold,\; archived\} \to \text{醒目標示}$$

$$\text{VersionInfo} = \begin{cases} latest\_version & + & tracked\_version & + & version\_lag \\ latest\_released\_at & & checked\_at & \end{cases}$$

$$version\_lag = \begin{cases} \mathbb{Z}_{\geq 0} & \to \text{顯示「落後 n 版」} \\ null & \to \text{顯示「無 tag，不計算」} \end{cases}$$

$$\text{Relations} = \{related\_projects,\; related\_repos,\; related\_tasks,\; related\_schedules\} \to \text{連結列表}$$

$$\text{ResearchList} = \text{research/*.formula.md 檔案清單} + \text{snapshots/*.formula.md 檔案清單}$$

輸出格式範例：

```
[{status}] {name}

URL:      {url}
Stars:    {stars}
License:  {license}
Language: {language}
Tags:     {tags}

版本狀況：
  最新版本:   {latest_version}  ({latest_released_at})
  追蹤版本:   {tracked_version}
  版本落差:   {version_lag} 版 / null
  最後查核:   {checked_at}

採用決策: {status} — {overview 摘要中 Decision 節}

相關連結:
  {related_projects}
  {related_repos}
  {related_tasks}

調研文件:
  research/overview.formula.md
  research/*.formula.md（其他）
  snapshots/*.formula.md（若有）
```

## Step 4: Confirm

$$(\text{slug 存在}) \to \text{顯示 Render 結果}$$

$$(\text{slug 不存在}) \to \text{提示：此 slug 尚無記錄，請執行 repo-create \{slug\} 建立條目}$$
