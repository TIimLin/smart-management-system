---
note_type: formula
source: agent-role-planning/SKILL.md
---

# Planning 四大思維工具

$$\text{PlanningOps} = \text{analyze} + \text{interpret} + \text{transform} + \text{validate}$$

## analyze — 將一切轉成公式

$$\text{analyze}(\text{any\_input}) \to \text{MathFormula}$$

$$= \text{CFDSExtract}(\text{input}) \to \text{PatternRecognize}(\text{CFDSComponents}) \to \text{FormulaGenerate}$$

## interpret — 將公式轉成解釋

$$\text{interpret}(\text{MathFormula}) \to \text{NaturalExplanation}$$

$$= \text{FormulaParse} \to \text{SemanticExtract}(\text{intent} + \text{significance} + \text{value}) \to \text{LanguageGenerate}$$

## transform — 將公式轉成公式

$$\text{transform}(\text{FormulaA} + \text{Operation} + \text{FormulaB}) \to \text{OptimizedFormula}$$

$$= \text{OperatorMastery} \to \text{FormulaManipulate} \to \text{OptimizationEngine}(\text{minimal\_complexity} \times \text{maximum\_effectiveness})$$

## validate — 驗證實作符合公式

$$\text{validate}(\text{MathFormula}) \to \text{StructuralReport}$$

$$= \text{SyntaxValidation}(\text{cfds\_completeness} + \text{operator\_correctness}) \to \text{SemanticVerification} \to \text{StructuralAnalysis}$$

## 狀態記錄

$$\text{updateLog}(\text{Event}, \text{level}, \text{Context}) \to \texttt{planning.log}$$

$$\text{updateJson}(\text{Data}, \texttt{planning.md}) \to \text{持久化狀態}$$

## planning.md 結構

```json
{
  "business_increment": "TASK.md 業務增量",
  "EngineeringStages": ["stage1", "stage2"],
  "current_stage_index": 0,
  "WorkflowFormula": "StageProcess -> QualityGates",
  "ImplementationFormula": "TechStack × SystemDesign × CodeStructure",
  "ExecutionGuide": "自然語言執行指導",
  "completion_status": "stage_complete | stage_continue | cross_stage_alert"
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [TOOL] Message
[TIMESTAMP] [INFO] [analyze] 分析 TASK.md 為 StageRequirements
[TIMESTAMP] [INFO] [transform] 將需求轉換為 EngineeringStages 序列
[TIMESTAMP] [INFO] [analyze] 分析當前階段為 WorkflowFormula
[TIMESTAMP] [INFO] [transform] 生成 ImplementationFormula
[TIMESTAMP] [INFO] [interpret] 產生 ExecutionGuide
[TIMESTAMP] [INFO] [validate] 驗證階段完成狀態 → {stage_complete | stage_continue | cross_stage_alert}
```
