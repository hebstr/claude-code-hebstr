---
name: reco
description: "Invoke ONLY when the user explicitly types `/workflow:reco` — do not auto-trigger on phrases like 'qu'en penses-tu', 'que recommandes-tu', 'what do you think', 'best practices', or any other recommendation-asking vocabulary. The CLAUDE.md communication rule already covers light-mode end-of-prompt recommendations; this skill is for deep recommendations that require external sources (official documentation + community practice + verified citations). Without arguments: ask the user what they want a recommendation on. With arguments: research the topic via parallel agents (official docs via WebFetch, community practice via WebSearch), then synthesize a structured recommendation. User-invocable only via /workflow:reco."
allowed-tools: Read Glob Grep Bash WebFetch WebSearch Agent
---

# Reco

Deep-mode recommendation backed by external sources.

## Invocation

This skill only runs when the user types `/workflow:reco` explicitly. It is not auto-triggered by semantic description matching.

If you arrived here through anything other than an explicit `/workflow:reco` invocation, stop and ask the user what they actually want.

The light-mode equivalent ("present your own recommendation when offering choices") is already a CLAUDE.md communication rule. Invoke this skill only when the user wants the heavier output: official documentation + community practice + verified citations.

## Input

`/workflow:reco <free-form description of what the user is considering>`

Examples:
- `/workflow:reco should I use polars or pandas for this CSV pipeline (1M rows, mostly transforms)?`
- `/workflow:reco best way to structure a Python CLI with subcommands and a config file`
- `/workflow:reco what's the recommended pattern for stopping criteria in evolutionary algorithms`

If invoked with no arguments, ask the user what they want a recommendation on — do not guess from prior context.

## Process

1. **Parse the input.** Identify the domain (R, Python, shell, architecture, statistics, etc.), the specific question, and the constraints if mentioned. If the question is ambiguous on a load-bearing dimension (e.g. "best way to do X" without saying for what scale or context), ask one clarifying question before proceeding.

2. **Spawn two parallel agents** in a single message (two `Agent` tool calls):
   - **Agent A — official documentation.** Search for and fetch the relevant official docs. Prefer authoritative sources (project websites, PEPs for Python, CRAN docs for R, RFCs, etc.). Verify URLs before citing. Report what the doc actually says, with quoted excerpts and source URLs. Use `general-purpose` (Explore lacks WebFetch/WebSearch in practice).
   - **Agent B — community practice.** Search blogs, conference talks, GitHub issues, Stack Overflow answers, and notable practitioners' writing. Report consensus and divergences with sources. Use `general-purpose`.

3. **Synthesize in the main thread.** Wait for both agents, then produce the output structure below. Do not rubber-stamp agent output: subagent claims are unverified — spot-check anything that will drive the recommendation (URLs, CLI flags, API syntax, version numbers).

## Output structure

```
## My take
<1-3 sentences: direct recommendation with reasoning, formed before reading agent output to keep it independent>

## Tradeoffs
<bullet list of the key tradeoffs, max 5>

## What the official documentation says
<summary from Agent A with quoted excerpts and verified URLs; if no authoritative doc found, say so>

## What the community recommends
<summary from Agent B noting consensus vs divergence, with sources; flag if the community contradicts the docs>

## Final recommendation
<single sentence stating the recommendation, then 1-2 lines of justification grounded in the evidence above>
<if sources disagree or evidence is thin, say so explicitly and lower the confidence>
```

## Guardrails

- Never write a URL without verifying it (WebFetch or `gh api` for GitHub). Training-data URLs are unreliable. If verification fails, omit the link and say so.
- If sources disagree, surface the disagreement — do not paper over it.
- If neither agent finds authoritative material, lower confidence in the final recommendation and say what evidence is missing.
- Mirror the user's conversation language for prose. Structured headers can stay in English.
- Stay in the scope of the question. Do not expand to adjacent decisions unless directly relevant.
- The "My take" section comes first and is written before reading the agents' output — this is intentional, so that external sources can confirm, refine, or overturn an independent prior rather than anchor it.
