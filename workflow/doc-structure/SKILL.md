---
name: doc-structure
description: Audit and reorganize project documentation layout — CLAUDE.md (Claude rules) vs README.md (human docs). User-invocable only via `/workflow:doc-structure`; does not auto-trigger on mentions of CLAUDE.md, README.md, documentation, or sync. Status: WIP — convention to refine on first real usage.
allowed-tools: Read Write Edit Glob Grep
---

# doc-structure (WIP)

**Status: WIP MVP.** Captured from the 2026-05-16 audit of `solatis/claude-config:doc-sync`. Convention details are intentionally underspecified — refine on the first concrete usage (data project, R package, Quarto book).

## Workflow (5 phases, adapted from solatis doc-sync)

### 1. Discovery

Map every `CLAUDE.md` and `README.md` in the project (excluding `.git`, `node_modules`, `renv/`, `.venv/`, `target/`, `dist/`, `build/`). Report counts + locations.

### 2. Audit

For each file, classify content into:

- **HOW (operational)**: paths, commands, naming conventions, decision log entries, "when editing X do Y" — belongs in `CLAUDE.md`
- **WHY (architectural)**: rationale, invariants, tradeoffs, design decisions, install/usage docs — belongs in `README.md`
- **Mixed / ambiguous**: flag for user judgment

### 3. Migration

This is what distinguishes `/workflow:doc-structure` from `/workflow:sync`, which only detects inconsistencies without proposing moves.

For each piece of misplaced prose:

- Propose verbatim move (CLAUDE.md prose → README.md section, or vice versa)
- Show before/after diff per file
- Wait for user approval per migration (no auto-apply across the project)

### 4. Index updates

After migrations, ensure `CLAUDE.md` provides a table-style index of what's where:

```
| Path | What | When to read |
```

### 5. Verification

- Re-read modified files end-to-end
- Check that cross-references between CLAUDE.md and README.md still resolve
- Surface any leftover ambiguous content with one-line rationale

## Convention (placeholder — refine on usage)

- `.claude/CLAUDE.md` = project-specific rules for Claude (paths, datasets, naming, recent decisions)
- `README.md` (project root) = human-facing: architecture, install, usage
- No `README.md` in subdirectories unless there is a gap in invisible knowledge that the parent README cannot carry

**Open question (to resolve on first usage):** how does this interact with sub-package READMEs in monorepos? Defer until concrete case appears.

## Notes

This is a WIP MVP. After 1-2 real usages, tighten the convention, remove the placeholders, and propose `/audit:walkthrough` with `--reviewer audit:skill-adversary` to validate the trigger language.
