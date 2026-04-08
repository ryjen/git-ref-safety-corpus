# Agent Threat Model

This document applies a lightweight threat-modeling framework to the corpus so discussions can stay structured and repeatable.

It uses four simple layers:

1. system scope
2. trust boundaries
3. STRIDE threat categories
4. security requirements

## System scope

The system in scope is any AI-agent or automation workflow that:

- receives repository-controlled metadata
- republishes that metadata into prompts, plans, templates, or command arguments
- allows later components to interpret the resulting output

Examples:

- agentic CI/CD orchestration
- internal assistants that prepare commands from repository context
- review bots
- self-hosted coding agents
- task runners that mix user intent with Git metadata

## Assets

Assets potentially affected by this class of issue:

- source code integrity
- deployment correctness
- CI/CD credentials
- GitHub or Git provider tokens
- workflow secrets
- artifact integrity
- environment selection and release policy decisions
- auditability of generated actions

## Entry points

Representative untrusted inputs:

- branch names
- PR titles and bodies
- commit messages
- issue comments
- file names
- workflow-dispatch inputs
- repository config values

These are authorized inputs at the Git or collaboration layer, but they are still untrusted at the agent and execution layers.

## Trust boundaries

### Boundary 1: repository metadata to orchestrator context

Example:

```text
Git event -> workflow context.branch
```

Risk:

- metadata becomes available to automation without sink-specific validation

### Boundary 2: orchestrator context to freeform prompt or template

Example:

```text
context.branch -> "Check out branch {{ branch }} and prepare commands"
```

Risk:

- untrusted data is mixed with instructions
- provenance is lost

### Boundary 3: prompt to agent-generated plan

Example:

```text
prompt -> generated shell commands or tool calls
```

Risk:

- the agent reinterprets metadata as control-bearing text
- fallback or retry logic may amplify ambiguity

### Boundary 4: generated plan to execution sink

Example:

```text
generated plan -> shell / CLI / deploy wrapper / approval action
```

Risk:

- parser confusion
- command injection
- wrong-target deployment
- misleading review or approval outcomes

## STRIDE analysis

### Spoofing

Relevant cases:

- `feature-main-u3000-demo`
- Unicode-confusable PR titles or comments

Risk:

- agents or humans believe the metadata refers to a trusted branch or release target when it does not

### Tampering

Relevant cases:

- `feature-$(echo-test)`
- `feature-${IFS}echo-test`
- prompt-shaped issue comments or PR text

Risk:

- generated plans, scripts, or commands are altered by untrusted metadata

### Repudiation

Relevant cases:

- truncated UI labels
- normalized display values differing from raw values

Risk:

- it becomes hard to prove what exact metadata the agent saw versus what operators saw

### Information disclosure

Relevant cases:

- metadata influencing agent-generated commands that expose secrets
- workflow context copied into logs, prompts, or task transcripts

Risk:

- tokens, secrets, and internal URLs may be exposed through downstream actions or outputs

### Denial of service

Relevant cases:

- parser-confusion values such as `feature--help`
- retry loops triggered by malformed or misleading metadata

Risk:

- workflows fail closed in noisy ways or repeatedly trigger invalid execution paths

### Elevation of privilege

Relevant cases:

- untrusted metadata causes an agent or runner to invoke privileged operations it would not otherwise perform

Risk:

- metadata crosses from data plane into control plane and influences actions executed with CI/CD or app-level privileges

## Structured outcomes

This corpus supports the following claims:

1. Git-valid metadata can become dangerous after leaving Git.
2. The key failure is loss of trust-boundary discipline, not invalid ref syntax.
3. AI-agent systems widen the attack surface because they introduce prompt, planning, and tool-selection boundaries before execution.
4. Security fixes must be applied at each sink, not only at repository ingestion.

## Security requirements

Derived requirements for AI-agent and CI/CD systems:

- treat repository metadata as untrusted outside Git
- keep metadata in typed fields as long as possible
- avoid flattening metadata and instructions into the same freeform prompt
- require typed tool calls or argv-style execution for downstream actions
- validate values separately for shells, CLIs, paths, templates, and display
- log raw and escaped forms for review-sensitive metadata
- preserve provenance so the system can distinguish user intent from repository metadata
- prevent fallback logic from broadening execution when parsing fails

## Suggested review questions

- Where does repository metadata first enter the workflow?
- Where is metadata converted into freeform text?
- Which component first turns that text into executable intent?
- Are raw and display forms handled separately?
- Can the same metadata influence both machine execution and human approval?
- Is validation performed at each sink, or only once upstream?
