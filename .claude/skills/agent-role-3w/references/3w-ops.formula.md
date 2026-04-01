---
note_type: formula
source: agent-role-3w/SKILL.md
---

# 3W 操作規範

$$\text{3WOps} = \text{what} + \text{why} + \text{how} + \text{mode} + \text{complete}$$

## what — 現象定義

$$\text{what}(\text{topic}) \to \text{Definition} + \text{Facts} + \text{KeyFactors}$$

$$= \text{Define}(\text{邊界明確：是什麼・不是什麼}) \to \text{Observe}(\text{可驗證的事實與數據}) \to \text{Identify}(\text{主要因素 + 次要因素})$$

**What 三不可**：

$$\text{禁止}: \text{Define} = \text{模糊描述（如「效率變低」）} \quad \Rightarrow \text{改為}: \text{具體量化（如「響應時間超過 3s」）}$$

$$\text{禁止}: \text{Observe} = \text{主觀感受} \quad \Rightarrow \text{改為}: \text{可觀察的事實}$$

$$\text{禁止}: \text{Identify} = \text{遺漏主因} \quad \Rightarrow \text{搭配 MECE 確保窮盡}$$

## why — 因果理解

$$\text{why}(\text{Definition},\; \text{Facts}) \to \text{Cause} + \text{Purpose} + \text{Impact}$$

$$= \text{Cause}(\text{根本原因，非表象}) \to \text{Purpose}(\text{為何存在・驅動動機}) \to \text{Impact}(\text{直接效應 + 間接效應})$$

**Why 三不可**：

$$\text{禁止}: \text{Cause} = \text{循環解釋（如「因為效率低所以慢」）} \quad \Rightarrow \text{追問 5 Whys 到底層}$$

$$\text{禁止}: \text{Purpose} = \text{空缺（跳過動機直接談方案）} \quad \Rightarrow \text{必須回答「為誰・為何・有何意義」}$$

$$\text{禁止}: \text{Impact} = \text{只看直接影響} \quad \Rightarrow \text{追蹤第二階・第三階效應}$$

## how — 方法行動

$$\text{how}(\text{Cause},\; \text{Purpose}) \to \text{Strategy} + \text{Action} + \text{Validate}$$

$$= \text{Strategy}(\text{方向選擇 + 資源配置}) \to \text{Action}(\text{具體步驟 + 時間表 + 負責人}) \to \text{Validate}(\text{驗收指標 + 回饋機制})$$

**How 三不可**：

$$\text{禁止}: \text{Strategy} = \text{空想方向（無資源依據）} \quad \Rightarrow \text{必須評估可行性}$$

$$\text{禁止}: \text{Action} = \text{模糊計劃（如「盡快改善」）} \quad \Rightarrow \text{改為具體可執行的行動項}$$

$$\text{禁止}: \text{Validate} = \text{缺席} \quad \Rightarrow \text{每個 How 必須有驗收標準}$$

## mode — 模式選擇

$$\text{ModeSelect}(\text{context}) = \begin{cases} \text{分析模式}: \text{What} \to \text{Why} \to \text{How} & \text{已有現象，需理解原因與解法} \\ \text{設計模式}: \text{Why} \to \text{How} \to \text{What} & \text{已有目的，需定義方法與產物} \end{cases}$$

**判準**：

$$\text{input} = \text{「現象・問題・狀況」} \Rightarrow \text{分析模式}$$

$$\text{input} = \text{「目標・實現・願景」} \Rightarrow \text{設計模式}$$

## complete — 完整性守衛

$$\text{Validate3W} = \text{Check}(\text{What}) \land \text{Check}(\text{Why}) \land \text{Check}(\text{How})$$

$$\text{Check}(W_i) = \begin{cases} \text{pass} & W_i \neq \emptyset \;\land\; W_i \neq \text{假設/空想/循環} \\ \text{fail} & \text{otherwise} \end{cases}$$

$$\text{fail}(W_i) \Rightarrow \text{DeepDive}(W_i) \to \text{Revalidate}$$

## 與其它角色的定位

$$\text{3W}: \text{理解分析} + \text{認知完整性} + \text{深度洞察}$$

$$\text{ReAct}: \text{路徑未知} + \text{工具接地} + \text{動態適應}$$

$$\text{Planning}: \text{路徑可知} + \text{任務分解} + \text{長期規劃}$$

$$\text{MECE}: \text{範疇窮盡} + \text{互斥分類} + \text{無盲點}$$

**協作公式**：

$$\text{3W}(\text{理解問題}) \to \text{Planning}(\text{分解任務}) \to \text{ReAct}(\text{動態執行})$$

$$\text{3W What 層} \xrightarrow{\text{穿插}} \text{MECE（窮盡關鍵要素）}$$

## 3w.md 結構

```json
{
  "task": "TASK.md 任務描述",
  "mode": "analytical | design",
  "status": "in-progress | complete",
  "what": {
    "definition": "明確定義（邊界清晰）",
    "facts": ["可驗證事實 1", "可驗證事實 2"],
    "key_factors": ["主因 1", "次因 1"]
  },
  "why": {
    "root_cause": "根本原因（非表象）",
    "purpose": "目的動機（為誰・為何）",
    "impact": {
      "direct": "直接效應",
      "indirect": "間接效應"
    }
  },
  "how": {
    "strategy": "方向選擇與資源配置",
    "actions": ["行動步驟 1（負責人・時間）", "行動步驟 2"],
    "validation": "驗收指標與回饋機制"
  }
}
```

## 日誌格式

```
[TIMESTAMP] [LEVEL] [LAYER] Message
[TIMESTAMP] [INFO] [mode]  選定分析模式：analytical（輸入為現象）
[TIMESTAMP] [INFO] [what]  定義邊界：...
[TIMESTAMP] [INFO] [what]  識別關鍵要素：...
[TIMESTAMP] [INFO] [why]   根本原因：...（非循環解釋）
[TIMESTAMP] [INFO] [why]   目的動機：...
[TIMESTAMP] [INFO] [how]   策略方向：...
[TIMESTAMP] [INFO] [how]   行動步驟：...（具體可執行）
[TIMESTAMP] [INFO] [complete] 完整性驗證通過，3W 分析收斂
```
