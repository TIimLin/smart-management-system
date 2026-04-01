---
name: project-archive
description: >
  封存 project 條目至 .ai-core/projects/archived/。
  Archive ≠ Delete：移動目錄，保留所有規劃和研究文件（plans/, research/, .cache/）。
  Trigger: "封存專案", "archive project {slug}", "專案結束", "不再追蹤此專案"
argument-hint: [slug]
disable-model-invocation: true
layer: 2
---

# Project Archive

$$\text{ProjectArchive} = \text{SlugResolve} \to \text{ConfirmCheck} \to \text{StatusUpdate} \to \text{Move} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}(\text{"請提供 project slug"})$$

$$\sim(\texttt{.ai-core/projects/\{slug\}/PROJECT.md} \;\exists) \to \text{錯誤：找不到 project，用 project-sort 確認 slug}$$

## Step 2: ConfirmCheck

$$\text{ConfirmCheck}: \text{顯示警告} \to \text{等待使用者確認（user-only）}$$

```
⚠️  即將封存 project：{slug}

  From:  .ai-core/projects/{slug}/
  To:    .ai-core/projects/archived/{slug}/

  Archive ≠ Delete：所有規劃和研究文件保留，僅移動位置。
  確認封存？(y/N)
```

$$\text{N 或空白} \to \text{取消，不進行任何操作}$$

## Step 3: StatusUpdate

$$\text{Read}(\texttt{.ai-core/projects/\{slug\}/PROJECT.md}) \to \text{status} \leftarrow archived \to \text{Write}(\texttt{PROJECT.md})$$

$$\text{Frontmatter 律}: status: archived \quad \text{（status} \in \{idea,\; planning,\; active,\; shipped,\; archived\}\text{）}$$

## Step 4: Move

$$\text{Move}: \texttt{mkdir -p} \to \texttt{mv} \quad \text{（保留整個目錄樹）}$$

```bash
mkdir -p ".ai-core/projects/archived/"
mv ".ai-core/projects/{slug}/" ".ai-core/projects/archived/{slug}/"
```

$$\text{Archive 律}: \texttt{.ai-core/projects/archived/\{slug\}/} \supset \{PROJECT.md,\; plans/,\; research/,\; .cache/\}$$

## Step 5: Confirm

```
✅ Project archived

slug:    {slug}
From:    .ai-core/projects/{slug}/
To:      .ai-core/projects/archived/{slug}/
status:  archived（已寫入 PROJECT.md frontmatter）

Archive ≠ Delete：所有規劃和研究文件完整保留。
注意：.cache/code symlink 已隨目錄移動，不影響 local_path 實際目錄。
```
