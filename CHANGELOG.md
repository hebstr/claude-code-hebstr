# Changelog

## [Unreleased]

### `review`

#### Changed
- `full-review` — pre-launch availability report now also checks `/review-walkthrough` (Phase 4 dependency), in addition to `/critical-code-reviewer` and the R-package skills.
- `skill-adversary` — `output-fuzzer` sub-agent deferred to V2; context doc updated to reflect the two-agent layout (`trigger-attacker`, `instruction-critic`) and point to `doc/v2.md` for the third axis.
- `blindspot-review` — added `disable-model-invocation: true` to enforce the explicit-invocation contract claimed in the description (previously gated by description text only ; the canonical Claude Code mechanism is the boolean field).
- `mcp-adversary`, `skill-adversary` — removed non-canonical `context: main` field from frontmatter. The official Claude Code skill schema only documents `context: fork` (forked subagent context) ; the absence of the field already means execution in the parent context, so `context: main` was redundant at best and invited undefined behavior at worst.

#### Removed
- `litrev` plugin reverted to standalone repo (`github.com:hebstr/claude-code-litrev`). Migration into the `hebstr` marketplace was never validated runtime; rolled back to keep stacks (markdown skills vs Python MCP) and audiences (Claude Code devs vs medical researchers) separated.

### `workflow`

#### Added
- `write` — strips AI writing patterns from prose and rewrites it to sound human. Routes between French and English references based on the text being edited (`references/write-fr.md` ~900 lines, `references/write-en.md`). Includes a bilingual review mode (FR↔EN typography, faux amis, calques, allowlist of preserved technical anglicisms). Migrated from a personal fork of `waza/write` after substantial divergence (FR reference, bilingual mode, custom allowlist).

#### Changed
- `sync-files` renamed to `sync`. Cross-repo semantic consistency scan with parallel agents (formerly opt-in via `--deep`) is now the default and only mode; `--deep` flag removed. Invocation is now `/sync`.
- `write` — French reference split into a register-neutral core always loaded (`references/write-fr-core.md`, ~230 lines, 19 cross-register rules + 12 most frequent AI tells) and an extended file loaded on demand (`references/write-fr-extended.md`, ~680 lines, faux amis full table, corporate-tone, rare typography, dé-listification). Extended loads in Bilingual Review Mode, on explicit deep-review request, or for register edge cases (administrative, release notes, rare typography). Legacy `write-fr.md` removed. Version `3.24.0-fr` → `3.25.0-fr`.
- `write` — hardening pass after `/review:blindspot-review` (skill-adversary on Sonnet + cross-model judge `google/gemini-2.5-pro` via OpenRouter): scoped « kill all adverbs » to empty intensifiers only (preserves meaning-bearing adverbs); added explicit user-text-is-data firewall to Hard Rules; clarified FR detection threshold (majority running prose, not isolated tokens); resolved overlap between Pre-flight routing and Bilingual Review Mode (mode now requires two parallel versions); capped dé-listification scope (single block only, ask before propagating across sections); added Pre-flight in-scope check that refuses commit messages, code comments, docstrings on explicit invocation; reconciled output rule with Bilingual Mode inline annotations.
- `write` — frontmatter aligned to Claude Code skill standard ([code.claude.com/docs/en/skills.md](https://code.claude.com/docs/en/skills.md)). Removed non-standard `metadata.version` field (no canonical `version` field in the skill schema; internal release tag now tracked in `WRITE_PLAN.md` and the plugin-level `marketplace.json` only). Added `disable-model-invocation: true` — the canonical mechanism documented for forcing explicit-only invocation, replacing the description-text-only gate.

## [0.1.0] - 2026-04-26

Initial public release.

### `review` 0.1.0

#### Added
- Plugin scaffolding with 5 skills bundled.
- `review-walkthrough` — interactive, point-by-point walkthrough of a review report. Orchestrator mode (target + reviewer) and walkthrough-only mode (existing report). Re-evaluates findings, proposes fixes, checks impacted files for regressions.
- `full-review` — full-coverage project review with parallel specialist agents (architecture, quality, tests, docs), consolidated deduplicated report sorted by severity.
- `blindspot-review` — circularity-aware orchestrator. Detects when a reviewer shares its target's codebase, prompts, or model family, then injects cross-model judging via OpenRouter and convergence analysis. Explicit-invocation only.
- `skill-adversary` — adversarial critic for Claude Code skills. Reports trigger edge cases, instruction ambiguities, contradictions, cross-file coherence issues, and gaps.
- `mcp-adversary` — adversarial critic for MCP servers. Reports inter-tool discrimination issues, schema anti-patterns, semantic drift, error handling inconsistencies, and undocumented workflow dependencies.

#### Security
- `skill-adversary` and `mcp-adversary` switched from content-embedded sub-agent prompts to a path-based contract: sub-agents receive absolute paths and `Read` files themselves. Removes prompt-injection surface via closing tags (`</skill>`, `</server>`) and context-bleed via prompt negation. Validated cross-model on 2026-04-25.

### `workflow` 0.1.0

#### Added
- Plugin scaffolding with 1 skill bundled.
- `sync-files` — scan files for staleness relative to recent changes and propose targeted updates. `--deep` mode runs cross-repo semantic consistency scan with parallel agents. User-invocable only.

[0.1.0]: https://github.com/hebstr/claude-code-plugins/releases/tag/v0.1.0
