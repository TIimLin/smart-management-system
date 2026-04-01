---
name: session-find
description: >
  Search OLD Claude Code sessions by prompt content/keyword to retrieve session IDs for
  `claude --resume`. Auto-excludes current session. Use /session-current to get current
  session ID. Use when user says "找 session"、"resume 對話"、"session id"、
  "重開 terminal 找不到"、"Cursor 當掉"，或需要恢復指定 Claude Code 對話。
argument-hint: "[keyword ... | exact phrase | numbered prompt list | --include-self]"
user-invocable: true
layer: 5
type: tool
---

# Session Find

$$\text{SessionFind}(\text{input?}) = \text{InputClassify} \to \text{ProjectResolve} \to \text{SelfExclusion} \to \text{ContentSearch} \to \text{ResultPresent} \to \text{ResumeGuide}$$

## Step 0: InputClassify

$$\text{InputClassify}(\text{input}) = \begin{cases}
\text{含獨立數字行 } \texttt{/\textasciicircum\textbackslash d+\$/m} & \to \text{Mode 1: PromptList} \\
|\text{input}| > 20 \;\lor\; \text{word\_count} > 3 & \to \text{Mode 2: ExactPhrase} \\
\sim & \to \text{Mode 3: Keywords}
\end{cases}$$

$$\text{PromptList} \xrightarrow{\text{strip 數字行}} \text{prompts}[] \xrightarrow{\operatorname{argmax}\,\text{len}} \text{MostDistinctive} \xrightarrow{\text{truncate}[:60]} \text{ExactPhrase}$$

> Mode 1 降維到 Mode 2：取最長 prompt 前 60 字元做精確搜尋。

## Step 1: ProjectResolve

$$\text{folder} = \$\text{PWD.replace}("/",\;"-") \quad \text{（完整替換，含首 "−"，e.g. /home/user/... → -home-user-...）}$$

$$\text{dir} = \texttt{\textasciitilde/.claude/projects/\{folder\}/}$$

$$(\text{dir 不存在}) \to \text{列出 \textasciitilde/.claude/projects/} \to \text{Ask user 確認對應資料夾}$$

## Step 2: SelfExclusion

$$\text{SelfExclusion}(\text{files}) = \begin{cases}
\texttt{--include-self} \in \text{input} & \to \text{files（不過濾）} \\
\sim & \to \text{files} \setminus \left\{\operatorname{argmax}_{\,\text{mtime}}(\text{files})\right\}
\end{cases}$$

> 執行時 mtime 最新的 .jsonl = 當前 session，預設排除，避免當前對話污染搜尋結果。

## Step 3: ContentSearch

$$\text{ContentSearch}(\text{mode},\;\text{target},\;\text{dir}) = \begin{cases}
\text{Mode 1/2: exact} & \to \texttt{grep -F target[:60] dir/*.jsonl} \to \text{files[]} \\
& \quad (\text{no match}) \to \text{python3 json\_decode fallback} \\
\text{Mode 3: keywords} & \to \displaystyle\bigcap_{k}\,\texttt{grep -lF } k \;\texttt{dir/*.jsonl} \to \text{files[]}
\end{cases}$$

```bash
# Mode 1/2
python3 ".claude/skills/session-find/scripts/search.py" "{dir}" --exact "{target[:60]}"

# Mode 3
python3 ".claude/skills/session-find/scripts/search.py" "{dir}" --keywords kw1 kw2 ...
```

## Step 4: ResultPresent

$$\text{files (mtime DESC)} \xrightarrow{\text{for each}} \begin{cases}
\text{session\_id} & = \text{basename}(\text{file},\;".jsonl") \\
\text{snippet} & = \text{首次命中的 user message 前 80 字元}
\end{cases}$$

$$\text{display}: \underbrace{\text{\{rank\}}}_{\text{序號}} \cdot \underbrace{\text{session\_id}}_{\text{UUID}} \mid \underbrace{\text{mtime}}_{\text{⏱}} \mid \underbrace{\text{snippet}_{\leq 80}}_{\text{💬 上下文}}$$

## Step 5: ResumeGuide

$$\text{ResumeGuide} = \begin{cases}
|\text{matches}| = 1 & \to \texttt{claude --resume \{session\_id\}} \\
|\text{matches}| > 1 & \to \text{列表展示} \to \text{user confirm} \to \texttt{claude --resume \{session\_id\}} \\
|\text{matches}| = 0 & \to \text{Alternatives}
\end{cases}$$

$$\text{Alternatives} = \begin{cases}
\texttt{claude --resume} & \text{native 互動 picker（按 session 名稱過濾）} \\
\texttt{claude -c} & \text{continue 當前目錄最近一次 session} \\
\texttt{claude -n "name"} & \text{建議未來命名 session 以利搜尋} \\
\text{換關鍵字重試} & \text{縮短 / 換片段}
\end{cases}$$
