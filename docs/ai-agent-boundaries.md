# AI Agent Boundary Notes

This document focuses on AI-agent workflows rather than traditional CI/CD alone.

The key point is that a Git ref can become dangerous before it ever reaches a shell. In agentic systems, untrusted repository metadata is often copied into prompts, task descriptions, review text, orchestration plans, or tool-call arguments. Once that happens, the ref stops being "just data" and starts influencing control flow.

## Core pattern

The general path looks like this:

1. A repository event provides metadata such as branch name, PR title, commit message, or file name.
2. The orchestrator inserts that value into freeform task text or agent context.
3. The agent reasons over that text and emits plans, commands, or tool calls.
4. A later tool, runner, or human approval layer interprets the output.

The vulnerability appears when untrusted metadata is allowed to shape the control plane.

## Why AI agents make this worse

Traditional automation often has a single dangerous sink such as a shell command.

AI-agent systems add more interpretation boundaries:

- prompt construction
- plan generation
- tool selection
- argument construction
- retry / fallback logic
- human review of generated actions

That means a ref can influence behavior long before direct execution.

## Unsafe versus safer patterns

Unsafe pattern:

```text
Task: Check out branch feature-$(echo-test) and prepare the commands needed to validate and deploy it.
```

Why it is unsafe:

- branch text is mixed with instructions
- the agent is allowed to reinterpret the value while planning
- downstream tools may receive output influenced by syntax-bearing metadata

Safer pattern:

```json
{
  "action": "checkout_and_validate",
  "repository": "example/repo",
  "branch": "feature-$(echo-test)"
}
```

Why it is safer:

- the branch remains a typed field rather than embedded prompt prose
- downstream code can validate it per sink
- display, policy, and execution can use different handling for the same raw value

## Example mappings from this corpus

### `feature-$(echo-test)`

Use to discuss:

- shell-like syntax entering prompt context
- agent-generated command plans influenced by command-substitution-looking text
- templated task specs that later reach shells or shell-adjacent runners

### `feature-${IFS}echo-test`

Use to discuss:

- shell reconstruction through `${IFS}`
- obfuscated control syntax that looks less obvious in review
- agent plans that may normalize or preserve shell-significant text into later steps

### `feature--help`

Use to discuss:

- parser confusion
- wrappers that stop treating refs as opaque values and start treating them as option-like tokens
- agent-generated CLI commands that omit explicit field names such as `--branch`

### `feature-main-u3000-demo`

Use to discuss:

- review or approval confusion
- display truncation and normalization mismatches
- agents and humans seeing different representations of the same underlying value

## Other Git-controlled inputs that matter for agents

The same boundary problem applies to more than branch names:

- PR titles
- PR body text
- commit messages
- issue titles and comments
- file names
- workflow-dispatch inputs
- config values stored in the repository

If an agent ingests these into freeform context and later emits commands or tool calls, they become part of the agent control surface.

## Threat model for AI-agent workflows

The safest way to explain this class of issue is:

- Git metadata is authorized at the repository layer.
- Authorized metadata is still untrusted at the agent layer.
- Any untrusted metadata copied into prompts, plans, templates, or command strings can become control input.

For a more structured version of that argument, see [docs/agent-threat-model.md](/home/ryjen/Projects/git-ref-safety-corpus/git-ref-safety-corpus/docs/agent-threat-model.md).

## Defensive guidance for agent builders

- Treat all repository metadata as untrusted when it leaves Git.
- Avoid embedding raw refs into freeform prompts when a structured field will do.
- Keep user intent, repository metadata, and execution parameters separate.
- Prefer typed tool calls and argv-style execution over text-built commands.
- Validate each value at the sink where it will actually be interpreted.
- Normalize for display and policy decisions, but preserve raw values for audit logs.
- Make approval UIs show escaped and raw representations for suspicious metadata.
- Do not let the agent "helpfully" reinterpret repo metadata into shell syntax, flags, or template fragments.
