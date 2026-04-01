---
name: repo-archive
description: >
  封存 repo 條目至 .ai-core/repos/archived/。
  Archive ≠ Delete：移動目錄，保留所有研究文件（research/, snapshots/, .cache/）。
  Trigger: "封存 repo", "archive repo {slug}", "不再追蹤 {repo名}"
argument-hint: "[slug]"
disable-model-invocation: true
layer: 1
---

# Repo Archive

$$\text{RepoArchive} = \text{SlugResolve} \to \text{ConfirmCheck} \to \text{StatusUpdate} \to \text{Move} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供 repo slug"})$$

$$\sim(\texttt{.ai-core/repos/\{slug\}/REPO.md} \;\exists) \to \text{錯誤：找不到 repo，用 repo-sort 確認 slug}$$

## Step 2: ConfirmCheck

$$\text{ConfirmCheck}: \text{顯示警告} \to \text{等待使用者確認（user-only）}$$

```
⚠️  即將封存 repo：{slug}

  From:  .ai-core/repos/{slug}/
  To:    .ai-core/repos/archived/{slug}/

  Archive ≠ Delete：所有研究文件保留，僅移動位置。
  確認封存？(y/N)
```

$$\text{N 或空白} \to \text{取消，不進行任何操作}$$

## Step 3: StatusUpdate

$$\text{Read}(\texttt{.ai-core/repos/\{slug\}/REPO.md}) \to \text{status} \leftarrow archived \to \text{Write}(\texttt{REPO.md})$$

$$\text{Frontmatter 律}: status: archived \quad \text{（符合 ThoughtWorks Technology Radar status 集合）}$$

## Step 4: Move

$$\text{Move}: \texttt{mkdir -p} \to \texttt{mv} \quad \text{（保留整個目錄樹）}$$

```bash
mkdir -p ".ai-core/repos/archived/"
mv ".ai-core/repos/{slug}/" ".ai-core/repos/archived/{slug}/"
```

$$\text{Archive 律}: \texttt{.ai-core/repos/archived/\{slug\}/} \supset \{REPO.md,\; research/,\; snapshots/,\; .cache/\}$$

## Step 5: Confirm

```
✅ Repo archived

slug:    {slug}
From:    .ai-core/repos/{slug}/
To:      .ai-core/repos/archived/{slug}/
status:  archived（已寫入 REPO.md frontmatter）

Archive ≠ Delete：所有研究文件完整保留。
```
