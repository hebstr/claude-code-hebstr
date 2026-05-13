---
name: blindspot
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash Agent Skill
description: >
  Circularity-aware orchestrator for audit skills. Detects when an audit skill (skill-adversary,
  mcp-adversary, sweep, critical-code-reviewer) is about to review an artifact that shares
  its own codebase, prompts, or model family — then injects cross-model judging and transparency
  countermeasures via OpenRouter.
  EXPLICIT-INVOCATION ONLY: this skill never auto-triggers from implicit context
  (enforced by `disable-model-invocation: true`). Invoke directly via "/blindspot"
  or by name ("lance blindspot", "blindspot review").
  Use when: the user explicitly invokes blindspot, asks for a "circular review" /
  "review circulaire" / "self-review check", flags that reviewer and target share
  the same origin ("review [skill] with [skill]", "review this skill with skill-adversary"
  on a Claude Code skill), or asks for circularity countermeasures alongside another
  audit skill ("check for circularity", "add a second opinion", "get an external judge").
  Do NOT apply to: general code review, PR review, plain skill-adversary/mcp-adversary/sweep
  invocations without circularity concern, or LLM evaluation methodology discussions.
---

# blindspot

Orchestrates circularity-aware auditing. When an audit skill must review an artifact that shares
its own base (code, prompts, model family), this skill detects the conflict and injects
countermeasures: cross-model judging via OpenRouter, and a transparency block in the final report.

**Orchestration must run in the main model context.** The only subagent this skill spawns is cross-model-judge (for the OpenRouter call). Do not delegate the orchestration itself to a subagent.

## Invocation

```
/blindspot <target-path> [--reviewer <audit-skill>]
```

- `<target-path>` (positional, required): path to the artifact being reviewed
- `--reviewer <audit-skill>` (flag, optional): the audit skill to run. Default: `critical-code-reviewer`. Supported: `skill-adversary`, `mcp-adversary`, `sweep`, `critical-code-reviewer`, or any review skill.

This syntax is harmonized with `/walkthrough` so that chaining the two is frictionless: same positional `<target>` first, same `--reviewer` flag, same default reviewer.

If invoked without `<target-path>`, ask the user for it. If `--reviewer` is omitted, default to `critical-code-reviewer` silently.

### Input validation

Before proceeding, validate `<target-path>`:
1. Resolve it to an absolute path
2. Verify it exists and contains readable files
3. Reject paths outside `~/.claude/` and the current working directory tree. Report the error using this template and stop:

   ```
   <target-path> is outside the allowed scope (~/.claude/ or the current working directory). blindspot refuses to read arbitrary filesystem paths to avoid acting on unintended targets.

   To proceed, either:
     - cd into the project root that contains <target-path>, then relaunch /blindspot <target-path>
     - or pass an absolute path inside ~/.claude/ if you intended to audit an installed skill
   ```

   Substitute `<target-path>` with the resolved absolute path the user passed.
4. Reject self-invocation — would create infinite recursion. Resolve `--reviewer` to a concrete `SKILL.md` path using the same runtime resolution procedure as Phase 0 Path overlap (env shortcut → installed_plugins.json → `~/.claude/skills/`). If the resolved path's directory matches blindspot's own directory (compare via `realpath` on both sides), reject the invocation regardless of how the user spelled the argument (literal `blindspot`, absolute path, relative path, or symlink). Report the error and suggest using a different audit skill (e.g., `--reviewer skill-adversary`). Also reject if `--reviewer` resolves to a wrapper skill that, by its own SKILL.md content, would re-invoke blindspot internally (best-effort check: grep the resolved SKILL.md for `/blindspot` or `audit:blindspot` invocations; if found, refuse and require the user to pass the wrapper's underlying audit skill directly).

## Phase 0 — Circularity Detection

Determine whether the audit is circular. A review is circular when reviewer and target share
any of these properties.

### Path overlap

Check if `<target-path>` is within or overlaps with the audit skill's own directory. The audit skill's location must be resolved at runtime — do not rely on a single static env var, because `${CLAUDE_PLUGIN_ROOT}` is only set when the host plugin is invoked through the normal plugin loader and is undefined in dev mode (skill executed from a checked-out repo) or non-plugin installs (`~/.claude/skills/<name>/`).

**Resolution procedure**, in order. First match wins:

1. **`${CLAUDE_PLUGIN_ROOT}` shortcut.** If `$CLAUDE_PLUGIN_ROOT` is non-empty AND `$CLAUDE_PLUGIN_ROOT/audit/<reviewer>/SKILL.md` exists, use that path. This is the fast path for the standard plugin install.
2. **Plugin manifest scan.** Read `~/.claude/plugins/installed_plugins.json`, walk each install path, look for `<install_path>/audit/<reviewer>/SKILL.md`. If found, use that path.
3. **Global skill scan.** Look for `~/.claude/skills/<reviewer>/SKILL.md`. If found, use that path.
4. **No path resolvable.** The reviewer's install location cannot be determined. Skip the directory-comparison conditions (1) and (2) of the overlap check below, fall back to condition (3) only (the distributional rule — any Claude-authored reviewer/target pair sets path overlap = Yes), and append an `info` line in the report: `Reviewer <name> path not resolved — directory overlap check skipped.`

Path overlap is circular if **any** of these conditions is true (OR logic):
1. Target path is inside the resolved audit skill directory (direct self-review) — applies only when resolution succeeded.
2. Target path contains files imported or referenced by the audit skill — applies only when resolution succeeded.
3. **Distributional path-overlap rule** — sets path overlap = Yes whenever both reviewer and target share Claude as their distributional origin, regardless of directory comparison or whether step 4 of the resolution fired:
   - **Target side**: the target is Claude-authored content — a Claude Code skill (`SKILL.md`), an MCP server with tool definitions authored for Claude, a project containing prompt text / agent definitions / `CLAUDE.md` rules optimized for Claude, or other Claude-distribution-shaped artifacts.
   - **Reviewer side**: the audit skill's own instructions were written by/for Claude — i.e. it is a Claude Code skill itself. In practice this covers `skill-adversary`, `mcp-adversary`, `sweep`, `critical-code-reviewer`, and any future audit skill installed as `SKILL.md`.
   - When both sides hold, the audit shares distributional assumptions with its target even without filesystem overlap; the rule was originally written for skill-adversary but applies identically to every Claude-authored reviewer/target pair.

### Model family overlap

The reviewing model and the model that generated the target share the same family if either condition holds (OR):
- The target was generated by Claude (any version) AND the reviewer is Claude. In Claude Code the
  reviewer is always Claude, so this reduces to "target was generated by Claude" — a property of
  the target, not a constant.
- The target contains prompt text, SKILL.md instructions, or agent definitions authored for
  Claude — these were optimized for Claude's distribution and will be judged leniently by Claude.

Both conditions are False only when the target is human-written code or code generated by a
non-Claude model with no Claude-targeted prompt content. In that case, model-family overlap = No.

### Circularity verdict

| Path overlap | Model family overlap | Verdict |
|-------------|---------------------|---------|
| Yes | Yes | **Strong circularity** — both structural and distributional bias |
| No | Yes | **Model circularity** — distributional bias only (most common case) |
| Yes | No | **Structural circularity** — unlikely in practice |
| No | No | **No circularity** — proceed normally |

If **no circularity** (rare — typically human-written codebase being audited by Claude): inform the
user that blindspot's countermeasures are not load-bearing here, but proceed anyway — the user
explicitly invoked `/blindspot`, so honor that. Skip the cross-model judge to avoid wasting an
OpenRouter call, run the original audit skill directly, and append a short note in the report
explaining why the cross-model layer was skipped.

If circularity detected: report the verdict and proceed to Phase 1.

### Report to user

```
## Circularity Detection

**Audit skill:** <skill-name>
**Target:** <target-path>
**Path overlap:** Yes/No — <explanation>
**Model family overlap:** Yes/No — <explanation>
**Verdict:** <Strong circularity / Model circularity>

Proceeding with countermeasures.
```

## Phase 1 — Cross-Model Routing

The primary countermeasure is routing part of the audit to a model from a different family
via OpenRouter.

### Detect OpenRouter availability

```bash
test -n "$OPENROUTER_API_KEY" && echo "openrouter:available" || echo "openrouter:missing"
```

### If OpenRouter available: Pick external model

Before spawning the cross-model judge, present the model menu to the user and wait for their choice. Display verbatim in the user's language:

```
External model for cross-model judge — Claude wrote the target, so the goal is a second opinion from a non-Claude family.

  1. google/gemini-2.5-pro       — default. Strong reasoning, far from Claude's training distribution. Slower, more expensive.
  2. google/gemini-2.5-flash     — same family as 1, cheaper and faster. Use for large targets where cost matters.
  3. openai/gpt-4.1              — rigorous, instruction-focused. Different family from 1 — useful if you've already audited with Gemini.
  4. openai/o4-mini              — OpenAI's reasoning model (visible thinking). Slower than gpt-4.1 but catches subtler logic flaws.
  5. deepseek/deepseek-r1        — open reasoning model. Often more direct, less hedged than commercial models.
  6. meta-llama/llama-4-maverick — open weights, alternative distribution. Pick when other models converge and you want a wildcard.
  7. Custom                        — type any OpenRouter model ID. A cost notice is shown before launch.

Quick rule: for a one-shot audit, pick 1. For a second pass after Gemini, pick 3 or 5 (different family). For speed on a large artifact, pick 2.

Your choice [1-7, Enter for default]:
```

**On user response:**

- **`1`-`6`** → map to the corresponding curated entry (see `agents/cross-model-judge.md` for the canonical mapping). Use that model ID as `EXTERNAL_MODEL`.
- **Empty / `Enter` / `default` / "1"** → use `google/gemini-2.5-pro`.
- **Full model ID matching one of the curated entries** (e.g., `openai/gpt-4.1`) → accept and use it.
- **`7` / `custom`** → trigger the custom flow described below.
- **Anything else / ambiguous** → re-present the menu once with a one-line clarification ("Pick a number 1-7 or press Enter for default."), then default to `1` on a second ambiguous response.

**Custom model flow (option 7):**

1. Prompt: `OpenRouter model ID (e.g., provider/model-name):` and wait for input.
2. Validate the input format with regex `^[A-Za-z0-9_-]+/[A-Za-z0-9._-]+$` (letters, digits, dashes/dots/underscores; case-insensitive; exactly one slash; no spaces). If invalid, re-prompt once showing the expected pattern. On second invalid input, abort the custom flow and default to `1`.
3. On valid format, display the cost notice and wait for confirmation:

   ```
   ⚠ Custom model: <model-id>

   This model is not in the curated list. OpenRouter pricing varies by orders of magnitude across providers and tiers — frontier reasoning models can be 50-100× the cost per call of smaller mid-tier models.

   Verify current pricing at https://openrouter.ai/<model-id> before continuing.

   Proceed with <model-id>? [y/N]:
   ```

4. On `y` / `yes` → use the custom ID as `EXTERNAL_MODEL`. On `N` / empty / anything else → return to the main model menu (re-display from the top).

**No silent interpolation.** The format regex is the only validation done by the skill — it rejects shell-suspicious characters (spaces, `;`, `|`, `$`, `\``, backticks, etc.) before the value ever reaches the agent. The agent uses `jq --arg` parameterization (see `agents/cross-model-judge.md`), which is injection-safe regardless, but the skill-level regex prevents accidental typos from triggering OpenRouter API errors that would consume a billing call.

**Do not persist the user's choice.** Same reasoning as walkthrough's notices: a "remember my pick" toggle would silently lock the audit into one model family across future invocations, defeating the purpose of cross-model judging. The menu is cheap (one keystroke for default) and the right model can depend on what the user already audited.

### Launch cross-model judge

Spawn the **cross-model-judge** agent (see agents/cross-model-judge.md) in **foreground** with these inputs:

- `TARGET_PATH`: the resolved `<target-path>` from invocation
- `ARTIFACT_TYPE`: `"skill"` if target contains a SKILL.md, `"mcp-server"` if it contains MCP tool definitions, `"codebase"` otherwise
- `AUDIT_FOCUS`: derive from the audit skill, in this order:
  1. **Known reviewers** (built-in mapping):
     - `skill-adversary` → `"trigger accuracy, instruction clarity, security, completeness"`
     - `mcp-adversary` → `"tool discrimination, schema quality, discoverability"`
     - `sweep` or `critical-code-reviewer` → `"code quality, security, architecture, test coverage"`
  2. **Unknown reviewer**: extract the reviewer's stated focus dynamically — read the resolved reviewer `SKILL.md`'s `description:` frontmatter field, identify the audit dimensions it claims to check (e.g., look for verbs like "review", "audit", "find", followed by their objects), and join them as `"<dim1>, <dim2>, ..."`. If the description does not surface concrete dimensions, fall back to the generic `"code quality, security, correctness, completeness"`.
  3. Never pass an empty or literal `"undefined"` value — the external model would receive `AUDIT FOCUS: ` with no focus and produce a less targeted audit.
- `EXTERNAL_MODEL`: the model ID selected at the previous step

Then spawn the original audit skill as a **second foreground Agent** (not via the Skill tool — the Skill tool would run the audit inline in the main context and exhaust the budget; the walkthrough orchestrator follows the same convention for the same reason). The Agent's prompt instructs it to read the target audit skill's `SKILL.md` and execute its procedure on `<target-path>`.

**Canonical parallel pattern.** Emit both Agent tool calls in a single message — two `Agent` blocks side by side. This is the only reliable way to parallelize: a Skill call would block the main context and force the Agent to wait, and sequential Agent calls double the wall-clock time. The pattern is identical to the one the parent walkthrough orchestrator already validated; reuse it as-is.

### If OpenRouter not available: Fallback mode

Do NOT silently skip. Instead:

1. Warn the user that no cross-model countermeasure is available
2. Spawn the audit skill as a **foreground Agent** (same pattern as the cross-model-judge path above — never via the Skill tool, to keep the orchestrator's context budget intact)
3. Append a **fallback transparency block** to the report (see Phase 2)

## Phase 2 — Transparent Report

After collecting results, compile the final report.

### If cross-model judge was used

Present the report using this template:

```
## Blindspot Review — <target>

### Circularity Assessment

**Audit skill:** <skill-name>
**Verdict:** <Strong circularity / Model circularity>
**Countermeasures applied:** Cross-model judge via OpenRouter (<model-name>)

### Cross-Model Findings (<model-name>)

<Findings from the external model, formatted as a numbered list with severity>

### Same-Model Findings (Claude)

<Findings from the original audit skill>

### Convergence Analysis

To build this section, compare the two finding sets using semantic matching. Wording will differ — match on substance, not phrasing.

**Matching procedure.** For each external finding, scan all Claude findings for a match. Two findings match when **at least 2 of these 3 signals align**:

1. **Same scope** — same file or same logical section (e.g. same agent, same Phase block, same function). Cross-file findings match when they target the same conceptual unit.
2. **Same root cause** — same underlying defect class (e.g. "stale documentation vs implementation", "missing error path", "ambiguous instruction", "unreachable branch"). Symptom phrasing differs; defect class doesn't.
3. **Same fix mechanism** — the corrective action would touch the same surface (same lines, same instruction, same conditional). If both findings would be resolved by the same edit, they match.

When only 1 signal aligns, treat as a near-miss: classify both findings separately (one Claude-only, one external-only) and add a brief note in the Convergence Analysis that they may target related issues. When 0 signals align, the findings are independent.

Then: for each Claude finding, check whether it was already matched to an external finding. Classify every finding into exactly one bucket: agreed, Claude-only, or external-only.

If either model returned zero findings or errored out, skip the convergence analysis and note which source is missing.

**Meta-bias note.** This matching step is performed by Claude — the same model whose self-preference is being audited. Self-preference can bias the classification in two directions: (a) over-matching (declaring "agreed" to suppress an external-only finding Claude missed), (b) under-matching (declaring "Claude-only" when Claude agreed but used different wording, inflating own-findings novelty). Boundary cases between agreed and Claude-only deserve the most skepticism. This caveat is also surfaced in the Transparency block.

**Agreed findings** (flagged by both models):
<List — these are high-confidence findings>

**Claude-only findings** (not flagged by external model):
<List — these may reflect self-preference bias or genuine issues the external model missed>

**External-only findings** (not flagged by Claude):
<List — these are the blindspot candidates — issues Claude may have systematically overlooked>

### Transparency

- **Circularity type:** <verdict>
- **External model used:** <model name> via OpenRouter
- **Residual bias risk:** Cross-model judging reduces but does not eliminate bias.
  The external model has its own biases. Convergent findings are highest confidence.
  Divergent findings warrant human attention.
- **Convergence matching done by Claude:** the agreed/Claude-only/external-only classification
  was assigned by Claude — the same model being audited for self-preference. Treat boundary
  cases between agreed and Claude-only with extra skepticism; Claude may have over-matched
  to suppress findings it missed, or under-matched to inflate its own findings' novelty.
- **Recommendation:** Review "External-only findings" with particular care —
  these represent potential blindspots in Claude's self-evaluation.
```

### If fallback mode (no OpenRouter key)

Run the original audit skill as a foreground Agent (same Agent-not-Skill convention as Phase 1), then append:

```
## Blindspot Review — <target>

### Circularity Assessment

**Audit skill:** <skill-name>
**Verdict:** <Strong circularity / Model circularity>
**Countermeasures applied:** None (OPENROUTER_API_KEY not set)

### Audit Findings

<Findings from the original audit skill>

### Circularity Warning

This audit was performed by Claude reviewing a Claude-authored artifact.
No cross-model countermeasure was available.

**Known bias risks:**
- Self-preference bias: Claude systematically rates its own outputs higher
  (Panickssery et al., 2024)
- Shared RLHF distribution: reviewer and target share the same notion of "good output"
- Sycophantic agreement: tendency to validate presented content rather than critique it

**Manual countermeasures recommended:**
1. Set OPENROUTER_API_KEY to enable automatic cross-model judging:
   - Get a key at https://openrouter.ai/keys (free tier available)
   - `export OPENROUTER_API_KEY=<your-key>` in your shell (and add the line to `~/.bashrc` / `~/.zshrc` for persistence)
   - Restart Claude Code so the new env is inherited by the MCP servers and Bash subshells
   - Re-run `/blindspot <target-path> [--reviewer <skill>]` — the cross-model judging path will activate automatically
2. Ask a human reviewer to specifically check for findings that seem surprisingly lenient
3. Challenge any "no issues found" conclusions — absence of findings is itself a red flag
   in a circular review
4. Compare severity ratings against similar non-circular reviews for calibration

### Transparency

- **Circularity type:** <verdict>
- **External model used:** None
- **Residual bias risk:** HIGH — no cross-family mitigation applied.
  All findings should be treated with additional skepticism.
```

## Important constraints

- **Orchestrator only.** This skill never performs the audit itself. It detects circularity,
  routes to an external model when possible, and wraps the results in transparency.
- **Does not block audits.** If circularity is detected but no countermeasure is available,
  the audit still runs — with warnings.
- **No duplicate work.** The original audit skill runs exactly once. The cross-model judge
  runs independently. Results are compared, not merged.
- **Transparency is mandatory.** Every report includes the circularity assessment and
  countermeasures applied (or not applied), regardless of findings.
- **Model selection.** The external model is picked interactively at invocation via the menu in Phase 1 (default on Enter: `google/gemini-2.5-pro` — strong reasoning, non-Claude family). Six curated options are surfaced; option 7 accepts any OpenRouter model ID after format validation and an explicit cost-warning confirmation. Both the skill and the agent re-validate against the format regex `^[A-Za-z0-9_-]+/[A-Za-z0-9._-]+$` (defense in depth), and the agent uses `jq --arg` parameterization for the actual API call.
- **No credentials in prompts.** The OPENROUTER_API_KEY is read from the environment.
  Never log, echo, or include it in any output.
