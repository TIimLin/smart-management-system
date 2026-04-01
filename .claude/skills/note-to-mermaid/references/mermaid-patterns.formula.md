# Mermaid Patterns Formula

$$\text{MermaidType} = \text{TypeDetect}(\text{structure}) \to \text{Syntax}$$

## Flowchart

$$\text{使用時機}: \text{線性流程} + \text{決策分支} + \text{A} \to \text{B} \to \text{C 序列}$$

```mermaid
flowchart LR
  A[開始] --> B{判斷}
  B -->|是| C[執行]
  B -->|否| D[跳過]
  C --> E[結束]
```

## Sequence Diagram

$$\text{使用時機}: \text{多主體（系統/人）之間的互動訊息}$$

```mermaid
sequenceDiagram
  participant A as 使用者
  participant B as 系統
  A->>B: 請求
  B-->>A: 回應
```

## Mindmap

$$\text{使用時機}: \text{層次結構} + \text{\#\#/\#\#\# 嵌套} + \text{無橫向流程}$$

```mermaid
mindmap
  root((主題))
    子主題 A
      細節 1
      細節 2
    子主題 B
```

## State Diagram

$$\text{使用時機}: \text{明確狀態名稱} + \text{觸發條件} + \text{狀態機邏輯}$$

```mermaid
stateDiagram-v2
  [*] --> 待機
  待機 --> 執行中: 觸發
  執行中 --> 完成: 成功
  執行中 --> 錯誤: 失敗
  完成 --> [*]
```

## Class Diagram

$$\text{使用時機}: \text{實體 + 屬性 + 關係}（\text{has-a, is-a, uses}）$$

```mermaid
classDiagram
  class Note {
    +string title
    +string domain
    +create()
  }
  class Memory {
    +string topic
    +Date created
  }
  Note "1" --> "*" Memory : links
```
