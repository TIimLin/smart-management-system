---
note_type: formula
source: agent-role-react/SKILL.md
---

# ReAct 操作規範

$$\text{ReActOps} = \text{think} + \text{act} + \text{observe} + \text{terminate}$$

## think — 推理決策

$$\text{think}(\text{task},\; \text{Scratchpad}) \to \text{ReasoningTrace} + \text{ActionDecision}$$

$$= \text{ContextScan}(\text{Scratchpad}) \to \text{PlanStep}(\text{距目標還差什麼？}) \to \text{ToolSelect}(\text{最合適的工具} + \text{args})$$

## act — 接地執行

$$\text{act}(\text{tool},\; \text{args}) \to \text{Obs}$$

$$\text{工具範例}: \text{search} \mid \text{read} \mid \text{write} \mid \text{bash} \mid \text{grep} \mid \text{任何真實可執行工具}$$

$$\text{禁止}: \text{Act}_n \text{ 後由 LLM 憑空補全 Obs 內容}$$

## observe — 回饋注入

$$\text{observe}(\text{Obs}_n) \to \text{Scratchpad.append}(\text{Obs}_n) \to \text{ReadyForThink}_{n+1}$$

$$\text{Scratchpad 過長} \to \text{Summarize}(\text{舊步驟}) + \text{Keep}(\text{最近 5 步} + \text{原始 task})$$

## terminate — 終止決策

$$\text{FinalAnswer}: \text{ReasoningTrace}_n \ni \text{"答案已知"} \to \text{OutputFinal}$$

$$\text{MaxSteps}: n \geq 15 \to \text{OutputBestSoFar} \quad \text{（不可留空）}$$

$$\text{StuckDetect}: \Delta(\text{Act}_{n-2},\; \text{Act}_{n-1},\; \text{Act}_n) = 0 \to \text{ChangeStrategy} \mid \text{OutputBestSoFar}$$

## 與其它角色的定位

$$\text{ReAct}: \text{路徑未知} + \text{需工具接地} + \text{動態適應}$$

$$\text{Planning}: \text{路徑可預知} + \text{需前期分解} + \text{長期任務}$$

$$\text{Execution}: \text{公式已定} + \text{精確實現} + \text{雙向驗證}$$

$$\text{混合}: \text{Planning}(\text{外層分解}) \to \text{ReAct}(\text{每個子任務的內層探索})$$

## react.md 結構

```json
{
  "task": "TASK.md 任務描述",
  "status": "running | converged | max_steps | stuck",
  "step": 1,
  "scratchpad": [
    {"n": 1, "think": "推理內容", "act": "工具 + 參數", "obs": "真實觀察結果"},
    {"n": 2, "think": "...", "act": "...", "obs": "..."}
  ],
  "final_answer": "收斂答案或最佳現有答案"
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [TOOL] Message
[TIMESTAMP] [INFO] [think] [T1] 分析任務，決定第一步：search(X)
[TIMESTAMP] [INFO] [act]   [A1] 執行 search(X)
[TIMESTAMP] [INFO] [obs]   [O1] 獲得結果：...（N chars）
[TIMESTAMP] [INFO] [think] [T2] 根據 O1 調整策略：需進一步 read(Y)
[TIMESTAMP] [INFO] [act]   [A2] 執行 read(Y)
[TIMESTAMP] [INFO] [obs]   [O2] 獲得結果：...
[TIMESTAMP] [INFO] [terminate] FinalAnswer 達成 step=2
```
