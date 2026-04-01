# CFDS 基底系統

## 核心公理

$$\text{任何系統} = f(C, F, D, S)$$

$$C = \text{Code} = \text{可執行邏輯（函數、類別、模組、Skills 指令）}$$

$$F = \text{Files} = \text{配置與資源（設定檔、模板、*.formula.md）}$$

$$D = \text{Data} = \text{資料結構（JSON, YAML, schema, frontmatter）}$$

$$S = \text{State} = \text{運行狀態（索引、快取、當前任務進度）}$$

## 量化關係

$$\text{系統規模} = C_n + F_m + D_p + S_q \quad (n, m, p, q \geq 1)$$

## 分解公理

$$\text{複雜系統} = \Sigma(\text{簡單組件})$$

$$\text{分解終止條件}: \text{組件} = C + F + D + S$$

$$\text{分解原則} = \text{單一職責} + \text{最小介面} + \text{認知可控}$$

## 組合公理

$$\text{組合} = \text{基本單位} \to \text{複雜系統}$$

$$\text{組合驗證} = \text{介面一致} + \text{依賴滿足} + \text{功能完整}$$

## AI Core 的 CFDS 映射

$$C = \text{Skills（SKILL.md 的執行邏輯）}$$

$$F = \text{references/*.formula.md（公式化知識定義）}$$

$$D = \text{.formula/notes/ + .formula/memory/ + .formula/tasks/（知識與狀態資料）}$$

$$S = \text{MEMORY.md + TASKLIST.json（運行狀態索引）}$$

## AI Core 分層架構

$$\text{Layer 0}: \text{formula-contract} \text{（根基，所有 Skills 隱式依賴）}$$

$$\text{Layer 1}: \text{note-*} + \text{memory-*} \text{（知識與記憶，最常用）}$$

$$\text{Layer 2}: \text{task-*} + \text{agent-*} \text{（任務執行，開發時使用）}$$

$$\text{Layer 3}: \text{schedule-*} + \text{skill-*} \text{（管理層，偶爾使用）}$$

$$\text{Layer 4}: \text{squash-release} + \text{未來工具} \text{（Dev Ops，按需使用）}$$
