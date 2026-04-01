---
name: skills-contract
description: >
  AI Core Constitutional Contract M3：Skills 執行元標準。
  定義五大設計律（實體律、命名律、架構律、Formula律、分層律），
  規範所有 Skills 的設計、命名、結構與執行行為。
  Auto-loaded as Layer 0 Constitutional Contract. 所有 session 隱式依賴。
user-invocable: false
layer: 0
type: contract
---

# Skills Contract（M3：執行元標準）

$$M_3: \forall e \in \text{實體},\quad \text{Skills}(e) \supseteq \{create,\; read,\; update,\; archive,\; link,\; sort\},\quad \text{Archive} \neq \text{Delete}$$

$$M_{3.\text{task-前置}}: \forall t \xrightarrow{\text{執行}} \text{task-sort}(t) \to \begin{cases} \text{阻塞} & \to \text{中止} + \text{回報} \\ \neg\text{阻塞} & \to \text{繼續} \end{cases}$$

$$M_{3.\text{agent-前置}}: \forall a \xrightarrow{\text{執行}} \text{agent-sort}(\text{task}) \to \begin{cases} \sim\text{PhaseReady}(a) & \to \text{中止} + \text{回報 Phase Gate} \\ \text{PhaseReady}(a) & \to \text{繼續} \end{cases}$$

---

## 五大設計律

$$\text{Law 1（實體律）}: \forall e \in \text{Entity},\; \text{Skills}(e) \supseteq \{create, read, update, archive, link, sort\}$$

$$\text{Law 2（命名律）}: \text{Name} \in \{entity\text{-}op,\; entity\text{-}role\text{-}name,\; entity\text{-}to/from\text{-}type,\; tool\},\quad archive \neq delete$$

$$\text{Law 3（架構律）}: \text{唯一來源} = \texttt{260301-ai-core-architecture.md},\quad \text{Skill} = \text{SKILL.md} + \text{references/} + \text{scripts/}$$

$$\text{Law 4（Formula律）}: \text{SKILL.md} = \text{Formula Pipeline} + \text{Steps} + \text{Confirm},\quad \text{references/} = \texttt{*.formula.md}$$

$$\text{Law 5（分層律）}: \text{Layer}(s) \in \{0, 1, 2, 3, 4, 5\},\quad \forall s \in \text{Skills}$$

---

## 分層對照

$$\text{Layer 0}: \{*\text{-contract}\} \quad \text{（Constitutional，所有層隱式依賴）}$$

$$\text{Layer 1}: \{note\text{-*},\; memory\text{-*}\} \quad \text{（知識與記憶）}$$

$$\text{Layer 2}: \{task\text{-*},\; schedule\text{-*}\} \quad \text{（計劃層）}$$

$$\text{Layer 3}: \{agent\text{-*},\; workflow\text{-*}\} \quad \text{（協作層）}$$

$$\text{Layer 4}: \{skill\text{-*},\; contract\text{-*}\} \quad \text{（元管理層）}$$

$$\text{Layer 5}: \{note\text{-to/from-*},\; agent\text{-role-*},\; workflow\text{-role-*},\; tools\} \quad \text{（單一功能工具）}$$

---

## 觸發規則（Invocation Contract）

> 依據官方 frontmatter 語義：
> - `disable-model-invocation: true` → **user-only**（描述不進 context，Claude 不知道此 skill 存在，必須使用者 `/skill-name` 叫用）
> - `user-invocable: false` → **AI-only**（不出現在 `/` 選單，只有 Claude 可依 description 匹配自動叫用）
> - 預設（無以上設定） → **雙方皆可**（描述進 context，Claude 可自動叫用，使用者也可 `/skill-name`）

$$\text{Archive} \xrightarrow{\text{disable-model-invocation: true}} \text{user-only} \quad \text{（不可逆封存，AI 不可擅自決定）}$$

$$\text{Sort} \xrightarrow{} \begin{cases} \text{預設（雙方皆可）} & \text{task-sort：M3-task-前置 gate check，AI 自動叫用偵測跨任務阻塞} \\ \text{預設（雙方皆可）} & \text{agent-sort：M3-agent-前置 Phase Gate，AI 自動叫用偵測 phase 依賴} \\ \text{預設（雙方皆可）} & \text{note-sort / memory-sort：quadrant 模式，AI 可叫用進行知識庫優先級排查} \\ \text{disable-model-invocation: true} & \text{其餘 sort（schedule/skill/contract/workflow 等）：純展示，user-only} \end{cases}$$

$$\text{Read} \xrightarrow{\text{預設}} \text{auto} \quad \text{（無副作用，AI 執行前自然先讀，使用者亦可直接叫用）}$$

$$\text{Create/Update/Link} \xrightarrow{\text{預設（視情況）}} \text{雙方皆可} \quad \text{（依 description 觸發詞匹配，Claude 可自動叫用）}$$

$$\text{squash-release} \xrightarrow{\text{disable-model-invocation: true}} \text{user-only} \quad \text{（不可逆 git 操作，user 必須明確觸發）}$$

$$\text{Layer 0 Contracts} \xrightarrow{\text{user-invocable: false}} \text{AI-only} \quad \text{（背景知識，不應出現在使用者 / 選單）}$$

$$\text{Layer 5 agent-role-*} \xrightarrow{\text{user-invocable: false}} \text{AI-only} \quad \text{（角色定義，由 AI 在建立 agent 時自動載入）}$$

---

## δ(M3)：Subagent 傳播摘要

$$\delta(M_3) = \text{Skills}(\text{atomic} \cdot \text{flat}) + \text{task-sort}(\text{M3-task-前置}) + \text{agent-sort}(\text{M3-agent-前置}) + archive \neq delete + \text{Layer}(0\text{-}5)$$
