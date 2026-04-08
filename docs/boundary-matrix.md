# Git Ref Boundary Matrix

This matrix is meant for defensive analysis of how a Git-valid ref can become dangerous when downstream systems stop treating it as opaque data.

## Boundary model

The core path is:

1. A branch name enters a workflow as repository metadata.
2. The workflow republishes it into another context.
3. A later component interprets it as syntax, structure, or policy input.

The vulnerability appears at step 3, not at the Git layer.

## Matrix

| Source | Sink / boundary | Failure mode | Example ref from corpus | Related public example |
| --- | --- | --- | --- | --- |
| Git ref | Shell command string | Command injection via metacharacters or substitution | `feature-$(echo-test)` | `main;...` |
| Git ref | Shell command string | Word-splitting / shell reconstruction through `${IFS}` | `feature-${IFS}echo-test` | `main;curl${IFS}...` |
| Git ref | CLI / wrapper argument parsing | Option or parser confusion when ref stops being opaque data | `feature--help` | `-1` |
| Git ref | Generated script or task spec | Injection when templated text is later executed | `feature-$(echo-test)` | `main;...` |
| Git ref | Prompt / agent task text | Prompt contamination that later influences tool or shell generation | `feature-${IFS}echo-test` | `main;curl${IFS}...` |
| Git ref | Display / approval UI | Visual spoofing, hidden suffixes, or review confusion | `feature-main-u3000-demo` | `main[U+3000 padding]|| true;...` |
| Git ref | Normalization / allowlist checks | Inconsistent policy decisions across components | `feature-main-u3000-demo` | `main[U+3000 padding]|| true;...` |
| Git ref | Artifact names / cache keys / paths | Wrong-target routing, collisions, parser confusion, path handling surprises | `feature--help` | `-1` |

## Concrete non-Codex workflows

### Orchestrator to runner

Unsafe pattern:

```text
webhook -> workflow context.branch -> template "git fetch origin {{ branch }}" -> shell
```

Risk:

- `feature-$(echo-test)` becomes command substitution if a shell evaluates the string.
- `feature-${IFS}echo-test` can be reconstructed into multiple shell words at execution time.

### Orchestrator to CLI wrapper

Unsafe pattern:

```text
webhook -> branch passed to wrapper -> wrapper re-emits string into tool invocation
```

Risk:

- `feature--help` stops being treated as a branch identifier and starts behaving like an option-shaped token.

### Orchestrator to agent prompt

Unsafe pattern:

```text
webhook -> branch inserted into task text -> agent plans shell/tool actions from prompt context
```

Risk:

- branch text acts as control input inside a later planning or execution boundary.

### Orchestrator to human approval

Unsafe pattern:

```text
webhook -> branch rendered in UI -> reviewer sees truncated or normalized form
```

Risk:

- `feature-main-u3000-demo` may look more trusted than it is if downstream display handling hides or normalizes parts of the string.

## Defensive guidance

- Treat Git refs as untrusted input outside Git.
- Prefer argv-style process execution over shell-built command strings.
- Use `--` where relevant when forwarding untrusted values to CLIs.
- Separate raw values from display values; normalize for display and policy, but preserve raw values for logging and audit.
- Do not inject raw refs into prompts, scripts, templates, cache keys, or file paths without sink-specific handling.
