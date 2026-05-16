---
name: doc-structure
description: Audit and reorganize project documentation layout — CLAUDE.md (Claude rules) vs README.md (human docs). User-invocable only via `/workflow:doc-structure`; does not auto-trigger on mentions of CLAUDE.md, README.md, documentation, or sync. Status: WIP — convention to refine on first real usage.
allowed-tools: Read Write Edit Glob Grep
---

# doc-structure (WIP)

**Status: WIP MVP.** Captured from the 2026-05-16 audit of `solatis/claude-config:doc-sync`. Convention details are intentionally underspecified — refine on the first concrete usage (data project, R package, Quarto book).

## Pre-flight gate

Before running the workflow, surface this notice and wait for confirmation:

> ⚠ This skill is WIP. The HOW/WHY taxonomy and the cross-doc convention are placeholders that will be refined on first concrete usage. Migration proposals from this run reflect provisional rules. Continue? [y/N]

On `N` or empty: exit cleanly without running any phase. On `y`: proceed.

## Workflow (5 phases, adapted from solatis doc-sync)

### 1. Discovery

Map every `CLAUDE.md` and `README.md` in the project. Exclude these directories (illustrative list — add similar vendored/generated dirs as encountered): `.git`, `node_modules`, `bower_components`, `vendor`, `renv/`, `.venv/`, `__pycache__`, `target/`, `dist/`, `build/`, Quarto `_freeze/`, `_site/`, `_book/`. Do not use `.gitignore` as the exclusion source — it commonly contains `.claude/`, which is the skill's primary scan target. Report counts + locations.

If more than one `CLAUDE.md` or more than one `README.md` is found (monorepo, sub-package layout), stop after Phase 1. Surface the file list to the user and ask which pair to scope the audit on; do not proceed to Phase 2 until a single pair is selected. The monorepo convention is unresolved (see "Convention" section).

If neither `CLAUDE.md` nor `README.md` is found, stop after Phase 1 with a message and exit; there is nothing to audit. If exactly one of the two is missing, stop after Phase 1 and ask the user whether to create an empty stub for the missing file (do not auto-create); on confirmation, write a one-line placeholder and exit, so the user can populate it before re-running. Do not synthesize content from the present file.

### 2. Audit

For each file, classify content into:

- **HOW (operational)**: paths, Claude-facing operational commands (e.g. "to rebuild the index, run X"), naming conventions, decision log entries, "when editing X do Y" — belongs in `CLAUDE.md`. Excludes user-facing install/usage commands, which always go to README.
- **WHY (architectural)**: rationale, invariants, tradeoffs, design decisions, install/usage docs (including the commands users run to install or use the project) — belongs in `README.md`
- **Mixed / ambiguous**: flag for user judgment. Default-route these sections to Mixed so they reach the end-of-Phase-2 adjudication (where the user can drop them): license headers, changelogs, contributor lists, code of conduct, security policies, embedded YAML/JSON config blocks. Do not silently skip these — a security policy may contain operational instructions for Claude that warrant migration

At the end of Phase 2, before Phase 3 starts, surface all Mixed/ambiguous items as a single batched list with one-line rationale per item. For each, ask the user to assign HOW, WHY, or "drop — no migration". Phase 3 then runs on the consolidated HOW/WHY classifications.

### 3. Migration

This is what distinguishes `/workflow:doc-structure` from `/workflow:sync`, which only detects inconsistencies without proposing moves.

For each piece of misplaced prose:

- Propose verbatim move (CLAUDE.md prose → README.md section, or vice versa)
- Bundle all proposed moves for the selected CLAUDE.md/README.md pair into a single before/after diff covering both files
- Wait for user approval on that bundle. The user may accept the whole bundle, reject the whole bundle, or selectively accept/reject individual moves within it (numbered list). No auto-apply across the project; granularity is per file pair, not per prose block

### 4. Index updates

After migrations, ensure `CLAUDE.md` provides a table-style index of what's where:

```
| Path | What | When to read |
|------|------|--------------|
| README.md | install + usage + architecture | when onboarding or evaluating an integration |
```

Placement: insert the table under a top-level `## Index` heading at the bottom of `CLAUDE.md`. If `## Index` already exists, replace its content (do not append a duplicate section). The "What" column states the file's primary content type in 3-6 words; "When to read" states a concrete trigger condition, not a generic phrase like "before starting work".

Skip Phase 4 entirely when zero migrations were accepted in Phase 3 — the existing layout is presumed correct.

### 5. Verification

- Re-read modified files end-to-end
- Check that cross-references between CLAUDE.md and README.md still resolve. Scope: markdown links of the form `[text](path)` and `[text](path#anchor)` only. "Resolve" means: target file exists at the link path (relative to the linking file's directory), and if an anchor is present, a heading in the target file generates that anchor (GFM slugification: lowercase, spaces → `-`, punctuation stripped). Do not check bare URLs, plain-text mentions of file names, or external links.

## Convention (placeholder — refine on usage)

- `.claude/CLAUDE.md` = project-specific rules for Claude (paths, datasets, naming, recent decisions) + an `## Index` section listing project documentation files with their purpose and read-trigger
- `README.md` (project root) = human-facing: architecture, install, usage
- No `README.md` in subdirectories unless at least one of these conditions holds: (a) the subdirectory contains a public entry point (CLI, library export, plugin install command) with its own usage instructions that do not fit the parent narrative; (b) the subdirectory is an independently testable or runnable unit; (c) the subdirectory is published, vendored, or distributed as a standalone artifact

**Open question (to resolve on first usage):** how does this interact with sub-package READMEs in monorepos? Defer until concrete case appears.

## Maintainer notes (not runtime instructions)

The block below is a TODO list for the human maintainer. Claude must not act on it during normal skill invocation — do not propose `/audit:walkthrough` or any other command at the end of a run on the basis of this section.

- This is a WIP MVP.
- After 1-2 real usages: tighten the convention, remove the placeholders.
- Once the convention is stable: re-audit with `/audit:walkthrough --reviewer audit:skill-adversary` to validate the trigger language.
