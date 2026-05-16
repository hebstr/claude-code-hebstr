---
name: model-extract
description: Use when the user wants to reverse-engineer a statistical or simulation model codebase into a formal specification — typically inherited Stan/brms/PyMC/cmdstanr code, ODE/PDE systems, agent-based models, epidemiological or biostatistical pipelines. Also triggered by `/audit:model-extract <path>`.
allowed-tools: Read, Glob, Grep, Bash(rg:*), Bash(fdfind:*)
disable-model-invocation: true
---

# model-extract

Reverse-engineer a model implementation into a formal specification: math, observation model, likelihood and priors, inference procedure, and an explicit list of ambiguities and red flags. Goal: separate what the code *demonstrably does* from what the author *probably intended*, so the user can validate the model's scientific assumptions.

## Operating principles

Every claim must be tagged as one of:

| Tag | Meaning | Evidence |
|---|---|---|
| **observed** | Directly read from code | `path:line` citation required |
| **inferred** | Reasonable extrapolation from observed code + standard usage | Cite both the code anchor and the convention being assumed |
| **speculative** | Plausible but not supported by current evidence | Flag explicitly; offer questions to resolve |

Never let inferred claims drift into observed claims. If the only evidence for X is "Stan files usually do X", that's inferred, not observed.

## Scope check

Before starting, confirm the target is one of:
- Probabilistic model (Stan, brms, rstanarm, PyMC, NumPyro, Turing.jl)
- Mechanistic / dynamical system (ODE/PDE in deSolve, diffeqr, SciPy, JAX)
- Agent-based model
- Statistical pipeline with explicit likelihood (custom GLMM, survival, state-space)
- Calibration / inverse problem code

If the target is a generic data pipeline or ML training script without an explicit generative or mechanistic model, this skill is the wrong tool. Suggest a code-review skill instead.

## Workflow

### Step 0 — Model boundary

Map directory and file roles. Separate:
- **Model code** (the math): `.stan` files, likelihood functions, ODE definitions, transition rules
- **Inference runtime** (the engine): MCMC config, ODE solver options, optimization loop
- **Data plumbing** (I/O): readers, formatters, post-processing

Output: a small directory map with one-line roles. Do not deep-read everything; identify what to read in Step 1.

### Step 1 — Entry-point inventory

Table of models found, even if there's only one:

| Model ID | Type | Primary file(s) | Entry point | Status |
|---|---|---|---|---|
| (assign or use existing name) | probabilistic / mechanistic / ABM / hybrid | path | function or script | active / dead-code / WIP |

### Step 2 — Formal specification (per model)

For each active model, extract:

1. **Classification**: statistical (regression, hierarchical, mixture), state-space, ODE/PDE, ABM, hybrid.
2. **Generative story** (1–2 sentences): what data is observed, what latents and parameters generate it, what stochasticity is assumed.
3. **Math** (LaTeX):
   - State evolution or generative process
   - Observation model (likelihood)
   - Priors (with hyperparameters)
   - Inference target (posterior, MAP, MLE, calibration objective)
4. **Inference procedure**: algorithm (NUTS / HMC / VI / ABC / particle filter / Newton / L-BFGS), chain count, iterations, warmup, tuning parameters. Cite the call site.

For ODE/PDE models, add: state vector, initial conditions, parameters, solver + tolerances, time grid.

For ABMs, add: entity state vector, update semantics (synchronous / asynchronous / continuous-time), transition rules as `precondition → stochastic mechanism`, RNG handling and seed strategy.

### Step 3 — Red flags

Three mandatory lists, even if empty:

- **Ambiguities** requiring human resolution (e.g. "prior `normal(0, sigma)` — sigma is read from a config not yet located")
- **Potential bugs** with severity (Info / Warn / Critical) and confidence (Low / Med / High); each requires a `path:line` anchor
- **Scientific risks** (identifiability, prior dominance, model misspecification, numerical instability, reproducibility gaps); each requires a validation suggestion

### Step 4 — Deliverable

Single markdown document with sections:
1. Executive summary (≤ 5 sentences)
2. Model inventory table
3. Per-model math sheets with parameter tables
4. Cross-cutting notes (shared utilities, reused priors)
5. Validation checklist (concrete checks the user should run before trusting outputs)

## Reading discipline

- Follow call graphs from the entry point. Don't ingest the repo wholesale.
- Stop reading a file once its role is clear. The math sheet is the output, not a transcript.
- When a number is stated, cite where it comes from (file, line, or env var). Hardcoded magic numbers are a red flag in themselves.
- If the same parameter has different names across files, list all aliases and pick a canonical one.

## What this skill is not

- Not a code review (use `audit:walkthrough` or `posit-dev:critical-code-reviewer` for that)
- Not a documentation generator (this skill exposes uncertainty; doc generation hides it)
- Not a model improver (only describes what's there; user decides what to fix)
