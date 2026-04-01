---
note_type: formula
source: agent-role-execution/SKILL.md
---

# Execution 雙向驗證規範

$$\text{BiValidate} = \text{forward}(\text{Formula} \to \text{Code}) \times \text{reverse}(\text{Code} \to \text{Formula})$$

## 偏差計算

$$\text{deviation\_score} = \frac{|\text{CurrentFormula} \triangle \text{TargetFormula}|}{|\text{TargetFormula}|} \in [0, 1]$$

$$(\text{deviation\_score} > \text{threshold}) \to \text{重新融合}$$

## 融合公式結構

$$\text{FusionFormula} = \Delta C + \Delta F + \Delta D + \Delta S$$

$$\Delta C = \text{新增/修改函數},\quad \Delta F = \text{新增/修改配置},\quad \Delta D = \text{資料結構變更},\quad \Delta S = \text{狀態轉移調整}$$

## execution.md 結構

```json
{
  "continuation_status": "new_start | resume",
  "current_formula": "映射的專案公式",
  "project_type": "greenfield | brownfield | legacy",
  "fusion_formula": "PreciseOperations -> InjectionPoints",
  "compliance_score": 0.0,
  "pass_status": "pass | fail",
  "acceptance_status": {
    "test_results": "all_passed | partial | failed",
    "final_status": "complete | incomplete"
  }
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [TOOL] Message
[TIMESTAMP] [INFO] [analyze] 從 planning.md 提取執行需求
[TIMESTAMP] [INFO] [analyze->transform] 映射專案為 CurrentFormula
[TIMESTAMP] [INFO] [transform->validate] deviation_score: {n}
[TIMESTAMP] [INFO] [transform->validate] 生成 FusionFormula
[TIMESTAMP] [INFO] [transform->validate] 實現完成 compliance_score: {n}
[TIMESTAMP] [INFO] [validate] 測試驗收完成 status: complete
```
