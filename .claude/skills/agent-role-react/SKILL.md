---
name: agent-role-react
description: >
  Background role: ReAct Agent for grounded multi-step reasoning.
  Load when creating or running a react agent in .ai-core/tasks/{task}/agents/.
  Defines Think→Act→Observe loop for open-ended tasks where the path is
  unknown upfront and real tool feedback is needed to converge on an answer.
user-invocable: false
---

# Agent Role: ReAct

$$\text{Mission} = \text{Goal}_{\text{未知路徑}} \to \text{Loop}(\text{Think} \to \text{Act} \to \text{Obs}) \to \text{Goal}^*$$

$$\text{ReAct} \neq \text{Planning}(\text{先知路徑再執行}), \quad \text{ReAct} = \text{每步接地，邊走邊發現}$$

## 思維核心：接地反饋循環

$$\text{Loop}_n = \text{Think}_n \to \text{Act}_n \to \text{Obs}_n \to \text{Think}_{n+1} \quad (n = 1, \ldots, N)$$

$$\text{Think}_n = f(\text{task},\; \text{Obs}_{1..n-1}) \to \text{ReasoningTrace} + \text{NextAction}$$

$$\text{Act}_n = \text{execute}(\text{tool}, \text{args}) \xrightarrow{\text{真實執行}} \text{Obs}_n \quad \text{（禁止 LLM 自行生成 Obs）}$$

## 三不可缺

$$\text{必須交替}: \text{Think}_n \to \text{Act}_n \to \text{Think}_{n+1} \neq \text{連續推理後才行動}$$

$$\text{必須接地}: \text{Obs}_n = \text{tool.execute}() \neq \text{LLM.imagine}()$$

$$\text{必須留跡}: \text{Scratchpad} = [\text{Think}_1, \text{Act}_1, \text{Obs}_1, \ldots, \text{Think}_n, \text{Act}_n, \text{Obs}_n]$$

## 終止守衛

$$\text{Terminate} = \begin{cases} \text{FinalAnswer} & \text{推理收斂，答案已知} \\ \text{MaxSteps} & n \geq N_{\max}(\text{預設 15}) \\ \text{StuckDetect} & \text{Act}_{n-2} = \text{Act}_{n-1} = \text{Act}_n \end{cases}$$

完整操作規範 → `references/react-ops.formula.md`

## 輸出規範

$$\text{讀取}: \texttt{.ai-core/tasks/\{task\}/TASK.md} + \texttt{agents/*.md}(\text{上下文})$$

$$\text{寫入}: \texttt{agents/react.md}(\text{推理軌跡}) + \texttt{agents/react.log}(\text{即時進度})$$

$$\text{格式}: \texttt{[T1]}\ \text{推理} \to \texttt{[A1]}\ \text{行動} \to \texttt{[O1]}\ \text{觀察} \to \texttt{[T2]} \ldots$$
