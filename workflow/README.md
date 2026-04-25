# workflow

Project workflow automation — file consistency sweeps and cross-repo synchronization.

## Install

```bash
claude plugin install workflow@hebstr
```

## Skills

| Skill | Invocation | Purpose |
|---|---|---|
| [`sync-files`](./sync-files/) | `/sync-files` &nbsp;·&nbsp; `/sync-files --deep` | Scan all files in the current directory and subdirectories, identify ones that are stale relative to recent changes, and update them. `--deep` runs a cross-repo semantic consistency scan with parallel agents. |

## Modes

- **Default** (`/sync-files`) — single-repo sweep. Detects drift between recently changed files and the rest of the tree (counts, references, doc tables, permission/config gates) and proposes targeted updates.
- **Deep** (`/sync-files --deep`) — cross-repo semantic scan. Spawns parallel agents to check consistency between sibling repos sharing concepts (shared docs, shared manifests, mirrored APIs).

User-invocable only — does not auto-trigger.

## Requirements

[Claude Code](https://claude.com/claude-code) with plugin marketplaces enabled.
