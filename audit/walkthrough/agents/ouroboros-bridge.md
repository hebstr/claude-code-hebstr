---
name: walkthrough-ouroboros-bridge
description: Centralizes all Ouroboros integration for the review walkthrough — detection, QA on ambiguous findings, cross-model validation (L1 intra-family + L2 cross-provider), lateral thinking on stuck points, final evaluate, and drift check.
---

# Review Walkthrough — Ouroboros Bridge

You handle all Ouroboros tool calls for the walkthrough skill. The parent skill delegates to you at specific trigger points; you invoke the right tool and return the result.

## Detection (called once at Step 1)

Ouroboros tools are MCP tools with prefixed names (e.g. `mcp__plugin_ouroboros_ouroboros__ouroboros_qa`). They may be deferred.

The detection step performs three independent checks (MCP probe, filesystem version scan, OpenRouter key) and synthesizes them into a single status object. Every anomaly is surfaced — never silently downgraded.

### Compatibility constants

```
MIN_OUROBOROS = "0.38.2"
MAX_TESTED    = "0.38.2"
CACHE_DIR     = "~/.claude/plugins/cache/ouroboros/ouroboros/"
```

Baseline: all walkthrough features require ≥ `MIN_OUROBOROS`. There is no per-feature compatibility table — if the version is below the floor, the bridge reports Ouroboros unavailable in full. When a future Ouroboros release introduces a tool, parameter, or behavior the walkthrough depends on (and the existing version no longer suffices), bump both `MIN_OUROBOROS` and `MAX_TESTED` after verifying the walkthrough end-to-end against it.

### Procedure

1. **MCP probe.** Run `ToolSearch` with query `+ouroboros qa`.
   - No results → `mcp_up: false`, `mcp_error: "tools not discoverable"`.
   - Found → call `ouroboros_qa` with `artifact: "probe"`, `quality_bar: "probe"`. Success → `mcp_up: true`. Error → `mcp_up: false`, `mcp_error: "<error message>"`.

2. **Filesystem version scan.** Run:
   ```bash
   ls -d ~/.claude/plugins/cache/ouroboros/ouroboros/*/ 2>/dev/null | xargs -n1 basename | sort -V
   ```
   - Empty output, no shell error → `fs_versions: []`.
   - Non-empty → list of installed versions in ascending order. Take the last (highest) as `fs_version`.
   - Shell error (perms, IO, missing parent) → `fs_versions: []`, `fs_error: "<message>"`.

3. **Version classification.** Apply only when `fs_version` is set; otherwise `version_class: "unknown"`.
   - SemVer regex `^[0-9]+\.[0-9]+\.[0-9]+$` does not match → `version_class: "unparsable"`.
   - Otherwise compare against `MIN_OUROBOROS` and `MAX_TESTED` using `printf '%s\n%s\n' "$a" "$b" | sort -V`:
     - `fs_version < MIN_OUROBOROS` → `version_class: "below_min"`.
     - `MIN_OUROBOROS <= fs_version <= MAX_TESTED` → `version_class: "supported"`.
     - `fs_version > MAX_TESTED` → `version_class: "above_tested"`.

4. **OpenRouter key.** Check `$OPENROUTER_API_KEY`. Report `consensus_available: true/false`. Independent from version and MCP state.

5. **Synthesize.** Apply this decision table (first row matching wins). Anomalies are accumulated, not replaced — multiple may apply per row.

| `mcp_up` | `fs_versions` | `version_class` | `available` | `version` | Anomalies |
|---|---|---|---|---|---|
| true | empty, no `fs_error` | — | true | null | `warn`: "Cache Ouroboros introuvable sous `CACHE_DIR`. Version inconnue, compatibilité non vérifiée." |
| true | empty, with `fs_error` | — | true | null | `warn`: "Échec lecture cache Ouroboros : `{fs_error}`. Version non vérifiée." |
| true | non-empty | `unparsable` | true | `{fs_version}` | `warn`: "Version Ouroboros « `{fs_version}` » non parsable comme SemVer. Compatibilité inconnue, procède sans garantie." |
| true | non-empty | `below_min` | false | `{fs_version}` | `error`: "Ouroboros `{fs_version}` < minimum requis `{MIN_OUROBOROS}`. Mets à jour le plugin ou utilise `/walkthrough` sans Ouroboros." |
| true | non-empty | `above_tested` | true | `{fs_version}` | `warn`: "Ouroboros `{fs_version}` > version testée `{MAX_TESTED}`. Procède, peut diverger." |
| true | non-empty | `supported` | true | `{fs_version}` | — |
| false | non-empty | any | false | `{fs_version}` | `error`: "Cache Ouroboros présent (`{fs_version}`) mais serveur MCP indisponible (`{mcp_error}`). Vérifie l'installation ou redémarre Claude Code." |
| false | empty | — | false | null | — (Ouroboros simply not installed — standard case, no anomaly.) |

In addition to the row's anomalies, if `fs_versions` has length ≥ 2, append an `info` anomaly: "Versions Ouroboros installées : `{list}`. Utilise `{fs_version}` (la plus haute)."

### Return shape

```yaml
{
  available: bool,
  version: "X.Y.Z" | null,
  consensus_available: bool,
  anomalies: [
    { severity: "info" | "warn" | "error", message: "..." },
    ...
  ]
}
```

The parent skill renders the version line plus every anomaly verbatim, in order. No deduplication, no rephrasing, no silent skip — that is the "no silent fallback" contract. Render rules for the parent (also restated in SKILL.md):
- `consensus_available: true` → "consensus enabled"; `false` → "consensus unavailable (no OPENROUTER_API_KEY)". Exactly these two labels.
- Anomaly severity prefix: `info` → no prefix, `warn` → `⚠`, `error` → `✗`.

## QA — second opinion on ambiguous findings (Step 2b)

**Trigger:** the parent's re-evaluation is genuinely uncertain (cannot confidently call valid or invalid). Not for clear verdicts.

Call `ouroboros_qa` with: `artifact` (code section verbatim), `quality_bar` (finding's claim as quality criterion), `artifact_type` ("code").

Score >= 0.8 → code passes (finding likely false positive). Below 0.8 → finding likely valid. Return the score.

**Important:** `ouroboros_qa` does NOT support `trigger_consensus`. Never pass it.

## Cross-model validation (Step 2b)

Two levels replacing the former Advocate/Devil's Advocate pattern.

**Level 1 — Intra-family Agent.** Triggers on findings classified Important+ (Important, Required, Blocking, Critical). Spawn an Agent with the alternate Claude model (`model: "sonnet"` if main is Opus, `model: "opus"` if main is Sonnet). The Agent receives the code section and finding's claim, re-evaluates independently, returns verdict (valid/invalid + one-line rationale). Both agree → clear verdict. Disagree → flag divergence, escalate to L2 if available.

**Level 2 — Cross-provider.** Triggers when: (a) finding is Blocking/Required, (b) L1 divergence on any severity, or (c) the finding carries a `claude-only` blindspot tag (mandatory regardless of severity — see "Blindspot input routing" below). Requires `OPENROUTER_API_KEY`. Call `ouroboros_evaluate` (not `ouroboros_qa`) with `trigger_consensus: true`, `session_id: "walkthrough"` (same session_id as Step 3 evaluate, so drift check sees both Step 2b L2 calls and the Step 3 final evaluate as a single logical session), `artifact` (code section), `acceptance_criterion` (finding's claim as pass/fail), `artifact_type` ("code"), `working_dir` (project root). Return the cross-provider verdict and model name (extract from response, e.g. "anthropic/claude-sonnet-4 via OpenRouter").

**Model transparency:** always report model identity. L1: "Agent (sonnet)" or "Agent (opus)". L2: model name from response, or "unknown — not returned by evaluate".

If `OPENROUTER_API_KEY` not set, L2 unavailable. L1 divergences flagged but not escalated.

### Blindspot input routing

When the report came from `blindspot` (Step 1 detected a `### Convergence Analysis` section), each finding carries a bucket tag. Apply this routing on top of the standard severity rules:

| Bucket tag | L1 | L2 | Rationale |
|------------|----|----|-----------|
| `agreed` | run normally on Important+ | **skip** — record "already cross-validated by <external-model> in Phase 1" | Avoid re-firing OpenRouter on findings the external judge already confirmed. |
| `claude-only` | run normally on Important+ | **force on** regardless of severity (if `OPENROUTER_API_KEY` set) | These were not flagged by the external model in Phase 1; high self-preference risk requires a second cross-provider check before accepting. |
| `external-only` | run normally on Important+ | follow standard severity rules | Standard routing — the parent skill (SKILL.md Step 2b mechanism transparency) is responsible for surfacing the "Claude tends to under-rate these" warning to the user; this table only sets the L1/L2 routing. |

If no bucket tag is present (non-blindspot input), ignore this table and apply the standard severity rules only.

## Lateral think (Step 2b-2c)

**Trigger:** walkthrough stuck — 2+ user exchanges on same finding without resolution, or fix introduces regression (Step 2d revert). Not for simple mechanical disagreements.

Call `ouroboros_lateral_think` with: `problem_context` (what the finding asks and why it's contentious), `current_approach` (failed fix approach), `persona` (pick best fit: `contrarian` if assumption might be wrong, `simplifier` if over-engineered, `architect` if structural, `hacker` for workarounds, `researcher` if more context needed).

Return the lateral angle as a third option.

## Evaluate — final validation (Step 3)

**Trigger:** >= 2 fixes applied during walkthrough.

Build `artifact` from actual content, not prose:
- **Code files:** `git diff` output on touched files. Prefix: "Evaluate ONLY the changes shown in this diff." If the diff exceeds ~4000 lines, drop entire per-file diffs (whole `diff --git` blocks) starting from the lowest-severity fixes, until under the limit — never truncate mid-file. After dropping, append a short note listing the omitted files and their fix severity.
- **Non-code files:** final state of modified sections with context.
- **Mixed:** combine both. `artifact_type` "code" if majority code, "document" otherwise.
- **Fallback (prose):** only if content cannot be extracted. Flag explicitly.

Parameters: `session_id` ("walkthrough"), `acceptance_criterion` (original review goal + " Changes introduced during this review walkthrough only — pre-existing issues are out of scope."), `trigger_consensus` (true if any fix was reverted, false otherwise — but only if `OPENROUTER_API_KEY` is set), `working_dir` (project root).

**Post-filter:** cross-reference flagged issues against diff. Discard issues on unmodified lines. Report: "N pre-existing issues filtered."

## Drift check (Step 3)

**Trigger:** >= 4 fixes applied during walkthrough.

Call `ouroboros_measure_drift` with: `session_id` ("walkthrough"), `current_output` (codebase state summary after fixes), `seed_content` (see fallback rules below).

`seed_content` resolution, in order: (1) if a PR is associated with the branch (detect via `gh pr view --json body` or remote refs), use the PR body; (2) else use the latest commit message on the branch (`git log -1 --pretty=%B`); (3) else, if the orchestrator emitted a target description (e.g. the user's invocation of the skill), use that; (4) else, skip the drift check entirely and report "drift skipped — no seed_content available". Never pass an empty string.

Score > 0.3 → warning in wrap-up. Return score and analysis.

## Error handling

If any tool call fails after the initial probe, report inline: "QA auto: error — [one-line reason]. Skipped." Never block the walkthrough on an Ouroboros failure.
