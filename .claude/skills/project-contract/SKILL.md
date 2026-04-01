---
name: project-contract
description: >
  AI Core Entity Contract Layer 0：project 實體憲法。
  定義 PROJECT.md schema、目錄結構律、formula 格式律、version 追蹤律、.cache symlink 律。
  Single source of truth for all project-* skills。
  Auto-loaded by project-create/read/update/archive/link/sort。
user-invocable: false
layer: 0
type: contract
---

# Project Contract（Entity-Level Constitutional Law）

$$\text{ProjectContract} = \text{Schema} + \text{DirLaw} + \text{FormulaLaw} + \text{VersionLaw} + \text{CacheLaw} + \text{LinkLaw}$$

$$\text{entity}_{project} = \text{己方主導的構想 / 規劃 / 實作，判準：Ownership = 我}$$

---

## Schema 律（PROJECT.md Frontmatter）

$$\text{Frontmatter} = \text{identity} + \text{status} + \text{location} + \text{tech} + \text{temporal} + \text{version} + \text{branch} + \text{relations}$$

```yaml
name: ""           # 專案顯示名稱
slug: ""           # kebab-case，唯一識別符，對應目錄名
description: ""    # 一句話描述
status: idea       # idea | planning | active | shipped | archived
url: ""            # 己方 GitHub repo URL；無 repo 時為 ""
local_path: ""     # 本機 repo 絕對路徑；無時為 ""
language: []       # 主要程式語言列表
tags: []           # 扁平 tag，不分層
created: ""        # ISO 8601 日期（YYYY-MM-DD）
latest_version: "" # flexible string：SemVer tag / git tag / null
latest_released_at: ""  # ISO 8601 日期
total_releases: 0  # GitHub releases 數量；無時為 0
default_branch: main    # 主要分支名稱（統一名稱，非 current_branch）
branches: []       # 所有分支列表
related_projects: []    # [[../../projects/{slug}/PROJECT.md]]
related_repos: []       # [[../../repos/{slug}/REPO.md]]
related_tasks: []       # [[../../tasks/{name}/TASK.md]]
related_schedules: []   # [[../../schedule/{period}/TASK.md]]
```

$$\text{欄位存在律}: \forall f \in \text{Frontmatter},\; f \text{ 永遠存在},\; \text{空時} = \{\text{""} \mid [] \mid 0 \mid \text{null}\}$$

$$\text{Card 律}: \text{所有欄位永遠存在} \Rightarrow \text{web card 元件可無條件解構 frontmatter}$$

---

## DirLaw 律（目錄結構）

$$\text{Dir}_{project} = PROJECT.md + plans/ + research/ + \texttt{.cache/}$$

```
.ai-core/projects/{slug}/
├── PROJECT.md        ← 固定名稱，formula 格式（SKILL.md 同模式）
├── plans/            ← *.formula.md（PRD、架構、roadmap）
├── research/         ← *.formula.md（技術調研筆記）
└── .cache/           ← gitignored
    └── code          ← symlink → local_path（project-code-link 建立）
```

$$\text{Scaffold 律}: project\text{-}create \to \{PROJECT.md,\; plans/,\; research/,\; .cache/\} \text{ 全部建立}$$

$$\text{Archive 律}: project\text{-}archive \to \texttt{.ai-core/projects/archived/\{slug\}/},\quad \text{Archive} \neq \text{Delete}$$

---

## FormulaLaw 律（格式規範）

$$\text{FormulaLaw}: \text{.ai-core/projects/} \to \text{所有 md 均為 formula 格式，無純 NL 文件}$$

$$PROJECT.md \parallel SKILL.md: \begin{cases} \text{固定名稱（非 *.formula.md）} \\ \text{內容為 formula 格式（frontmatter + formula body）} \\ \text{無需額外 PROJECT.formula.md} \end{cases}$$

$$\text{plans/*.formula.md + research/*.formula.md}: \text{formula 格式，AI 在骨架內自由建立}$$

---

## VersionLaw 律（版本追蹤）

$$\text{latest\_version} = \begin{cases} \text{SemVer tag（如 v1.2.3）} & \exists\;\text{GitHub releases} \\ \text{git tag} & \exists\;\text{tag},\;\nexists\;\text{releases} \\ \text{short SHA（7 位）} & \nexists\;\text{tag} \\ \text{""} & \text{尚無版本} \end{cases}$$

$$\text{project-update 自動更新}: \{latest\_version,\; latest\_released\_at,\; total\_releases,\; default\_branch,\; branches\}$$

更新方式：讀取 `local_path` 的 git 資訊（`git tag --sort=-creatordate`、`git branch`）。

---

## CacheLaw 律（.cache 管理）

$$\text{Cache}_{project}: \texttt{.cache/code} = symlink \to local\_path$$

$$\text{project-code-link}: \begin{cases} local\_path \neq \text{""} & \to \texttt{ln -sf \{local\_path\} .ai-core/projects/\{slug\}/.cache/code} \\ local\_path = \text{""} & \to \text{跳過，待設定後再呼叫} \end{cases}$$

$$\text{保留律}: \texttt{.cache/} \text{ 永遠保留，直到 project-code-link --reset 重置}$$

`.gitignore` 規則：`.ai-core/projects/*/.cache/`

---

## LinkLaw 律（雙向連結）

$$\text{link}(project, B) \to \begin{cases} B.related\_projects \ni \texttt{[[../../projects/\{slug\}/PROJECT.md]]} \\ project.related\_\{type\}s \ni \texttt{[[../../\{type\}s/\{B.slug\}/\{Entry\}.md]]} \end{cases}$$

$$B \in \{project,\; repo,\; task,\; schedule\}$$

---

## δ(ProjectContract)：Subagent 傳播摘要

$$\delta(\text{ProjectContract}) = \text{Schema}(\text{20 fields}) + \text{Dir}(PROJECT.md + plans + research + .cache) + \text{Formula}(\text{全 formula}) + \text{Version}(\text{flexible string}) + \text{Cache}(\text{symlink})$$
