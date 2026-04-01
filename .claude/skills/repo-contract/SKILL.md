---
name: repo-contract
description: >
  AI Core Entity Contract Layer 0：repo 實體憲法。
  定義 REPO.md schema、目錄結構律、formula 格式律、research 骨架模板、version 追蹤律、.cache clone 律。
  Single source of truth for all repo-* skills。
  Auto-loaded by repo-create/read/update/archive/link/sort。
user-invocable: false
layer: 0
type: contract
---

# Repo Contract（Entity-Level Constitutional Law）

$$\text{RepoContract} = \text{Schema} + \text{DirLaw} + \text{FormulaLaw} + \text{ResearchSkeleton} + \text{VersionLaw} + \text{CacheLaw} + \text{LinkLaw}$$

$$\text{entity}_{repo} = \text{他人開發的開源 repo，我調研 / 參考，判準：Ownership = 他人}$$

$$\text{status} \in \{assess,\; trial,\; adopt,\; hold,\; archived\} \quad \text{（ThoughtWorks Technology Radar）}$$

---

## Schema 律（REPO.md Frontmatter）

$$\text{Frontmatter} = \text{identity} + \text{eval} + \text{location} + \text{tech} + \text{temporal} + \text{version} + \text{branch} + \text{relations}$$

```yaml
name: ""           # repo 顯示名稱
slug: ""           # kebab-case，唯一識別符，對應目錄名
description: ""    # 一句話描述
status: assess     # assess | trial | adopt | hold | archived
url: ""            # 外部 repo URL，必填（GitHub / GitLab / 其他）
stars: 0           # GitHub stars；非 GitHub 時為 0
license: ""        # 授權類型（MIT / Apache-2.0 / GPL-3.0...）
language: []       # 主要程式語言列表
tags: []           # 扁平 tag，不分層
checked_at: ""     # AI 最後排查時間（ISO 8601 日期）
latest_version: "" # flexible string（見 VersionLaw）
latest_released_at: ""  # ISO 8601 日期
tracked_version: "" # 我們目前研究/使用的版本（同 flexible string）
version_lag: null  # 落後版本數；無 tag/release 時為 null
default_branch: "" # 主要分支名稱（統一名稱，非 current_branch）
branches: []       # 所有分支列表
related_projects: []   # [[../../projects/{slug}/PROJECT.md]]
related_repos: []      # [[../{slug}/REPO.md]]
related_tasks: []      # [[../../tasks/{name}/TASK.md]]
related_schedules: []  # [[../../schedule/{period}/TASK.md]]
```

$$\text{欄位存在律}: \forall f \in \text{Frontmatter},\; f \text{ 永遠存在},\; \text{空時} = \{\text{""} \mid [] \mid 0 \mid \text{null}\}$$

$$\Delta_{repo \setminus project} = \{stars,\; license,\; checked\_at,\; tracked\_version,\; version\_lag\}$$

---

## DirLaw 律（目錄結構）

$$\text{Dir}_{repo} = REPO.md + research/ + snapshots/ + \texttt{.cache/}$$

```
.ai-core/repos/{slug}/
├── REPO.md           ← 固定名稱，formula 格式（SKILL.md 同模式）
├── research/         ← *.formula.md（調研報告，依 ResearchSkeleton 生成）
├── snapshots/        ← *.formula.md（特定版本快照，如 v0.3.2.formula.md）
└── .cache/           ← gitignored
    └── code/         ← 實際 clone（非 symlink，區別於 project 的 symlink）
```

$$\text{Scaffold 律}: repo\text{-}create \to \{REPO.md,\; research/,\; snapshots/,\; .cache/\} \text{ 全部建立}$$

$$\text{Archive 律}: repo\text{-}archive \to \texttt{.ai-core/repos/archived/\{slug\}/},\quad \text{Archive} \neq \text{Delete}$$

---

## FormulaLaw 律（格式規範）

$$\text{FormulaLaw}: \text{.ai-core/repos/} \to \text{所有 md 均為 formula 格式，無純 NL 文件}$$

$$REPO.md \parallel SKILL.md: \begin{cases} \text{固定名稱（非 *.formula.md）} \\ \text{內容為 formula 格式（frontmatter + formula body）} \\ \text{無需額外 REPO.formula.md} \end{cases}$$

$$\text{research/*.formula.md + snapshots/*.formula.md}: \text{formula 格式，AI 依骨架建立}$$

---

## ResearchSkeleton 律（調研骨架模板）

$$\text{research} = \underbrace{\text{固定骨架}}_{\text{MECE 覆蓋}} + \underbrace{\text{thought-sphere 填充}}_{\text{深度分析}}$$

`repo-create` 生成 `research/overview.formula.md` 時依此骨架：

```
## 3W 定位
$$\text{3W} = What(\text{做什麼}) + Why(\text{解決何問題}) + How(\text{核心機制})$$

## 場景與市場
$$\text{Market} = \text{目標客戶} + \text{產業} + \text{典型用途} + \text{熱門程度}$$

## 技術棧
$$\text{TechStack} = \text{語言} + \text{框架} + \text{依賴} + \text{運行環境}$$

## 架構分析
[thought-sphere 自由分析：模組劃分、設計模式、擴展點]

## 資料流程
[mermaid 或 formula 描述]

## 使用者操作流程
[mermaid 或 formula 描述]

## API 入口
[主要 class/function/endpoint + 使用範例]

## 交叉比對
[與 .ai-core/projects/ + repos/ 的相符、依賴、競品關係]

## 競品比較
[vs 同類方案]

## 採用決策
$$\text{Decision} = status \in \{assess, trial, adopt, hold\} + \text{理由}$$
```

---

## VersionLaw 律（版本追蹤）

$$\text{latest\_version} = \begin{cases} \text{SemVer tag（如 v0.3.5）} & \exists\;\text{GitHub releases} \\ \text{git tag} & \exists\;\text{tag},\;\nexists\;\text{releases} \\ \text{short SHA（7 位）} & \nexists\;\text{tag} \\ \text{""} & \text{尚未調研} \end{cases}$$

$$version\_lag = \begin{cases} \mathbb{Z}_{\geq 0} & \exists\;\text{tag/release，可計數} \\ null & \nexists\;\text{tag，無法計算} \end{cases}$$

$$\text{repo-update 自動更新}: \{checked\_at,\; latest\_version,\; latest\_released\_at,\; tracked\_version,\; version\_lag,\; default\_branch,\; branches\}$$

更新方式：GitHub API（`/repos/{owner}/{repo}/releases/latest`）或 `git ls-remote --tags`。

---

## CacheLaw 律（.cache 管理）

$$\text{Cache}_{repo}: \texttt{.cache/code/} = \text{實際 clone（非 symlink，區別於 project）}$$

$$\text{repo-code-fetch}: \begin{cases} \nexists\;\texttt{.cache/code/} & \to \texttt{git clone \{url\} .cache/code/} \\ \exists\;\texttt{.cache/code/} & \to \texttt{git -C .cache/code pull} \end{cases}$$

$$\text{保留律}: \texttt{.cache/code/} \text{ 永遠保留，直到 repo-code-clear 手動清除}$$

`.gitignore` 規則：`.ai-core/repos/*/.cache/`

---

## LinkLaw 律（雙向連結）

$$\text{link}(repo, B) \to \begin{cases} B.related\_repos \ni \texttt{[[../../repos/\{slug\}/REPO.md]]} \\ repo.related\_\{type\}s \ni \texttt{[[../../\{type\}s/\{B.slug\}/\{Entry\}.md]]} \end{cases}$$

$$B \in \{project,\; repo,\; task,\; schedule\}$$

---

## δ(RepoContract)：Subagent 傳播摘要

$$\delta(\text{RepoContract}) = \text{Schema}(\text{20 fields}) + \text{Dir}(REPO.md + research + snapshots + .cache) + \text{Formula}(\text{全 formula}) + \text{Skeleton}(\text{10 sections}) + \text{Version}(\text{flexible string} + version\_lag) + \text{Cache}(\text{clone})$$
