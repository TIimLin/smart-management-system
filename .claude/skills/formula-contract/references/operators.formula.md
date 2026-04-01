# CFDS 運算符完整定義

## 基礎運算符

$$+ = \text{功能擴展}: A + B \text{（將 B 加入 A）}$$

$$- = \text{功能移除}: A - B \text{（從 A 移除 B）}$$

$$\times = \text{強依賴}: A \times B \text{（A 與 B 強耦合，缺一不可）}$$

$$\div = \text{模組化}: A \div B \text{（將 A 分解為 B 個部分）}$$

$$= = \text{等價替換}: A = B \text{（A 與 B 功能等價）}$$

$$() = \text{優先控制 + 條件表達}: (A + B) \times C, \quad (condition) \to action$$

## 流程運算符

$$\to = \text{執行順序}: A \to B \text{（執行 A 後執行 B）}$$

$$\Rightarrow = \text{依賴關係}: A \Rightarrow B \text{（A 依賴於 B）}$$

$$\leftrightarrow = \text{雙向連結}: A \xleftrightarrow{} B \text{（雙向關聯）}$$

## 邏輯運算符

$$| = \text{互斥選擇}: A \mid B \text{（選 A 或 B，不可同時）}$$

$$\& = \text{並行同時}: A \;\&\; B \text{（A 與 B 並行執行）}$$

$$\sim = \text{邏輯否定 / 剩餘情況}: \sim(condition), \;\sim \to \text{default}$$

## 高階運算符

$$\Sigma = \text{求和 / 遍歷}: \Sigma(\text{entities})$$

$$\partial = \text{增量變化}: \partial A / \partial B \text{（A 相對 B 的變化率）}$$

$$\circ = \text{函數組合}: f \circ g \circ h = h \to g \to f$$

$$\surd = \text{提取抽象}: \surd(A, B, C) \text{（提取 ABC 公共部分）}$$

$$\int = \text{整合統一}: \int(A, B, C) \text{（將 ABC 整合為系統）}$$

## 優先級（高 → 低）

$$1.() \quad 2.\circ \quad 3.\surd\int\partial \quad 4.\times\div \quad 5.+- \quad 6.\Rightarrow \quad 7.\to \quad 8.\&| \quad 9.\sim$$

## 命名慣例

$$\text{大寫} = \text{可運算或拆解的函數、模組、單位（如 NoteCreate, DomainDetect）}$$

$$\text{小寫} = \text{不可拆解的特定內容值、參數（如 domain, topic, tags）}$$
