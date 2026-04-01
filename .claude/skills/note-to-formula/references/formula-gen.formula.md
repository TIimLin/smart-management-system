---
note_type: formula
source: note-to-formula/SKILL.md
---

# Formula Generation 規範

$$\text{FormulaGen} = \text{ContentRead} \to \text{CFDSExtract} \to \text{LaTeXEncode} \to \text{Output}$$

## 生成規範

$$\text{語言} = \text{繁體中文} \times \text{LaTeX 數學符號} \times \text{臺灣字詞語法}$$

$$\text{命名} = \begin{cases} \text{大寫} & \text{可運算函數、模組、單位} \\ \text{小寫} & \text{不可拆解的特定值、參數} \end{cases}$$

## 結構模板

```latex
## 核心公式

$$\text{主題} = \text{要素}_1 + \text{要素}_2 \times \text{要素}_3$$

## 展開定義

$$\text{要素}_1 = \text{子概念}_a + \text{子概念}_b$$

## 關係圖

$$\text{輸入} \xrightarrow{\text{處理}} \text{輸出}$$

## 邊界條件

$$(\text{條件成立}) \to \text{結果}_A, \quad \sim \to \text{結果}_B$$
```

## CFDS 萃取

$$\text{CFDSExtract}(\text{主題}) \to C(\text{運算邏輯}) + F(\text{資源結構}) + D(\text{資料模型}) + S(\text{狀態流轉})$$
