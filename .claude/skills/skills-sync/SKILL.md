---
name: skills-sync
description: >
  Sync skills from a source project into the target project.
  Overwrites matching skills (src ∩ dst), copies source-only skills (src \ dst),
  preserves target-only skills (dst \ src).
  Trigger when user says "同步 skills", "skills sync", "蓋掉 skills", "更新 skills 目錄".
argument-hint: "[target-skills-path] [source-skills-path]"
user-invocable: true
layer: 5
type: tool
disable-model-invocation: false
---

# Skills Sync

$$\text{SkillsSync} = \text{PathResolve} \to \text{DirDiff} \to \text{SyncPlan} \to \text{Gate} \to \text{Execute} \to \text{Report}$$

## PathResolve

$$\text{src} = \text{args}[1] \mid \texttt{/mnt/c/Users/user/Documents/Yippine/Program/Knowledge-Castle/.claude/skills}$$
$$\text{dst} = \text{args}[0] \mid \texttt{.claude/skills}(\text{cwd})$$
$$(\text{src} \nexists \lor \text{dst} \nexists) \to \text{Ask}$$

## DirDiff

$$\text{Overlap} = \text{Skills}(\text{src}) \cap \text{Skills}(\text{dst})$$
$$\text{SrcOnly} = \text{Skills}(\text{src}) \setminus \text{Skills}(\text{dst})$$
$$\text{DstOnly} = \text{Skills}(\text{dst}) \setminus \text{Skills}(\text{src}) \quad \text{（保留不動）}$$

## SyncPlan

```
🔄  覆寫技能 (src → dst)：{|Overlap|}  skills
➕  新增技能 (src-only)：  {|SrcOnly|}  skills
🔒  保留技能 (dst-only)：  {|DstOnly|}  skills
```

## Gate

$$\text{gate} = \text{Preview} \to \text{approval} \to \text{Execute} \mid \sim\text{approval} \to \text{abort}$$

顯示 SyncPlan 完整清單，**詢問確認後才執行**（覆寫技能為破壞性操作）。

## Execute

$$\forall s \in \text{Overlap}: \text{rm -rf}(dst/s) \to \text{cp -r}(src/s,\; dst/)$$
$$\forall s \in \text{SrcOnly}: \text{cp -r}(src/s,\; dst/)$$

## Report

```
✅ Skills sync complete
src: {src}
dst: {dst}

🔄 覆寫技能：{Overlap list}
➕ 新增技能：{SrcOnly list}
🔒 保留技能：{DstOnly list}
```
