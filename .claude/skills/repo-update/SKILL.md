---
name: repo-update
description: >
  更新 repo 評估狀態、新增研究筆記、自動從 GitHub API 或 git 更新
  version 三件組（checked_at, latest_version, latest_released_at, version_lag, default_branch, branches）。
  Trigger: "更新 repo", "update repo {slug}", "sync repo 版本", "新增調研筆記"
argument-hint: [slug] [--sync-version] [--add-note <topic>] [--status <new-status>]
layer: 1
---

# Repo Update

$$\text{RepoUpdate} = \text{SlugResolve} \to \text{Read} \to \text{ChangeDetect} \to \text{VersionSync}^{?} \to \text{NoteAdd}^{?} \to \text{StatusUpdate}^{?} \to \text{Write} \to \text{Confirm}$$

## Step 1: SlugResolve

$$\text{slug} = \text{args}[0] \mid \text{Ask}$$

$$\text{args 解析}: \begin{cases} \text{args}[0] & \to \text{slug} \\ \texttt{--sync-version} & \to \text{flag}_{sync} = \top \\ \texttt{--add-note <topic>} & \to \text{flag}_{note} = \top,\; topic = \text{args}[\texttt{--add-note}+1] \\ \texttt{--status <new-status>} & \to \text{flag}_{status} = \top,\; new\_status = \text{args}[\texttt{--status}+1] \end{cases}$$

## Step 2: Read

$$\text{Read} = \texttt{.ai-core/repos/\{slug\}/REPO.md}_{frontmatter}$$

$$(\texttt{.ai-core/repos/\{slug\}/} \nexists) \to \text{Error}: \text{slug 不存在，請先執行 repo-create \{slug\}}$$

## Step 3: ChangeDetect

$$\text{Operations} = \text{flags 分析} \to \{op_{sync},\; op_{note},\; op_{status}\} \subseteq \text{本次執行集合}$$

$$\text{預設行為（無 flags）}: \text{flag}_{sync} = \top \quad \text{（預設執行 VersionSync）}$$

$$\text{組合執行}: \text{各 op 獨立，可同時觸發}$$

## Step 4: VersionSync（--sync-version 或預設）

$$\text{VersionSync} = \text{DataFetch} \to \text{FieldUpdate}$$

$$\text{DataFetch 策略（優先序）}:$$

$$\text{Priority}_1: \text{GitHub API} \to \texttt{GET https://api.github.com/repos/\{owner\}/\{repo\}/releases/latest}$$

$$\quad \to \{latest\_version,\; latest\_released\_at\}$$

$$\text{Priority}_2: \text{API 失敗} \to \texttt{git ls-remote --tags \{url\}} \to \text{最新 tag} \to latest\_version$$

$$\text{Priority}_3: \nexists\;\text{tag} \to \texttt{git ls-remote \{url\} HEAD} \to \text{short SHA（7 位）} \to latest\_version$$

$$\text{Priority}_4: \text{全部失敗} \to latest\_version = \text{""},\; \text{記錄失敗原因}$$

$$\text{default\_branch}: \texttt{git ls-remote --symref \{url\} HEAD} \to \text{解析 HEAD \to refs/heads/\{branch\}}$$

$$\text{branches}: \texttt{git ls-remote --heads \{url\}} \to \text{所有分支名稱列表}$$

$$version\_lag = \begin{cases} \mathbb{Z}_{\geq 0} & \exists\;\text{tag/release，計算 tracked\_version 至 latest\_version 的版本差} \\ null & \nexists\;\text{tag，無法計數} \end{cases}$$

$$\text{FieldUpdate}: \{checked\_at = today,\; latest\_version,\; latest\_released\_at,\; version\_lag,\; default\_branch,\; branches\}$$

## Step 5: NoteAdd（--add-note <topic>）

$$\text{NoteAdd} = \text{建立 research/\{topic\}.formula.md（formula 格式）}$$

$$\text{路徑}: \texttt{.ai-core/repos/\{slug\}/research/\{topic\}.formula.md}$$

$$\text{內容}: \begin{cases} \text{frontmatter}: \{created = today,\; topic\} \\ \text{body}: \text{AI 依 topic 填充內容（thought-sphere 分析）} \end{cases}$$

$$(\text{檔案已存在}) \to \text{詢問：覆蓋 or 追加？}$$

## Step 6: StatusUpdate（--status <new-status>）

$$new\_status \in \{assess,\; trial,\; adopt,\; hold\} \quad \text{（archived 由 repo-archive 處理）}$$

$$(\nexists\; new\_status \in \text{合法集合}) \to \text{Error}: \text{無效 status，合法值為 \{assess, trial, adopt, hold\}}$$

$$\text{StatusUpdate}: REPO.md.frontmatter.status \leftarrow new\_status$$

## Step 7: Write

$$\text{Write} = \text{寫回更新的 REPO.md frontmatter}$$

$$\text{只更新本次 ChangeDetect 標記的欄位，其餘欄位保持原值}$$

$$\text{Write 策略}: \text{讀取原始 REPO.md} \to \text{patch frontmatter 指定欄位} \to \text{寫回完整 REPO.md}$$

## Step 8: Confirm

$$\text{Confirm} = \text{顯示更新摘要}$$

```
已更新 repo 條目

slug:   {slug}
路徑:   .ai-core/repos/{slug}/

版本同步（若執行）：
  latest_version:     {before} → {after}
  latest_released_at: {before} → {after}
  version_lag:        {before} → {after}
  default_branch:     {before} → {after}
  checked_at:         {today}

狀態變更（若執行）：
  status: {before} → {after}

新增筆記（若執行）：
  research/{topic}.formula.md

→ 執行 repo-read {slug} 查看最新狀態
```
