---
name: repo-to-json
description: >
  從 REPO.md frontmatter 生成 REPO.json，供靜態網頁 Technology Radar card 展示用。
  Trigger: "匯出 repo json", "生成 repo card 資料", "repo-to-json",
  "建立 repos 的 JSON"。可指定單一 slug 或 --all 掃描全部
argument-hint: [slug | --all]
layer: 5
type: conversion
---

# Repo To JSON

$$\text{RepoToJSON} = \text{SlugResolve} \to \text{Read} \to \text{Transform} \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{Scope} = \begin{cases} \texttt{--all} & \to \text{glob 全部 .ai-core/repos/*/REPO.md} \\ \text{args[0]} & \to \text{單一 .ai-core/repos/\{slug\}/REPO.md} \\ \text{否則} & \to \text{詢問} \end{cases}$$

## Step 2: Read

讀取 REPO.md 的 frontmatter（所有 20 欄位）：

$$\text{Fields} = \{name,\; slug,\; description,\; status,\; url,\; stars,\; license,\; language,\; tags,$$
$$checked\_at,\; latest\_version,\; latest\_released\_at,\; tracked\_version,\; version\_lag,$$
$$default\_branch,\; branches,\; related\_projects,\; related\_repos,\; related\_tasks,\; related\_schedules\}$$

## Step 3: Transform

將 frontmatter 轉換為 JSON 結構：

```json
{
  "name": "",
  "slug": "",
  "description": "",
  "status": "",
  "url": "",
  "stars": 0,
  "license": "",
  "language": [],
  "tags": [],
  "checked_at": "",
  "latest_version": "",
  "latest_released_at": "",
  "tracked_version": "",
  "version_lag": null,
  "default_branch": "",
  "branches": [],
  "related_projects": [],
  "related_repos": [],
  "related_tasks": [],
  "related_schedules": [],
  "_generated_at": "{ISO 8601 now}"
}
```

$$\texttt{\_generated\_at} = \text{ISO 8601 當下時間（非 frontmatter 欄位，供快取驗證用）}$$

$$\text{型別律} = \begin{cases} \text{string 欄位空值} & \to \texttt{""} \\ \text{array 欄位空值} & \to \texttt{[]} \\ \texttt{stars} & \to \text{integer}，\text{預設} 0 \\ \texttt{version\_lag} & \to \text{integer or null}，\text{無版本差距資料時為 } \texttt{null} \end{cases}$$

## Step 4: Write

$$\text{OutputPath} = \texttt{.ai-core/repos/\{slug\}/REPO.json}$$

$$(\texttt{REPO.json} \exists) \to \text{直接覆寫（衍生檔，無需確認）}$$

每個 slug 各寫入獨立的 JSON 檔案。

## Step 5: Confirm

```
✅ Repo JSON generated

生成檔案：
  .ai-core/repos/{slug}/REPO.json
  ...（--all 模式列出全部）

總計：{N} 個檔案
```

$$\text{Hint}_{--all} = \text{生成的 JSON 可合併為單一 } \texttt{repos-index.json}（\text{手動或搭配自訂腳本}）$$
