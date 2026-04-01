---
name: project-create
description: >
  建立新的專案條目（scaffold PROJECT.md + plans/ + research/ + .cache/）。
  Trigger: "新增專案", "建立 project", "開新專案", "create project",
  "記錄構想", "新增 {專案名}"
argument-hint: [slug-or-name]
layer: 2
type: crud
---

# Project Create

$$\text{ProjectCreate} = \text{NameResolve} \to \text{ConflictCheck} \to \text{DirScaffold} \to \text{ProjectMdInit} \to \text{CacheSetup} \to \text{Confirm}$$

## Step 1: NameResolve

$$\text{slug} = \text{kebab-case}(\text{args}[0]),\; |\text{slug}| \leq 40$$

$$\text{name} = \text{DisplayName}(\text{args}[0])$$

$$\sim(\text{args}[0] \text{ 已提供}) \to \text{詢問：slug 和顯示名稱}$$

slug 規則：全小寫、以 `-` 分隔、無特殊符號、≤ 40 字元。

## Step 2: ConflictCheck

$$(\texttt{.ai-core/projects/\{slug\}/} \exists) \to \text{警告} + \text{詢問：繼續覆寫 or 取消？}$$

$$\sim(\text{衝突}) \to \text{繼續下一步}$$

## Step 3: DirScaffold

```bash
mkdir -p ".ai-core/projects/{slug}/plans"
mkdir -p ".ai-core/projects/{slug}/research"
mkdir -p ".ai-core/projects/{slug}/.cache"
```

$$\text{Dir}_{project} = PROJECT.md + plans/ + research/ + \texttt{.cache/}$$

## Step 4: ProjectMdInit

建立 `.ai-core/projects/{slug}/PROJECT.md`，schema 遵循 project-contract：

**Frontmatter**（所有欄位永遠存在，空時為 ""、[]、0）：

```yaml
name: "{DisplayName}"
slug: "{slug}"
description: ""
status: idea
url: ""
local_path: ""
language: []
tags: []
created: "{today ISO 8601}"
latest_version: ""
latest_released_at: ""
total_releases: 0
default_branch: main
branches: []
related_projects: []
related_repos: []
related_tasks: []
related_schedules: []
```

**Body**（formula 格式）：

```markdown
# {Name}

$$\text{Project} = \text{構想}(\text{Why}) + \text{目標}(\text{What}) + \text{方案}(\text{How})$$

## 定位
{待填寫}

## 目標
{待填寫}

## 計劃
$$\text{Roadmap} = \text{Phase}_1 \to \text{Phase}_2 \to \ldots$$
```

$$\text{AI 推斷律}: \text{args 含足夠語意} \to \text{填入 description/tags/language}；\text{否則留空待填}$$

## Step 5: CacheSetup

$$(\text{args 含 local\_path}) \to \text{呼叫 project-code-link 建立 symlink}$$

$$\sim(\text{local\_path 已提供}) \to \text{跳過，提示：可事後呼叫 project-code-link}$$

project-code-link 執行：

```bash
ln -sf "{local_path}" ".ai-core/projects/{slug}/.cache/code"
```

## Step 6: Confirm

```
✅ Project created

Slug:    {slug}
Name:    {name}
Path:    .ai-core/projects/{slug}/
Status:  idea
Cache:   {symlink 已建立 | 未設定（可呼叫 project-code-link）}

→ 編輯 PROJECT.md 填入 description / 目標
→ 使用 project-update --add-plan <topic> 新增規劃文件
```
