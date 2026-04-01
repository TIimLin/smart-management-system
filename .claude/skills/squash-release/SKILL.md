---
name: squash-release
description: Squash merge all WIP commits from the current branch into main with a comprehensive English commit message. Analyzes actual code diff (not WIP commit messages) to summarize changes. Use when the user says "上版", "squash 合併", "壓縮合併", or wants to consolidate WIP commits into a proper release.
argument-hint: "[override-source-branch]"
disable-model-invocation: true
---

# Squash Release

$$\text{SquashRelease} = \text{WIPBranch} \xrightarrow{\text{diff}} \text{SemanticCommit} \to \text{main}$$

$$\text{Release}(src) = \text{Preflight}(src) \to \text{Diff}(src) \to \text{Draft} \to \text{Gate} \to \text{Merge}(src) \to \text{Report}$$

## src 偵測

```
src = $ARGUMENTS | git branch --show-current
(src = main) → ❌ "Already on main. Switch to your working branch first."
```

## Preflight(src)

並行：`git status --porcelain` & `git log main..{src} --oneline`

```
(clean & has_wip) → proceed
~clean            → ❌ "Working tree not clean. Stash or commit first."
~has_wip          → ℹ️ "{src} is already up to date with main."
```

## Diff(src)

並行：`git diff main...{src} --stat` & `git diff main...{src}` & `git log main --oneline -5`

```
diff → classify(add | fix | update | refactor | remove)
```

> WIP commit 訊息（v1/v2/...）為無意義 save point，**不作為歸納依據**，僅分析 diff 內容。

## Draft

載入 `references/commit-format.formula.md` → 依格式規則生成 title + body。

## Gate

$$\text{gate} = \text{Preview} \to \text{approval} \to \text{Merge} \mid \sim\text{approval} \to \text{abort}$$

```
📋 Squash Release Preview
──────────────────────────────────────────
Source:  {src}  ({N} WIP commits)
Target:  main
Diff:    {X} files changed, {Y} insertions(+), {Z} deletions(-)

Commit message:
┌──────────────────────────────────────────
│ {title}
│
│ {body}
└──────────────────────────────────────────
```

**詢問確認後才執行**，若使用者拒絕則完全停止。

## Merge(src)

```bash
git checkout main
git merge --squash {src}
git commit -m "$(cat <<'EOF'
{title}

{body}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

```
~clean_merge → git merge --abort → git checkout {src}
             → ❌ "Merge conflict in: {files}. Aborted."
```

## Report

```
✅ Squash release complete

Source:  {src}  ({N} WIP commits squashed)
Target:  main
Commit:  {short-hash}  {title}

Suggested next steps:
  git push origin main        ← sync to remote
  git branch -d {src}         ← delete source branch (optional)
```
