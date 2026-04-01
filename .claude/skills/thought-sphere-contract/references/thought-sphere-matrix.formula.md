---
note_type: formula
source: agent-role-thought-sphere/SKILL.md
---

# 思維球 16 格完整矩陣

$$\mathbf{M}_{4 \times 4} = \begin{pmatrix}
\varphi(S,廣) & \varphi(S,深) & \varphi(S,精) & \varphi(S,簡) \\[4pt]
\varphi(T,廣) & \varphi(T,深) & \varphi(T,精) & \varphi(T,簡) \\[4pt]
\varphi(E,廣) & \varphi(E,深) & \varphi(E,精) & \varphi(E,簡) \\[4pt]
\varphi(V,廣) & \varphi(V,深) & \varphi(V,精) & \varphi(V,簡)
\end{pmatrix}$$

---

## 維度定義

$$S\;(\text{空間}) \triangleq \text{靜態結構性存在} \Rightarrow \text{「它是什麼？長什麼樣？」}$$

$$T\;(\text{時間}) \triangleq \text{動態演化過程} \Rightarrow \text{「它如何變化？何時發生？」}$$

$$E\;(\text{延伸}) \triangleq \text{關係互動網絡} \Rightarrow \text{「它與誰相關？如何影響？」}$$

$$V\;(\text{價值}) \triangleq \text{觀察者評估 + 驗證} \Rightarrow \text{「它值得嗎？如何確認？誰來判斷？」}$$

## 軸定義

$$廣 \triangleq \text{MECE 橫向窮舉（不重複、不遺漏）}$$

$$深 \triangleq \text{垂直縱向穿透（從表層到不可再分的底層）}$$

$$精 \triangleq \text{本質提煉（去噪，保留核心真理）}$$

$$簡 \triangleq \text{奧卡姆壓縮（最少元素表達最多資訊）}$$

---

## S 維度（空間）：靜態結構

### φ(S, 廣) — 空間 × 廣

$$\varphi(S, 廣) = \bigcup_{i=1}^{n} 類別_i, \quad 類別_i \cap 類別_j = \varnothing, \quad i \neq j$$

| | 內容 |
|---|---|
| 核心問題 | 「這個主題能分成哪些互不重疊、完全覆蓋的類別？」 |
| 核心方法 | MECE 分類、心智圖橫向發散、同心圓分層 |
| 基本單位 | **最小獨立分類單元**（不可再合併） |
| 子框架 | → `agent-role-mece`（嚴格分類邏輯） |

### φ(S, 深) — 空間 × 深

$$\varphi(S, 深) = \text{主題} \to \text{範圍} \to \text{項目} \to \text{概念} \to \text{原子（不可再分）}$$

| | 內容 |
|---|---|
| 核心問題 | 「這個概念的最底層構成要素是什麼？」 |
| 核心方法 | 層次分解（Hierarchical Decomposition）、知識圖譜 |
| 基本單位 | **最小不可分的概念原子**（Atomic Concept） |

### φ(S, 精) — 空間 × 精

$$\varphi(S, 精) = \text{現象} \xrightarrow{\text{提煉}} \text{概念} \xrightarrow{\text{提煉}} \text{本質} \xrightarrow{\text{提煉}} \text{公理}$$

| | 內容 |
|---|---|
| 核心問題 | 「去掉一切表象，最底層的真理是什麼？」 |
| 核心方法 | 第一性原理（First Principles）、奧卡姆剃刀 |
| 基本單位 | **最核心的不可再化簡的本質命題** |

### φ(S, 簡) — 空間 × 簡

$$\varphi(S, 簡) = \arg\min_{\mathcal{M}} |\mathcal{M}|, \quad \text{s.t. } \mathcal{M} \text{ 覆蓋所有本質資訊}$$

| | 內容 |
|---|---|
| 核心問題 | 「用最少的概念，如何完整描述這個事物的結構？」 |
| 核心方法 | 最小描述長度（MDL）、費曼技術 |
| 基本單位 | **最精簡的完整模型** |

---

## T 維度（時間）：動態演化

### φ(T, 廣) — 時間 × 廣

$$\varphi(T, 廣) = \underbrace{W_h(\text{過去}) \times W_t(\text{現在}) \times H(\text{未來})}_{3W} \cup \underbrace{\text{因} \times \text{緣} \times \text{果}}_{\text{因緣果}} \cup \underbrace{\{\text{成住壞空}\}}_{\text{生命週期}}$$

| | 內容 |
|---|---|
| 核心問題 | 「這個事物的完整時間軌跡是什麼？」 |
| 核心方法 | 3W 分析法、因緣果、生命週期模型（生老病死 / 成住壞空 / 生住異滅） |
| 基本單位 | **最小有意義的時間階段**（Atomic Stage） |
| 子框架 | → `agent-role-3w`（時間廣度的結構化展開） |

### φ(T, 深) — 時間 × 深

$$\varphi(T, 深) = \text{主題} \to \text{計畫} \to \text{任務} \to \text{步驟（SOP）} \to \text{最小可執行動作}$$

| | 內容 |
|---|---|
| 核心問題 | 「要實現這個目標，最細緻的操作步驟是什麼？」 |
| 核心方法 | WBS（工作分解結構）、SOP 設計、GTD |
| 基本單位 | **最小可執行步驟**（Atomic Action） |
| 子框架 | → `agent-role-planning`（業務需求 → 技術階段 → SOP） |

### φ(T, 精) — 時間 × 精

$$\varphi(T, 精) = \text{手段}_n \xrightarrow{\text{追溯}} \text{手段}_{n-1} \xrightarrow{\text{追溯}} \cdots \xrightarrow{\text{追溯}} \text{終極目的（不可再問）}$$

| | 內容 |
|---|---|
| 核心問題 | 「剝去所有手段，最根本的動力來源是什麼？」 |
| 核心方法 | 5 個為什麼（5 Whys）、目的樹、動機追溯 |
| 基本單位 | **最終不可再追問的終極目的** |

### φ(T, 簡) — 時間 × 簡

$$\varphi(T, 簡) = \arg\min_{\text{週期}} \text{步驟數}, \quad \text{s.t. 涵蓋完整演化邏輯}$$

| | 內容 |
|---|---|
| 核心問題 | 「描述這個事物演化的最簡時間模型是什麼？」 |
| 核心方法 | PDCA（最簡閉環）、MVP、Lean Cycle |
| 基本單位 | **最短有效閉環週期** |

---

## E 維度（延伸）：關係網絡

### φ(E, 廣) — 延伸 × 廣

$$\varphi(E, 廣) = \bigcup_{(A,B) \in \mathcal{P}^2,\, A \neq B} \text{關係}(A, B) \cup \text{比較矩陣（同異優缺）}$$

| | 內容 |
|---|---|
| 核心問題 | 「所有相關端點是什麼？完整關係網絡為何？」 |
| 核心方法 | 生態圖、利益相關者映射、同異優缺法則 |
| 基本單位 | **最小關係對** $A \leftrightarrow B$ |

### φ(E, 深) — 延伸 × 深

$$\varphi(E, 深) = \text{表層互動} \to \text{結構互動} \to \text{利益互動} \to \text{根本依賴（深層本質）}$$

| | 內容 |
|---|---|
| 核心問題 | 「兩個端點之間，最深層的互動機制是什麼？」 |
| 核心方法 | 系統動力學、Porter 五力、因果迴路圖 |
| 基本單位 | **一層互動深度**（每深一層揭示更多隱藏聯繫） |

### φ(E, 精) — 延伸 × 精

$$\varphi(E, 精) = \arg\max_{v \in \mathcal{V}} \text{影響力}(v), \quad \text{影響力}(v) = f(\text{規模}, \text{稀缺性}, \text{可接觸性})$$

| | 內容 |
|---|---|
| 核心問題 | 「誰/什麼是這個生態中最關鍵的槓桿點？」 |
| 核心方法 | 帕累托分析、圖論中心性、關鍵路徑法 |
| 基本單位 | **最具影響力的核心端點（槓桿點）** |

### φ(E, 簡) — 延伸 × 簡

$$\varphi(E, 簡) = \text{MST}(\mathcal{V}, \mathcal{E}) \Rightarrow \text{最小生成樹：核心生態骨架}$$

| | 內容 |
|---|---|
| 核心問題 | 「用最少的端點和關係，如何完整描述這個生態？」 |
| 核心方法 | 最小生成樹（MST）、核心三角模型 |
| 基本單位 | **最核心 N 個端點及其必要關係** |

---

## V 維度（價值）：觀察者評估與驗證

$$\boxed{V = \text{Valuation（評估）} \oplus \text{Validation（驗證）}: \text{不可分，是同一銅幣的正反面}}$$

### φ(V, 廣) — 價值 × 廣 【元導航格：決定其他格的優先順序】

$$\varphi(V, 廣) = \bigsqcup_{o \in \mathcal{O}} \text{視角}_o, \quad \mathcal{O} = \{\text{個人} \cup \text{組織} \cup \text{社會} \cup \text{未來世代}\}$$

| | 內容 |
|---|---|
| 核心問題 | 「這件事對所有相關觀察者而言分別有什麼意義？有哪些視角被遺漏？」 |
| 核心方法 | 利益相關者映射、六頂帽思考法、德菲法 |
| 基本單位 | **最小獨立觀察者單元** $(o)$：持有不可化約視角的評估主體 |
| 特殊職責 | **PriorityRank**：根據 $\mathcal{O}$ 窮舉結果決定其餘 15 格的掃描優先順序 |

### φ(V, 深) — 價值 × 深

$$\varphi(V, 深) = v_{\text{表層}} \xrightarrow{\text{追溯}} v_{\text{工具}} \xrightarrow{\text{追溯}} v_{\text{終端}} \xrightarrow{\text{追溯}} v_{\text{本體}}\;(\text{意義感 / 幸福感})$$

| | 內容 |
|---|---|
| 核心問題 | 「剝去所有工具性價值，最終在追求什麼？」 |
| 核心方法 | Value Laddering、馬斯洛垂直穿透、意義療法（Frankl） |
| 基本單位 | **一層價值深度**（手段到目的的每一級跳躍） |

### φ(V, 精) — 價值 × 精

$$\varphi(V, 精) = c^* = \arg\max_{c \in \mathcal{C}} \frac{\text{決策影響力}(c)}{\text{標準數量}} \quad \text{（元標準：統攝所有次級標準）}$$

| | 內容 |
|---|---|
| 核心問題 | 「若只能保留一個評估標準，最能代表真正意圖的是哪一個？」 |
| 核心方法 | OKR 的 O 提取、ROI 主軸分析、決策矩陣加權 |
| 基本單位 | **元標準** $c^*$：能統攝所有次級標準的最核心判斷依據 |
| 子框架 | → `agent-role-sese`（品質審計即是 V 精的執行層） |

### φ(V, 簡) — 價值 × 簡 【驗證格：確認整體分析正確性】

$$\varphi(V, 簡) = \text{最小完整驗證迴路}: H \xrightarrow{\text{行動}} O \xrightarrow{\Delta = O - H} \begin{cases} |\Delta| < \varepsilon & \Rightarrow H \text{ 成立} \\ |\Delta| \geq \varepsilon & \Rightarrow H \text{ 修正} \end{cases}$$

| | 內容 |
|---|---|
| 核心問題 | 「用最少的資源和步驟，如何確認這個分析是正確的？」 |
| 核心方法 | MVP 驗證、A/B 測試、PDCA、Lean Startup Build-Measure-Learn |
| 基本單位 | **最小驗證週期**：能確認或否定一個假設的最短完整迴路 |
| 特殊職責 | **Validate**：掃描完成後，用此格驗證整體分析 $\Psi(X)$ 是否正確 |

---

## 跨框架映射表

| 格 | 業界框架 |
|---|---|
| φ(S,廣) | McKinsey MECE、心智圖 |
| φ(S,深) | 知識圖譜、Ontology |
| φ(S,精) | 第一性原理（Aristotle/Musk）、蘇格拉底問答 |
| φ(S,簡) | 費曼技術、MDL |
| φ(T,廣) | 3W、PEST、因緣果、生老病死/成住壞空 |
| φ(T,深) | WBS、GTD、Agile Sprint |
| φ(T,精) | Toyota 5 Whys、目的樹 |
| φ(T,簡) | PDCA、Lean MVP |
| φ(E,廣) | 利益相關者映射、生態圖 |
| φ(E,深) | 系統動力學、Porter 五力 |
| φ(E,精) | 帕累托、圖論中心性 |
| φ(E,簡) | 最小生成樹、核心三角 |
| φ(V,廣) | 六頂帽、多視角分析、德菲法 |
| φ(V,深) | 馬斯洛、Value Laddering、Frankl 意義療法 |
| φ(V,精) | OKR、KPI 精簡化、決策矩陣 |
| φ(V,簡) | Lean Startup、A/B、科學方法 |

---

## 基本單位完整對照

$$\text{空間基本單位} = \text{概念原子}:\quad \text{最小不可分的知識單元}$$

$$\text{時間基本單位} = \text{事件原子}:\quad \text{最小有意義的時間轉變點}$$

$$\text{延伸基本單位} = \text{關係對}:\quad A \leftrightarrow B,\; A \neq B$$

$$\text{價值基本單位} = \text{評估四元組}:\quad (o, s, c, t) = \text{觀察者} \times \text{對象} \times \text{標準} \times \text{時間點}$$

$$\boxed{\text{AI Core CRUD+Link+Sort} \leftrightarrow \text{思維球原子化}:\quad \text{Sort} \leftrightarrow V(\text{以 }(o,s,c,t)\text{ 評估即是排序})}$$
