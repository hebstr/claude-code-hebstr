# hebstr

Claude Code skills and plugins by hebstr.

## Install

```bash
claude plugin marketplace add hebstr/claude-code-hebstr
```

Then install plugins individually:

```bash
claude plugin install <plugin>@hebstr
```

## Plugins

### `review`

Code, skill, and MCP review workflows.

| Skill | Purpose |
|---|---|
| `review-walkthrough` | Interactive, point-by-point walkthrough of any review report |
| `full-review` | Full-coverage project review with parallel specialist agents |
| `blindspot-review` | Circularity-aware orchestrator that adds cross-model judging via OpenRouter |
| `skill-adversary` | Adversarial critic for Claude Code skills |
| `mcp-adversary` | Adversarial critic for MCP servers |

```bash
claude plugin install review@hebstr
```
