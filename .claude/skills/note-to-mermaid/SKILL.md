---
name: note-to-mermaid
description: >
  Convert a markdown note to Mermaid diagram syntax, saved as SAME-NAME
  .mermaid.md in the SAME directory as the source. Auto-detects diagram type.
  Trigger when user says "mermaid", "轉成圖表", "畫流程圖", "畫架構圖",
  "diagram", "流程圖版", "*.mermaid.md", "sequence diagram",
  or when designing a workflow before implementation.
argument-hint: [filepath | keyword]
disable-model-invocation: false
---

# Note To Mermaid

$$\text{NoteToMermaid} = \text{SourceResolve} \to \text{CheckExisting} \to \text{TypeDetect} \to \text{MermaidGen} \to \text{Write} \to \text{Confirm}$$

## Step 1: SourceResolve

$$\text{Source} = \text{args} \mid \text{note-read}(\text{keyword}) \mid \text{Ask}$$

$$\text{OutputPath} = \text{source.dir} / \text{source.stem} + \texttt{.mermaid.md}$$

範例：`references/API Design.md` → `references/API Design.mermaid.md`（同目錄、同名）

## Step 2: CheckExisting

$$(\texttt{*.mermaid.md} \text{ 已存在}) \to \text{詢問：覆蓋或跳過？}$$

## Step 3: TypeDetect

參考 `references/mermaid-patterns.formula.md` 的完整語法規範。

$$\text{Type} = \begin{cases} \text{flowchart} & \text{線性流程、決策分支（A→B→C, if/else）} \\ \text{sequenceDiagram} & \text{多主體互動（角色 + 動詞 + 箭頭）} \\ \text{mindmap} & \text{層次結構（\#\#/\#\#\# 嵌套，無橫向流程）} \\ \text{stateDiagram-v2} & \text{明確狀態名稱 + 轉換條件} \\ \text{classDiagram} & \text{實體 + 屬性 + 關係（has-a, is-a）} \end{cases}$$

$$(\text{結構混合或無法判斷}) \to \text{flowchart LR 為預設}$$

## Step 4: MermaidGen

- 節點命名使用 source 中的原始術語
- 中文 label 保留繁體
- 保持與 source 相同的語意結構和層次

## Step 5: Write

```markdown
---
created: {今天 ISO 8601 +08:00}
modified: {今天 ISO 8601 +08:00}
note_type: formula
source: {source_filepath}
diagram_type: {detected_type}
---

\`\`\`mermaid
{generated mermaid syntax}
\`\`\`
```

## Step 6: Confirm

```
✅ Mermaid diagram created

Source:  {source_path}
Output:  {same_dir}/{stem}.mermaid.md
Type:    {diagram_type}
```
