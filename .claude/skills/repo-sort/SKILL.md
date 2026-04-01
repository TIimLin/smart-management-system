---
name: repo-sort
description: >
  列出所有 repos 的 Technology Radar 視圖，依 status/category/stars/checked_at 排序。
  Trigger: "列出 repos", "repo 清單", "technology radar", "哪些 repos", "repo-sort", "開源調研清單"
argument-hint: [--status <status>] [--tag <tag>] [--sort-by <field>]
layer: 1
---

# Repo Sort

$$\text{RepoSort} = \text{Scan} \to \text{Parse} \to \text{Filter} \to \text{Sort} \to \text{Render} \to \text{Confirm}$$

## Step 1: Scan

$$\text{Files} = \text{Glob}(\texttt{.ai-core/repos/*/REPO.md},\;\text{exclude: archived/})$$

$$\text{--archived flag} \Rightarrow \text{Files} \mathrel{+}= \text{Glob}(\texttt{.ai-core/repos/archived/*/REPO.md})$$

$$\sim(\text{Files} \neq \emptyset) \to \text{提示：尚無任何 repo 條目，用 repo-create 新增}$$

## Step 2: Parse

$$\text{每個 REPO.md 提取 frontmatter}: \{name,\; slug,\; status,\; stars,\; tags,\; checked\_at,\; latest\_version,\; tracked\_version,\; version\_lag,\; url\}$$

$$\text{欄位缺失律}: \text{欄位不存在} \to \text{以預設值替補} \quad \{stars \leftarrow 0,\; status \leftarrow assess,\; \text{其餘} \leftarrow ""\}$$

## Step 3: Filter

$$\text{--status} \; s \Rightarrow \text{保留} \; \{r \mid r.status = s\}$$

$$\text{--tag} \; t \Rightarrow \text{保留} \; \{r \mid t \in r.tags\}$$

$$\text{無 filter} \Rightarrow \text{保留全部（含 adopt/trial/assess/hold，不含 archived，除非 --archived）}$$

## Step 4: Sort

$$\text{預設排序}: \text{status 優先序} \succ \text{stars 降冪}$$

$$\text{status 優先序}: adopt \succ trial \succ assess \succ hold \succ archived$$

$$\text{--sort-by} = \begin{cases} checked\_at & \text{依最後排查時間降冪} \\ stars & \text{依 stars 降冪} \\ name & \text{依名稱字母升冪} \end{cases}$$

## Step 5: Render

$$\text{Render}: \text{Technology Radar 格式，依 status 分區顯示}$$

```
## Technology Radar

### 🟢 Adopt（N）
- {name} [{stars}★] [{latest_version}] — {url}
  tags: {tags} | lag: {version_lag} | checked: {checked_at}

### 🔵 Trial（N）
- {name} [{stars}★] [{latest_version}] — {url}
  tags: {tags} | lag: {version_lag} | checked: {checked_at}

### 🟡 Assess（N）
- {name} [{stars}★] [{latest_version}] — {url}
  tags: {tags} | lag: {version_lag} | checked: {checked_at}

### 🔴 Hold（N）
- {name} [{stars}★] [{latest_version}] — {url}
  tags: {tags} | lag: {version_lag} | checked: {checked_at}
```

$$\text{archived 律}: \text{archived 區塊僅在 --archived flag 時顯示}$$

$$\text{version\_lag 顯示}: \begin{cases} null & \to \text{"lag: —"（無 tag）} \\ 0 & \to \text{"lag: 0（最新）"} \\ n > 0 & \to \text{"lag: +n"} \end{cases}$$

## Step 6: Confirm

```
─────────────────────────────────────────────
Summary: {N} repos total

  🟢 Adopt  {N}  ·  🔵 Trial  {N}  ·  🟡 Assess  {N}  ·  🔴 Hold  {N}
  （封存：{N}，未顯示）
```
