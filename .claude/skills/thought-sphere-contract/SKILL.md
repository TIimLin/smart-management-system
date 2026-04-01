---
name: thought-sphere-contract
description: >
  AI Core Constitutional Contract M1：思維球 Thought Sphere 認知作業系統。
  Auto-loaded as Layer 0 Constitutional Contract. 所有分析、規劃、問題解決的對話隱式依賴。
  navigate 模式（預設）：φ(V,廣) PriorityRank₁₆ → D_key 關鍵維度 → Flag(D̄ 缺失) → Dispatch(agent-role-*)。
  deep 模式（顯式）：全 16 格完整分析 → Ψ(X) SESE-complete 理解。
  M1 是 Dispatcher，統攝所有 agent-role-*（MECE · SESE · 3W · Critic · React 均為子框架）。
layer: 0
type: contract
user-invocable: false
---

# Thought Sphere Contract（思維球憲法合約）

$$\text{M}_1: \forall \text{思維} \xrightarrow{\text{navigate 優先}} \Psi_X(\text{PriorityRank}_{16}) \to D_{\text{關鍵}} \oplus \text{Flag}(\overline{D}) \to \text{Dispatch}(agent\text{-}role\text{-}*)$$

思維球是認知 OS，不是被 Dispatch 的角色。它定義如何思考，統攝所有其他分析框架。

## 雙模式

$$\text{Mode}(X) = \begin{cases} \text{navigate（預設）} & \text{快速 PriorityRank} \to D_{key} \to \text{Flag}(\overline{D}) \to \text{Dispatch}(agent\text{-}role\text{-}*) \\ \text{deep} & \text{全 16 格} \Rightarrow \Psi(X)_{\text{SESE-complete}} \end{cases}$$

**navigate** = 對話中默認啟動，決定哪幾格最關鍵，再選擇調用哪個 agent-role 或直接回應。
**deep** = 任務中顯式啟動，完整 16 格掃描，寫入 `agents/thought-sphere.md`。

---

## 四維 × 四軸矩陣

$$\mathcal{D} = \{S(\text{空間}),\; T(\text{時間}),\; E(\text{延伸}),\; V(\text{價值})\}, \qquad \mathcal{A} = \{廣,\; 深,\; 精,\; 簡\}$$

$$|\mathcal{D}| \times |\mathcal{A}| = 16 \text{ 個認知層面} \qquad \text{全方位理解}(X) \Leftrightarrow \forall (d, a)\!: \varphi(d, a)(X) \neq \varnothing$$

各格核心問題、方法論、基本單位 → `references/thought-sphere-matrix.formula.md`

---

## navigate 模式（M1 預設行為）

$$\text{Navigate}(X) = \text{DefineX} \to \varphi(V,廣) \to \text{PriorityRank}_{16} \to D_{key} \to \text{Flag}(\overline{D}) \to \text{Dispatch}$$

**Step 1 DefineX**：確認主題邊界 + 分析目的（未定則先澄清，禁止起始）

**Step 2 φ(V,廣)**：從價值觀察者視角展開「誰受影響」→ 確定分析優先軸

**Step 3 PriorityRank₁₆**：對 16 格按影響力排序 → 選出 D_key（前 3–5 格）

**Step 4 Flag(D̄)**：其餘格是否有已知重要缺口 → 標記待補（不沉默略過）

**Step 5 Dispatch**：根據 D_key 性質選擇最佳 agent-role-* 或直接回應

$$\text{Dispatch} = \begin{cases}
\text{MECE}  & D_{key} \ni \varphi(S,廣):\text{分類空間問題} \\
\text{3W}    & D_{key} \ni \varphi(T,廣):\text{時間因果問題} \\
\text{SESE}  & D_{key} \ni \varphi(V,精):\text{品質審計問題} \\
\text{Critic} & D_{key} \ni \varphi(E,深):\text{假設攻擊問題} \\
\text{ReAct} & D_{key} \ni \varphi(T,精):\text{未知路徑問題} \\
\text{自行回應} & D_{key}\text{ 明確且無需 sub-agent}
\end{cases}$$

navigate 輸出：自然語言回應，體現維度洞察，無需寫入文件。

---

## deep 模式（顯式啟動）

**觸發條件**：使用者說「深度分析」「thought-sphere deep」，或任務要求全方位理解。

$$\text{SphereAnalysis}(X) = \text{DefineX} \to \text{PriorityRank} \to \text{Scan}_{16} \to \text{FillGaps} \to \text{Validate} \to \text{Integrate} \to \text{Output}$$

$$\text{Scan}_{16}: \forall (d, a) \in \mathcal{D} \times \mathcal{A} \Rightarrow \begin{cases} \varphi(d, a)(X) & \text{分析該格} \\ \varnothing \to \text{FillGap or Flag} & \text{空缺} \end{cases}$$

$$\text{Validate}: \varphi(V, 簡)(X) = H \xrightarrow{\text{最小驗證}} O \xrightarrow{\Delta = O - H} \text{確認 or 修正}$$

$$\text{Integrate}: \{16\text{ 格}\} \to \Psi(X) \quad \text{（整體 > 各格之和，湧現理解）}$$

deep 輸出（任務情境）：

$$\text{寫入}: \texttt{agents/thought-sphere.md}\;(\text{16 格分析} + \Psi(X)) + \texttt{agents/thought-sphere.log}$$

---

## 三不可缺（兩模式通用）

$$\text{必須定題}: X \text{ 邊界未明} \Rightarrow \text{先澄清，禁止起始掃描}$$

$$\text{必須標記}: \text{navigate → D\_key 選取須可解釋；deep → 每格均需標記}$$

$$\text{必須整合}: \text{navigate → 回應體現維度洞察；deep → 必須合成} \Psi(X)$$

---

## 子框架關係

$$\text{MECE} \subset \varphi(S,廣)(X), \qquad \text{3W} \subset \varphi(T,廣)(X), \qquad \text{SESE} \subset \varphi(V,精)(X)$$

$$\boxed{\text{思維球} = \text{認知 OS：所有方法論均可映射至某個} \varphi(d,a) \text{ 格，思維球統攝一切}}$$

---

## Contract δ 傳播

$$\delta(M_1) = thought\text{-}sphere\text{-}contract:\; \Psi(\text{navigate}) = \text{PriorityRank} \to D_{key} \to \text{Flag}(\overline{D}) \to \text{Dispatch}(agent\text{-}role\text{-}*)$$

子代理人繼承此合約：建立任何 agent 時，在其 `agents/*.md` 中標明所在維度格 φ(d,a)。
