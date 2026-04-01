---
name: project-sort
description: >
  列出所有 projects，依 status/priority 排序，呈現專案組合概覽（Portfolio View）。
  Trigger: "列出專案", "project 清單", "所有專案", "project-sort", "專案組合", "我有哪些專案"
argument-hint: [--status <status>] [--tag <tag>] [--sort-by <field>]
layer: 2
---

# Project Sort

$$\text{ProjectSort} = \text{Scan} \to \text{Parse} \to \text{Filter} \to \text{Sort} \to \text{Render} \to \text{Confirm}$$

## Step 1: Scan

$$\text{Files} = \text{Glob}(\texttt{.ai-core/projects/*/PROJECT.md},\; \text{exclude: archived/})$$

$$\text{--archived} \in \text{args} \Rightarrow \text{Files} \mathrel{+}= \text{Glob}(\texttt{.ai-core/projects/archived/*/PROJECT.md})$$

## Step 2: Parse

$$\forall f \in \text{Files}: \text{Meta}(f) = \text{frontmatter} \to \{name,\; slug,\; status,\; url,\; language,\; tags,\; created,\; latest\_version,\; total\_releases,\; default\_branch\}$$

## Step 3: Filter

$$\text{--status} \in \text{args} \Rightarrow \text{Files} \leftarrow \{f \mid f.status = \text{arg\_status}\}$$

$$\text{--tag} \in \text{args} \Rightarrow \text{Files} \leftarrow \{f \mid \text{arg\_tag} \in f.tags\}$$

## Step 4: Sort

$$\text{sort-by} = \begin{cases} \text{status（預設）} & active \succ shipped \succ planning \succ idea \succ archived \\ \text{created} & \text{created 降冪} \\ \text{name} & \text{name 升冪（字母序）} \end{cases}$$

$$\text{次序}: \text{status 相同時依 created 降冪排列}$$

## Step 5: Render

```
## Project Portfolio

### 🟢 Active（N）
- {name} [{status}] [{latest_version}] — {url | "（無 repo）"}
  tags: {tags} | lang: {language} | releases: {total_releases}

### ✅ Shipped（N）
- {name} [{status}] [{latest_version}] — {url | "（無 repo）"}
  tags: {tags} | lang: {language} | releases: {total_releases}

### 📋 Planning（N）
- {name} [{status}] — {url | "（無 repo）"}
  tags: {tags} | lang: {language}

### 💡 Idea（N）
- {name} [{status}] — {url | "（無 repo）"}
  tags: {tags}
```

$$\text{archived 象限}: \text{僅 --archived flag 時顯示}$$

## Step 6: Confirm

```
─────────────────────────────────────────────────────
Summary: 共 {N} 個 projects

  🟢 Active:   {N}
  ✅ Shipped:  {N}
  📋 Planning: {N}
  💡 Idea:     {N}
  🗄 Archived: {N}（用 --archived 顯示）
```
