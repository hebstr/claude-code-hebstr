# workflow

Project workflow automation — file consistency sweeps and cross-repo synchronization.

## Install

```bash
claude plugin install workflow@hebstr
```

## Skills

| Skill | Invocation | Purpose |
|---|---|---|
| [`sync`](./sync/) | `/sync` | Scan all files in the current directory and subdirectories, identify ones that are stale relative to recent changes, and update them. Always runs a cross-repo semantic consistency scan with parallel agents. |

## What it does

`/sync` performs a single-repo sweep (drift between recently changed files and the rest of the tree — counts, references, doc tables, permission/config gates) followed by a cross-repo semantic scan (parallel agents check consistency between sibling repos sharing concepts: shared docs, shared manifests, mirrored APIs).

User-invocable only — does not auto-trigger.

## Requirements

[Claude Code](https://claude.com/claude-code) with plugin marketplaces enabled.
