---
note_type: formula
source: agent-role-mece/SKILL.md
---

# MECE 操作規範

$$\text{MECEOps} = \text{AxisSelect} + \text{ValidateME} + \text{ValidateCE} + \text{Depth} + \text{Positioning}$$

## AxisSelect — 切割維度選擇

$$\text{AxisSelect}(\Omega) = \arg\max_{\text{axis}} \left( \text{MECE}(\text{axis}) \wedge \text{Insight}(\text{axis}) \right)$$

五大標準切割軸：

$$\text{ProcessAxis}: \Omega \to [\text{Step}_1, \ldots, \text{Step}_n] \quad \text{（流程：起始 → 中間 → 結束的時序分割）}$$

$$\text{ComponentAxis}: \Omega \to [\text{Part}_1, \ldots, \text{Part}_n] \quad \text{（組成：整體的結構性部分）}$$

$$\text{HypothesisAxis}: \Omega \to [\text{Cause}_1, \ldots, \text{Cause}_n] \quad \text{（假設：問題的所有可能原因）}$$

$$\text{DecisionAxis}: \Omega \to [\text{Option}_1, \ldots, \text{Option}_n] \quad \text{（決策：所有可能選項）}$$

$$\text{AttributeAxis}: \Omega \to [\text{Attr}_1, \ldots, \text{Attr}_n] \quad \text{（屬性：特性維度的正交分割）}$$

**Unit-First 原則**（更有洞見的軸選方式）：

$$\text{UnitFirst} = \underbrace{\text{FindAtom}(\Omega)}_{\text{找到 Ω 的最小不可分單位}} \to \underbrace{\text{VariationsOf}(\text{atom})}_{\text{該單位的自然分類}} \to \text{NaturalAxis}$$

先找出問題空間的基本單位 → 分析該單位的變異維度 → 此即最有洞見且最自然的切割軸

## ValidateME — 互斥驗證

$$\text{ValidateME}(\{B_i\}) = \forall\, i \neq j: \text{ask}\left(B_i \cap B_j = \emptyset?\right)$$

$$\text{重疊信號}: \text{某元素 } \omega \text{ 可同時歸入 } B_i \text{ 和 } B_j \to \text{ME violation}$$

$$\text{修復策略} = \begin{cases} \text{merge}(B_i, B_j) & \text{兩者本質相同} \\ \text{sharpen}(\partial B_i, \partial B_j) & \text{邊界模糊，精確化定義} \\ \text{redefine axis} & \text{切割維度本身有語意重疊} \end{cases}$$

## ValidateCE — 窮舉驗證

$$\text{ValidateCE}(\{B_i\}, \Omega) = \text{ask}\left(\exists\, \omega \in \Omega \setminus \bigcup_i B_i?\right)$$

$$\text{盲點信號}: \text{Other / Misc bucket 非空 or 不斷增大} \to \text{CE incomplete}$$

$$\text{修補策略} = \begin{cases} \text{extract}(\text{Other}) \to \text{name}(B_{n+1}) & \text{盲點可被命名} \\ \text{expand boundary}(B_k) & \text{盲點屬於某現有 bucket 的延伸} \\ \text{change axis} & \text{盲點無法被現有軸覆蓋} \end{cases}$$

## Depth 深度規範

$$D_{\max} = \begin{cases} 1 & \text{輕量分析（快速決策、選項列舉）} \\ 2 & \text{標準分析（問題拆解、根因分析）} \\ 3 & \text{深度分析（複雜系統、策略規劃）} \end{cases}$$

$$\text{每層 bucket 數}: 3 \leq |B_i| \leq 7 \quad \text{（超出則合併，不足則細分）}$$

$$\text{不同層可用不同切割軸}: \text{Layer}_1(\text{ComponentAxis}) \to \text{Layer}_2(\text{ProcessAxis})$$

## 與其它角色的定位

$$\text{MECE}: \Omega \text{ 已知邊界} + \text{需完整靜態地圖} + \text{一次分割到位}$$

$$\text{ReAct}: \text{路徑未知} + \text{需工具接地反饋} + \text{動態逐步導航}$$

$$\text{Planning}: \text{任務已知範疇} + \text{需技術工程分解} + \text{有序執行序列}$$

$$\text{混合範例}: \text{MECE}(\text{窮舉所有可能因素}) \to \text{Planning}(\text{針對各因素制定行動})$$

$$\text{混合範例}: \text{MECE}(\text{分割問題空間}) \to \text{ReAct}(\text{在各子空間內動態探索})$$

## mece.md 輸出結構

```json
{
  "task": "TASK.md 任務描述",
  "status": "valid | iterating | fuzzy_delivered | max_iter",
  "axis": "選用的切割維度（ProcessAxis / ComponentAxis / ...）",
  "partition": [
    {
      "id": "B1",
      "name": "bucket 名稱",
      "definition": "精確邊界定義",
      "children": []
    }
  ],
  "validation": {
    "ME": true,
    "CE": true,
    "overlap_notes": [],
    "gap_notes": []
  },
  "depth": 2,
  "iter": 1
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [PHASE]      Message
[TIMESTAMP] [INFO]  [axis]       選擇切割維度：ComponentAxis（理由：...）
[TIMESTAMP] [INFO]  [partition]  生成 bucket：B1=..., B2=..., B3=...
[TIMESTAMP] [INFO]  [ME_check]   B1∩B2=∅ ✓  B1∩B3=∅ ✓  B2∩B3=∅ ✓
[TIMESTAMP] [WARN]  [CE_check]   發現盲點：「...」未被涵蓋 → 新增 B4
[TIMESTAMP] [INFO]  [ME_check]   re-check after B4: all ✓
[TIMESTAMP] [INFO]  [CE_check]   全覆蓋確認 ✓
[TIMESTAMP] [INFO]  [deliver]    MECE valid  depth=2  iter=2  buckets=4
```
