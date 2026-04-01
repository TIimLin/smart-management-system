---
note_type: formula
source: agent-role-critic/SKILL.md
---

# Critic 操作規範

$$\text{CriticOps} = \text{extractAssumptions} + \text{attackLoop} + \text{synthesizeVerdict} + \text{terminate}$$

## extractAssumptions — 假設提取

$$\text{extractAssumptions}(A) \to \{a_1, \ldots, a_n\}$$

$$\text{Explicit}(A) = \{a \mid A \text{ 明確聲明 } a \text{ 為前提或條件}\}$$

$$\text{Implicit}(A) = \{a \mid A \text{ 的邏輯需要 } a \text{ 成立才能運作（未明說）}\}$$

$$\text{Contextual}(A) = \{a \mid A \text{ 依賴的外部環境、使用者行為或資源假設}\}$$

**提取觸發問題：**

- 這個方案假設誰會做什麼？
- 如果資源/時間/技術比預期差，這個方案還能運作嗎？
- 這個方案依賴哪些外部系統/人員/流程？
- 有哪些「當然會這樣」但其實可能不成立的前提？

$$\text{禁止}: |\text{Assumptions}| < 3 \to \text{必須深挖，假設 < 3 通常代表提取不完整}$$

## attackLoop — 攻擊循環

$$\text{attackLoop}(\{a_i\}) \to \{(a_i,\; \text{FailureMode}_i,\; \text{Severity}_i)\}$$

每個假設的攻擊三步驟：

$$\text{Step 1}: \text{反例}(a_i) = \text{何種情況下 } a_i \text{ 會失敗？}$$

$$\text{Step 2}: \text{後果}(a_i) = a_i \text{ 失敗後，Artifact 發生什麼？}$$

$$\text{Step 3}: \text{Severity}(a_i) = f(\text{失敗概率},\; \text{影響範圍},\; \text{可修復性})$$

**Severity 評分標準：**

| Severity | 失敗概率 | 影響 | 可修復 |
|----------|---------|------|--------|
| Fatal | 任意 | Artifact 完全失效 | 否 |
| Major | 中高 | 主功能缺失 | 難 |
| Minor | 低 | 品質降低 | 是 |

## synthesizeVerdict — 綜合裁決

$$\text{synthesizeVerdict}(\{(a_i, \text{FM}_i, S_i)\}) \to \text{Verdict}$$

$$\text{Verdict} = \text{FatalList} + \text{MajorList} + \text{MinorList} + \text{OverallJudgment}$$

$$\text{OverallJudgment} = \begin{cases} \text{Block} & |\text{FatalList}| > 0 \\ \text{Revise} & |\text{FatalList}| = 0 \wedge |\text{MajorList}| > 0 \\ \text{Proceed} & |\text{FatalList}| = |\text{MajorList}| = 0 \end{cases}$$

**Verdict 輸出模板：**

```
## 假設清單（{N} 個）
- [E] {explicit assumption}
- [I] {implicit assumption}
- [C] {contextual assumption}

## 攻擊結果

### ❌ Fatal（{N_f} 個）
- {assumption} → 反例: {when} → 後果: {consequence}

### ⚠️ Major（{N_m} 個）
- {assumption} → 反例: {when} → 後果: {consequence}

### 💡 Minor（{N_min} 個）
- {assumption} → 反例: {when} → 後果: {consequence}

## 最終裁決
{Block | Revise | Proceed}
{若 Block：列出必須解決的 Fatal 問題}
{若 Revise：列出優先修正的 Major 問題}
{若 Proceed：記錄 Minor 供後續參考}
```

## terminate — 完成條件

$$\text{Complete} = \text{Verdict 已輸出} \wedge \text{OverallJudgment 明確}$$

$$\text{MaxAssumptions}: |\{a_i\}| \geq 20 \to \text{聚焦 Fatal + Major，Minor 僅列標題}$$

$$\text{TautologyDetect}: \text{連續 3 個攻擊為空洞評論} \to \text{換視角重新 ExtractAssumptions}$$

## critic.md 結構

```json
{
  "artifact": "被批判的 artifact 路徑或名稱",
  "assumptions": {
    "explicit":    ["..."],
    "implicit":    ["..."],
    "contextual":  ["..."]
  },
  "attacks": [
    {
      "assumption":     "...",
      "type":           "explicit|implicit|contextual",
      "counter_example":"...",
      "failure_mode":   "...",
      "severity":       "Fatal|Major|Minor"
    }
  ],
  "verdict": {
    "fatal":    [],
    "major":    [],
    "minor":    [],
    "overall":  "Block|Revise|Proceed",
    "judgment": "..."
  }
}
```

## 日誌格式

```
[TIMESTAMP] [INFO]  [extract]  Explicit: 3, Implicit: 5, Contextual: 2 → Total: 10
[TIMESTAMP] [INFO]  [attack]   a1: {assumption} → Fatal
[TIMESTAMP] [INFO]  [attack]   a2: {assumption} → Major
[TIMESTAMP] [WARN]  [attack]   a3: 攻擊空洞，重新深挖
[TIMESTAMP] [INFO]  [verdict]  Fatal: 1, Major: 3, Minor: 4 → Block
[TIMESTAMP] [INFO]  [complete] critic.md 已寫入
```

## 與其它角色的協作模式

$$\text{3W} \to \text{Critic}: \text{攻擊 3W 的 Why（因果假設）和 How（方法假設）}$$

$$\text{MECE} \to \text{Critic}: \text{攻擊分割空間的邊界定義假設}$$

$$\text{Planning} \to \text{Critic}: \text{主要使用場景，壓力測試實施方案假設}$$

$$\text{Critic} \to \text{SESE}: \text{Critic 找出需解決的問題，SESE 精修修復後的版本}$$

$$\text{Critic} \to \text{Execution}: \text{Proceed 裁決後才允許 Execution 啟動（可選閘道）}$$
