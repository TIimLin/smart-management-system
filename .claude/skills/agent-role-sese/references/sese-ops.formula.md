---
note_type: formula
source: agent-role-sese/SKILL.md
---

# SESE 操作規範

$$\text{SESEOps} = \text{setObj} + \text{scan}_{4D} + \text{resolveParadox} + \text{refine} + \text{terminate}$$

## setObj — 目標設定

$$\text{setObj}(A) \to \text{Objective}$$

$$= \text{ArtifactType}(A) \to \text{IntendedPurpose} \to \text{SuccessCriteria}$$

$$\text{若 Objective 模糊}: \text{Ask}(\text{這個產物的核心目的是？讀者是誰？期望達成什麼？})$$

$$\text{禁止}: \text{在 Objective 不明確時繼續 Scan}_{4D}$$

## scan₄D — 四維掃描

$$\text{scan}_{4D}(A, \text{Obj}) \to \{I_S,\, I_E,\, I_{Sys},\, I_{Exh}\}$$

### Simple 掃描

$$I_S = \{e \in A \mid \text{Complexity}(e) > \text{NecessaryComplexity}(e, \text{Obj})\}$$

$$\text{問}: \text{這個部分可以更簡單表達而不失語意？有無冗長描述？有無多餘抽象層？}$$

### Effective 掃描

$$I_E = \{e \in A \mid \neg\, \text{Serves}(e, \text{Obj})\}$$

$$\text{問}: \text{這個部分是否直接服務於 Objective？有無偏題、重複、無效內容？}$$

### Systematic 掃描

$$I_{Sys} = \{(e_i, e_j) \in A \times A \mid \text{StructuralInconsistency}(e_i, e_j)\}$$

$$\text{問}: \text{命名一致嗎？格式統一嗎？方法可重現嗎？結構可預測嗎？}$$

### Exhaustive 掃描

$$I_{Exh} = \text{Domain}(\text{Obj}) \setminus \text{Coverage}(A)$$

$$\text{問}: \text{有哪些關鍵面向未被覆蓋？有無盲點？讀者會提出哪些未回答的問題？}$$

## resolveParadox — 悖論解決

$$\text{resolveParadox}(I_S, I_{Exh}) \to \text{CriticalCoverage}$$

$$\text{Step 1}: \text{列出} I_{Exh} \text{（必須補充的盲點）}$$

$$\text{Step 2}: \text{列出} I_S \text{中與} I_{Exh} \text{衝突的部分（加了 Exhaustive 就不 Simple）}$$

$$\text{Step 3}: \text{CriticalCoverage} = \{c \in I_{Exh} \mid \text{Impact}(c) \geq \theta_{\text{critical}}\}$$

$$\text{Step 4}: \text{對 CriticalCoverage 中每項，找最小表達方式（保持 Simple 約束）}$$

$$\text{Pareto 判準}: \text{覆蓋 80\% 理解的 20\% 結構 = CriticalCoverage 的決策依據}$$

## refine — 精修輸出

$$\text{refine}(A, \{I_S, I_E, I_{Sys}, I_{Exh}\}, \text{CriticalCoverage}) \to A^*$$

$$A^* = A - I_E - I_S(\text{非 critical}) + \text{CriticalCoverage} + \text{StructuralFix}(I_{Sys})$$

$$\text{優先順序}: \text{Effective（刪除偏題）} \to \text{Systematic（修正結構）} \to \text{Exhaustive（補充盲點）} \to \text{Simple（精簡表達）}$$

## terminate — 完成條件

$$\text{Complete} = A^* \text{ 已輸出} \wedge \text{SESEScore}(A^*) > \text{SESEScore}(A)$$

$$\text{MaxIter}: n \geq 3 \to \text{輸出當前最佳 } A^* + \text{說明未解決的 trade-offs}$$

$$\text{FuzzyDomain}: \theta_{\text{critical}} \text{ 不明確} \to \text{標注假設後交付}$$

## 與其它角色的協作模式

$$\text{ReAct}: \text{路徑未知} + \text{需工具接地} \quad \text{SESE}: \text{ReAct 輸出的品質審計}$$

$$\text{MECE}: \text{空間分割完整性} \quad \text{SESE}: \text{整體產物的 Systematic + Exhaustive 閘道}$$

$$\text{混合}: \text{Planning} \to \text{SESE}(\text{公式品質閘) \to \text{Execution} \to \text{SESE}(\text{程式品質閘}$$

## sese.md 結構

```json
{
  "target": "被審計的 artifact 路徑或描述",
  "objective": "這個 artifact 要達成的目的",
  "audit": {
    "simple":      { "score": 0, "issues": [], "recommendations": [] },
    "effective":   { "score": 0, "issues": [], "recommendations": [] },
    "systematic":  { "score": 0, "issues": [], "recommendations": [] },
    "exhaustive":  { "score": 0, "issues": [], "recommendations": [] }
  },
  "paradox_points": [
    { "tension": "描述 Simple↔Exhaustive 衝突點", "resolution": "CriticalCoverage 決策" }
  ],
  "critical_coverage": ["必須保留的最小覆蓋集"],
  "refined_artifact": "A* 的完整內容或路徑"
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [STEP] Message
[TIMESTAMP] [INFO] [setObj]         Objective: 審計 planning.md，確保業務增量描述 SESE
[TIMESTAMP] [INFO] [scan_simple]    發現 3 處冗長描述（lines 12, 24, 38）
[TIMESTAMP] [INFO] [scan_effective] 發現 1 處偏離主題（line 44）
[TIMESTAMP] [INFO] [scan_systematic] 命名不一致：Formula vs formula（lines 5,19）
[TIMESTAMP] [INFO] [scan_exhaustive] 缺少：錯誤處理場景覆蓋
[TIMESTAMP] [INFO] [resolveParadox] CriticalCoverage 決定：補充錯誤處理，壓縮 3 處冗長
[TIMESTAMP] [INFO] [refine]         A* 輸出完成，SESE score: 6→8
[TIMESTAMP] [INFO] [terminate]      Complete，sese.md 已寫入
```
