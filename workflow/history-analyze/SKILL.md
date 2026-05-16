---
name: history-analyze
description: Use when the user asks about shell efficiency, missing aliases, typing patterns, "what do I type too much", or workflow optimization based on their command history. Also triggered by direct invocation `/workflow:history-analyze`.
allowed-tools: Bash, Read, Edit
disable-model-invocation: true
---

# history-analyze

Analyze `~/.bash_history` for repeated patterns, missing aliases, recurring typos, and tool-upgrade opportunities. Propose concrete additions to the user's shell config.

## Trust boundary

Raw history must never reach the API. All history access goes through `scripts/sanitize-bash-history.sh`, which strips sensitive lines (credentials, tokens, env vars, connection strings, `.env` reads) and emits an abstracted frequency table. This skill must invoke that script as the only reader of `~/.bash_history`; never `cat`/`head`/`tail`/`Read` the history file directly.

If the sanitizer script is missing or has been modified since last use (`git status` shows changes), stop and ask the user to review before running.

## Workflow

### Step 1 — Run the sanitizer

```sh
~/Documents/pro/packages/claude-code-plugins/workflow/history-analyze/scripts/sanitize-bash-history.sh ~/.bash_history 10000
```

The script emits two sections:
- **Command frequency** (top 80, arguments abstracted)
- **Repeated multi-command chains** (alias/function candidates, args stripped)

If the output is empty or fails, surface the error and stop.

### Step 2 — Identify findings

From the frequency table, group findings by category:

| Category | Trigger | Action |
|---|---|---|
| Missing alias | command pattern used >20 times with same first arg (e.g. `git commit`) | Propose alias in `~/dotfiles/bash/.bashrc` or `~/dotfiles/bash/.bash_aliases` |
| Repeated chain | `cmd1 && cmd2` or `cmd1 | cmd2` >3 times | Propose shell function (allows args + early exit) |
| Recurring typo | command appears with edit distance ≤2 from a known command (e.g. `claude --resmue`) >1 time | Note for awareness; propose abbreviation alias only if user confirms |
| Tool-upgrade opportunity | legacy tool used while a modern replacement is in `rules/environment.md` (e.g. `find` while `fdfind` is available, `grep` while `rg` is available) | Propose habit shift, not blanket aliasing |

### Step 3 — Present, rank, await approval

Output the findings as a numbered list, ranked by estimated time savings (commands_per_week × seconds_saved_per_invocation). For each:
- Pattern observed and frequency
- Proposed alias/function/habit shift
- Target file path
- Estimated impact

Do not write to shell config files without explicit user approval per-finding.

### Step 4 — Apply approved changes

For approved aliases/functions, edit the appropriate stow-managed file under `~/dotfiles/bash/`. Resolve symlinks first (`readlink -e`) — never write through `~/.bashrc` directly. After editing, remind the user to `source ~/.bashrc` or open a new shell.

## Calibration

- Threshold of 20 occurrences for "missing alias" is a starting point. Adjust down for niche commands the user uses sparingly but consistently; adjust up for one-off bursts.
- Don't propose aliases for commands already aliased — grep `~/dotfiles/bash/.bashrc` first.
- Don't propose habit shifts for tools the user has explicitly rejected (check `CLAUDE.md` and `~/.claude/memory/`).
- Recurring typos are interesting signal even when below the 20-occurrence bar; surface them once.

## Notes

- The sanitizer's `SENSITIVE_PATTERNS` array is exhaustive for credentials but not infallible. If the user reports a leak, add the pattern there and re-run.
- The sanitizer skips `HISTTIMEFORMAT` timestamp lines (`^#[0-9]+`) and blank lines. Bash with `HISTCONTROL=ignoreboth` already de-dupes adjacent commands, so frequency counts reflect distinct invocations.
- Multi-line history entries (rare in bash; common in zsh) are not handled — the format here is one-command-per-line.
