# Agent Input Surface

This document expands the discussion beyond branch names.

In AI-agent workflows, many repository-controlled or user-supplied fields can become control input once they are copied into prompts, plans, templates, or shell-adjacent task descriptions.

## Inputs worth treating as untrusted

- branch names
- PR titles
- PR bodies
- commit messages
- issue titles
- issue comments
- file names
- workflow-dispatch inputs
- configuration values in the repository

The important point is not whether these fields are authorized or expected. The important point is whether the agent or orchestrator later treats them as inert data or as freeform control-bearing text.

## Why this matters for agents

Agent systems often blend:

- human instructions
- repository metadata
- prior tool output
- generated plans
- execution requests

If all of those are flattened into the same freeform context, repository metadata can influence the agent's decisions in ways that are hard to audit.

## Example failure modes

### Prompt contamination

Example:

```text
PR title: release prep $(echo-test)
Task: read the PR title, prepare the checkout command, and run validation.
```

The PR title is now inside the same context the agent uses to plan commands.

### Parser confusion

Example:

```text
workflow_dispatch input: branch=--help
```

If an agent or wrapper later emits:

```text
deploy-tool --branch --help
```

the metadata has shifted from data to parser-significant input.

### Review and approval confusion

Example:

```text
PR title: main[U+3000]approval
```

Different components may render, normalize, or truncate that value differently. Agents and humans may not be reasoning over the same apparent string.

## How to use the companion corpus

See [refs/agent-inputs.txt](/home/ryjen/Projects/git-ref-safety-corpus/git-ref-safety-corpus/refs/agent-inputs.txt) for representative values across:

- PR titles
- commit messages
- issue comments
- file names
- workflow-dispatch inputs

The point of that file is not to provide exploits. It is to support defensive testing of orchestration boundaries.

## Safe design principles

- Keep metadata in typed fields rather than freeform prompt prose when possible.
- Preserve source attribution so the agent knows which text is user intent versus repository metadata.
- Validate values per sink before they reach a shell, parser, template, UI, or tool call.
- Avoid fallback logic that turns parse failures into broader freeform agent discretion.
- Log raw and escaped forms for review-sensitive metadata.
