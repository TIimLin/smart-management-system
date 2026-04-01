# 常用 Formula Patterns

## CRUD Pattern

$$\text{CRUD}(\text{entity}) = \text{Create} + \text{Read} + \text{Update} + \text{Archive}$$

$$\text{Create}: \text{DomainDetect} \to \text{PathResolve} \to \text{FrontmatterGen} \to \text{Write} \to \text{Confirm}$$

$$\text{Read}: \text{QueryParse} \to \text{Search} \to \text{Rank} \to \text{Display}$$

$$\text{Update}: \text{TargetResolve} \to (\text{Read} \;\&\; \text{Stat}) \to \text{ModeDetect} \to \text{MergeWrite} \to \text{Confirm}$$

$$\text{Archive}: \text{TargetConfirm} \to \text{ArchivePath} \to \text{Move} \to \text{Confirm}$$

## Link Pattern

$$\text{Link}(A, B) = \text{Exist}(A) \;\&\; \text{Exist}(B) \to A \xleftrightarrow{} B$$

$$\text{雙向連結}: A.\text{related} \mathrel{+}= [[B]], \quad B.\text{related} \mathrel{+}= [[A]]$$

## Sort Pattern

$$\text{Sort}(\text{entities}) = \text{List} \to \text{Classify}(\text{key}) \to \text{Display}(\text{sorted})$$

$$\text{key} = \text{date} \mid \text{domain} \mid \text{tags} \mid \text{relevance} \mid \text{status}$$

## Observe → Think → Act Pattern

$$\text{OTA}(\text{input}) = \text{Observe}(\text{input}) \to \text{Think}(\text{formula}) \to \text{Act}(\text{output}) \to \text{Observe}(\text{feedback})$$

## Guard Pattern（前置條件）

$$(pre\text{-}condition) \to \text{Execute},\quad \sim(pre\text{-}condition) \to \text{Stop}(\text{reason})$$

## Parallel Fetch Pattern

$$\text{ParallelFetch} = A \;\&\; B \;\&\; C \text{（同一 round trip 完成多個獨立讀取）}$$

## Index Update Pattern

$$\text{IndexUpdate}(\text{MEMORY.md} \mid \text{TASKLIST.json}) = \text{Read} \to \text{Append}(\Delta) \to \text{Write}$$

## Path Resolution Pattern

$$\text{Path}(\text{entity}) = \text{BaseDir} + \text{Classifier} + \text{Timestamp?} + \text{TopicName} + \text{.ext}$$

範例：

$$\text{memory} = \texttt{.formula/memory/\{yyMMdd\}/\{hhmmss\}-\{topic\}.md}$$

$$\text{note} = \texttt{.formula/notes/\{domain\}/references/\{yyMMdd\}-\{topic\}.md}$$

$$\text{task} = \texttt{.formula/tasks/\{task-name\}/TASK.md}$$
