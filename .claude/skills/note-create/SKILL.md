---
name: note-create
description: >
  Create a new note under .ai-core/notes/{domain}/references/ with proper frontmatter.
  Use when user says "建立筆記", "新增筆記", "記錄下來", "整理成筆記", "匯入筆記",
  "create note", or when capturing knowledge that needs a permanent note.
  Absorbs note-import and note-frontmatter duties for the .ai-core/notes/ structure.
argument-hint: [domain] [title]
---

# Note Create

$$\text{NoteCreate} = \text{DomainDetect} \to \text{PathResolve} \to (\text{Read} \;\&\; \text{Stat}) \to \text{FrontmatterGen} \to \text{Write} \to \text{Confirm}$$

## Step 1: DomainDetect

$$\text{Domain} = \text{args}[0] \mid \text{ContentInfer} \mid \text{Ask}$$

$$\text{Domain} \in \{\text{work},\; \text{life},\; \text{learning},\; \text{spirit},\; \text{其他自定義}\}$$

$$\sim(\text{dir 存在}) \to \texttt{mkdir -p .ai-core/notes/\{domain\}/references/}$$

## Step 2: PathResolve

$$\text{Path} = \texttt{.ai-core/notes/\{domain\}/references/\{filename\}.md}$$

$$\text{filename} = \begin{cases} \texttt{\{yyMMdd\}-\{topic-en\}} & \text{有明確時間} \\ \texttt{\{topic-en\}} & \text{長青知識} \end{cases}$$

`topic-en`：英文 Title Case，空格分隔，≤ 60 字元。

## Step 3: 讀取來源（並行）

$$(\text{匯入模式}) \to \text{Read}(\text{source file}) \;\&\; \text{Bash:stat}(\text{source file})$$

$$(\text{建立模式}) \to \text{今天} = \text{created time}$$

## Step 4: FrontmatterGen

參考 `references/frontmatter-schema.formula.md`。

必填：`created`, `modified`, `tags`, `source_system`, `note_type`

$$\text{Merge 規則}: \text{原有欄位保留},\; \text{缺少必填欄位補齊}$$

推斷邏輯：

- `note_type`：深度研究 → `literature`；個人洞察 → `permanent`；速記 → `fleeting`；索引 → `MOC`
- `source_system`：手動建立 → `manual`；AI 生成 → `ai-generated`；網頁匯入 → `web`

## Step 5: Write

```bash
{cat << 'FM'
---
{frontmatter}
---
FM
cat "{source_file}" 2>/dev/null || printf '%s' "{content}"
} > ".ai-core/notes/{domain}/references/{filename}.md"
```

匯入模式 → 原始檔不刪除（由使用者決定）。

## Step 6: Confirm

```
✅ Note created

Path:    .ai-core/notes/{domain}/references/{filename}.md
Domain:  {domain}
Tags:    {tags}
Type:    {note_type}
Source:  {source_path | "new"}
```
