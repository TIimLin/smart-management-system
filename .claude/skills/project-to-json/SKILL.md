---
name: project-to-json
description: >
  從 PROJECT.md frontmatter 生成 PROJECT.json，供靜態網頁 card 展示用。
  Trigger: "匯出 project json", "生成 project card 資料", "project-to-json",
  "建立 projects 的 JSON"。可指定單一 slug 或 --all 掃描全部
argument-hint: [slug | --all]
layer: 5
type: conversion
---

# Project To JSON

$$\text{ProjectToJSON} = \text{SlugResolve} \to \text{Read} \to \text{Transform} \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{Scope} = \begin{cases} \texttt{--all} & \to \text{glob 全部 .ai-core/projects/*/PROJECT.md} \\ \text{args[0]} & \to \text{單一 .ai-core/projects/\{slug\}/PROJECT.md} \\ \text{否則} & \to \text{詢問} \end{cases}$$

## Step 2: Read

讀取 PROJECT.md 的 frontmatter（所有 20 欄位）：

$$\text{Fields} = \{name,\; slug,\; description,\; status,\; url,\; local\_path,\; language,\; tags,$$
$$created,\; latest\_version,\; latest\_released\_at,\; total\_releases,$$
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
  "local_path": "",
  "language": [],
  "tags": [],
  "created": "",
  "latest_version": "",
  "latest_released_at": "",
  "total_releases": 0,
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

$$\text{型別律} = \begin{cases} \text{string 欄位空值} & \to \texttt{""} \\ \text{array 欄位空值} & \to \texttt{[]} \\ \texttt{total\_releases} & \to \text{integer}，\text{預設} 0 \end{cases}$$

## Step 4: Write

$$\text{OutputPath} = \texttt{.ai-core/projects/\{slug\}/PROJECT.json}$$

$$(\texttt{PROJECT.json} \exists) \to \text{直接覆寫（衍生檔，無需確認）}$$

每個 slug 各寫入獨立的 JSON 檔案。

## Step 5: Confirm

```
✅ Project JSON generated

生成檔案：
  .ai-core/projects/{slug}/PROJECT.json
  ...（--all 模式列出全部）

總計：{N} 個檔案
```
