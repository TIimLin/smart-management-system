---
name: formula-contract
description: >
  Load when interpreting formula notation (→ × ~ & | Σ ∂ ∘ √ ∫), reading *.formula.md files,
  or executing any AI Core Skill. Provides CFDS operator semantics, Observe→Think→Act loop,
  and formula patterns used across all AI Core operations.
user-invocable: false
disable-model-invocation: false
---

# Formula Contract

$$\text{AI Core} = \text{Formula}(\text{極簡精確}) \times \text{Skills}(\text{按需載入}) \times \text{Notes}(\text{原子扁平})$$

## Observe → Think → Act 循環

$$\text{OTA} = \text{Observe}(\text{input}) \to \text{Think}(\text{formula 推導}) \to \text{Act}(\text{執行輸出}) \to \text{Observe}(\text{回饋})$$

每個 Skill 執行都遵循此循環：感知輸入 → 用 formula 推導決策 → 執行並回饋。

## Operator 速查

| 符號 | 語義 | 範例 |
|------|------|------|
| `→` | 執行順序 | `A → B → C` |
| `×` | 強依賴 / 組合 | `A × B` |
| `+` | 並列 | `A + B` |
| `()` | 分組 / 條件 | `(cond) → A, ~ → B` |
| `~` | 否定 / else | `~(found) → default` |
| `&` | 並行同時 | `A & B` |
| `\|` | 互斥選擇 | `A \| B` |
| `Σ` | 總和 / 遍歷 | `Σ(items)` |
| `∂` | 增量 | `∂(state)` |
| `∘` | 函數組合 | `f ∘ g` |

完整定義 → `references/operators.formula.md`

## CFDS 基底

$$\text{任何系統} = f(C, F, D, S)$$

$$C = \text{Code},\quad F = \text{Files},\quad D = \text{Data},\quad S = \text{State}$$

完整定義 → `references/cfds.formula.md`

## 常用 Patterns

→ `references/patterns.formula.md`
