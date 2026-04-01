---
name: project-update
description: >
  更新專案狀態、新增規劃文件、自動從本機 git 同步 version 欄位
  （latest_version, latest_released_at, total_releases, default_branch, branches）。
  Trigger: "更新專案", "update project {slug}", "sync project 版本",
  "新增計劃文件", "專案狀態改為 {status}"
argument-hint: "[slug] [--sync-version] [--add-plan <topic>] [--add-research <topic>] [--status <new-status>]"
layer: 2
type: crud
---

# Project Update

$$\text{ProjectUpdate} = \text{SlugResolve} \to \text{Read} \to \text{ChangeDetect} \to \text{VersionSync}^? \to \text{DocAdd}^? \to \text{StatusUpdate}^? \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{kebab-case}(\text{args}[0])$$

$$\sim(\text{args}[0]) \to \text{列出現有 projects 讓使用者選擇}$$

$$\sim(\texttt{.ai-core/projects/\{slug\}/} \exists) \to \text{錯誤：找不到專案，建議 project-create}$$

## Step 2: Read

$$\text{Read}(\texttt{.ai-core/projects/\{slug\}/PROJECT.md}) \to \text{frontmatter 解析}$$

讀取全部 frontmatter 欄位，尤其 `local_path`（VersionSync 使用）。

## Step 3: ChangeDetect

$$\text{Ops} = \{op \mid \text{flag} \in \text{args}\}$$

$$\text{Ops} \subseteq \{\text{VersionSync},\; \text{DocAdd},\; \text{StatusUpdate}\}$$

$$\text{flag 映射}: \begin{cases} \texttt{--sync-version} \to \text{VersionSync} \\ \texttt{--add-plan} \to \text{DocAdd}(\text{plans}) \\ \texttt{--add-research} \to \text{DocAdd}(\text{research}) \\ \texttt{--status} \to \text{StatusUpdate} \end{cases}$$

$$\sim(\text{任何 flag 指定}) \to \text{預設執行 VersionSync（若 local\_path 存在）}$$

## Step 4: VersionSync（--sync-version 或預設）

$$(\text{local\_path} \neq \text{""}) \to \text{執行 git 查詢}$$

$$(\text{local\_path} = \text{""}) \to \text{跳過，提示設定 local\_path 後再執行}$$

git 指令序列：

```bash
# latest_version：最新 tag
git -C "{local_path}" tag --sort=-creatordate | head -1

# latest_released_at：最新 tag 的提交時間
git -C "{local_path}" log -1 --format=%ai \
  $(git -C "{local_path}" tag --sort=-creatordate | head -1)

# total_releases：tag 總數（近似值）
git -C "{local_path}" tag | wc -l

# branches：所有分支列表
git -C "{local_path}" branch -a

# default_branch：當前 HEAD 分支
git -C "{local_path}" symbolic-ref --short HEAD
```

$$\text{VersionSync 更新欄位}: \{latest\_version,\; latest\_released\_at,\; total\_releases,\; default\_branch,\; branches\}$$

$$\text{latest\_version 策略}: \begin{cases} \text{SemVer tag（如 v1.2.3）} & \exists\;\text{tag} \\ \text{short SHA（7 位）} & \nexists\;\text{tag},\;\exists\;\text{commits} \\ \text{""} & \text{尚無任何提交} \end{cases}$$

## Step 5: DocAdd（--add-plan / --add-research）

$$\text{DocAdd}(\text{plans}, topic) \to \texttt{.ai-core/projects/\{slug\}/plans/\{topic\}.formula.md}$$

$$\text{DocAdd}(\text{research}, topic) \to \texttt{.ai-core/projects/\{slug\}/research/\{topic\}.formula.md}$$

新文件骨架（formula 格式）：

```markdown
---
created: {today ISO 8601}
modified: {today ISO 8601}
topic: {topic}
---

# {Topic}

$$\text{{Topic}} = \text{目標} + \text{方案} + \text{行動}$$

## 概述
{待填寫}

## 細節
{待填寫}
```

## Step 6: StatusUpdate（--status）

$$\text{status} \in \{idea,\; planning,\; active,\; shipped\}$$

$$\text{archived} \notin \text{StatusUpdate 選項},\quad \text{封存請使用 project-archive}$$

$$(\text{status} \notin \text{有效值}) \to \text{錯誤：status 無效，列出有效選項}$$

## Step 7: Write

$$\text{Write}(\texttt{PROJECT.md}) = \text{更新後 frontmatter} + \text{原有 body（不修改）}$$

更新 frontmatter 僅覆蓋被 Ops 影響的欄位，其餘欄位保留原值。

## Step 8: Confirm

```
✅ Project updated: {slug}

操作：{執行的 Ops 列表}

VersionSync：
  latest_version:    {latest_version | "跳過"}
  latest_released_at:{latest_released_at | "跳過"}
  total_releases:    {total_releases | "跳過"}
  default_branch:    {default_branch | "跳過"}
  branches:          {branches | "跳過"}

DocAdd：{新建文件路徑 | "無"}
Status：{舊 status} → {新 status | "無變更"}
```
