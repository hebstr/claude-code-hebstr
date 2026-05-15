# Changelog

## [audit 0.2.1] - 2026-05-15

### `audit`

#### Changed

- `walkthrough`: broaden circularity-check trigger in the orchestrator. Detection is now artifact-driven and reviewer-agnostic — any `SKILL.md`, any `*.md` under an `agents/` directory, any target inside `~/.claude/` or a plugin install, and any MCP tool-definition target now nudge toward `/blindspot`. Previously, `SKILL.md` reviewed by a non-skill-tool reviewer (e.g. `critical-code-reviewer`) would silently bypass the nudge, because the condition was gated by `reviewer.category == skill-tool`. The principle: circularity comes from the artifact being Claude-interpreted at runtime, not from which reviewer was chosen. Default response stays `[y/N]` to avoid chaining costly cross-model audits by inertia.
- `blindspot`: append an explicit `### Next step` block to both report templates (cross-model success and fallback). The block names the exact command — `/audit:walkthrough` with no arguments — and states what the walkthrough will do with the report (bucket-aware L2 routing in cross-model mode, standard L2 in fallback mode). Closes the loop: previously the report could land in the conversation with no instruction on how to consume it, leaving Claude to recall the chained command from `CLAUDE.md` — not always reliable across long sessions.

## [0.4.0] - 2026-05-12

### `workflow`

#### Added

- `reco`: deep-mode recommendation backed by external sources. Spawns two parallel agents (official documentation via WebFetch, community practice via WebSearch), then synthesizes a structured recommendation with verified citations (my take, tradeoffs, official docs, community, final recommendation). URLs are verified before citing; source disagreement is surfaced, not papered over. Light-mode recommendations (always recommend when presenting choices) live in CLAUDE.md as a communication rule, not in this skill. Explicit-invocation only (`/workflow:reco`).

## [0.3.0] - 2026-04-30

### `workflow`

#### Added

- `continue`: flush durable facts to memory, update `.claude/PLAN.md`, and print a minimal continuation prompt. No handoff document is written — PLAN.md and memory are the authoritative stores. Explicit-invocation only (`/workflow:continue`).

## [0.2.0] - 2026-04-30

### `workflow`

#### Added

- `write`: strips AI writing patterns and rewrites prose to sound human. Routes to a French or English reference based on the text. Includes a bilingual review mode (FR↔EN parity, typography, faux amis). Explicit-invocation only (`/workflow:write`).

#### Changed

- `sync-files` renamed to `sync`. Cross-repo semantic consistency scan is now the default and only mode; `--deep` flag removed. Invocation: `/workflow:sync`.

## [0.1.0] - 2026-04-26

Initial public release.

### `audit`

#### Added
- `walkthrough`: interactive, point-by-point walkthrough of a review report. Orchestrator mode (target + reviewer) and walkthrough-only mode (existing report). Re-evaluates findings, proposes fixes, checks impacted files for regressions.
- `sweep`: full-coverage project review with parallel specialist agents (architecture, quality, tests, docs), consolidated deduplicated report sorted by severity.
- `blindspot`: circularity-aware orchestrator. Detects when a reviewer shares its target's codebase, prompts, or model family, then injects cross-model judging via OpenRouter and convergence analysis. Explicit-invocation only.
- `skill-adversary`: adversarial critic for Claude Code skills. Reports trigger edge cases, instruction ambiguities, contradictions, cross-file coherence issues, and gaps.
- `mcp-adversary`: adversarial critic for MCP servers. Reports inter-tool discrimination issues, schema anti-patterns, semantic drift, error handling inconsistencies, and undocumented workflow dependencies.

#### Security
- `skill-adversary` and `mcp-adversary`: sub-agents use path-based file access instead of embedded prompts, removing prompt-injection surface.

### `workflow`

#### Added
- `sync-files`: scan files for staleness relative to recent changes and propose targeted updates. `--deep` mode runs cross-repo semantic consistency scan with parallel agents. User-invocable only.

[0.4.0]: https://github.com/hebstr/claude-code-plugins/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/hebstr/claude-code-plugins/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/hebstr/claude-code-plugins/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/hebstr/claude-code-plugins/releases/tag/v0.1.0
