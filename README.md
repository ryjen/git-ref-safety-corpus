# Git Ref Safety Corpus

A defensive test corpus for Git ref names that are benign as repository metadata but become risky when downstream systems treat them as trusted input.

## Purpose

This repository exists to support discussion, validation, and tooling around the gap between:

- authorized repository metadata
- safe downstream interpretation

It is inspired by recent public research into branch-name-driven command injection in AI/automation environments, but it is intentionally scoped for defensive testing and policy discussion.

## In scope

Examples here are meant to help reason about:

- shell metacharacters in ref names
- argument / parser confusion
- Unicode / invisible-character obfuscation
- encoded or high-entropy strings

## Out of scope

This repository does not include:

- live credential exfiltration payloads
- end-to-end exploit automation
- destructive commands intended for execution

## Example categories

- refs/shell-like.txt
- refs/parser-confusion.txt
- refs/unicode-obfuscation.txt
- refs/encoded-high-entropy.txt
- refs/agent-inputs.txt
- docs/boundary-matrix.md

## Why

Git metadata increasingly flows into:

- CI/CD pipelines
- shell scripts
- agent systems
- templates and prompts

The core issue is not only whether metadata is authorized, but whether it remains safe when interpreted outside Git.

## Non-Codex workflow examples

The public Barrack writeup on the Codex issue includes several concrete branch-name examples that are also useful for reasoning about non-Codex automation systems such as Anthesis, internal CI/CD wrappers, self-hosted agents, or orchestration pipelines:

- `-1`
- `main;...`
- `main;curl${IFS}...`
- `main[U+3000 padding]|| true;...`

In those cases, the branch name mattered not because Git considered it special, but because a downstream system treated the ref as executable or parser-significant input.

This corpus includes local analogues that map to the same classes of failure:

- `feature-$(echo-test)`
  Similar to the article's `main;...` and `${IFS}` examples. Useful for discussing shell interpretation after unsafe string interpolation into a command, task spec, or runner wrapper.

- `feature-${IFS}echo-test`
  Closest local analogue to the article's `${IFS}` bypass example. Useful for showing how a Git-valid ref can still become multiple shell words at execution time.

- `feature--help`
  Not a shell injection example, but a parser / argument confusion example in the same family. Useful for discussing wrappers, CLIs, or orchestration layers that stop treating a ref as opaque data and start treating it like an option.

- `feature-main-u3000-demo`
  Closest local analogue to the article's Unicode-obfuscated `main[U+3000 padding]...` example. Useful for discussing normalization mismatches, UI truncation, approval confusion, and hidden suffixes in branch-derived workflow state.

For Anthesis-style or other non-Codex workflows, the general path is:

1. Branch name enters workflow context as repository metadata.
2. The workflow republishes it into prompts, templates, scripts, env vars, or command strings.
3. A later component interprets it as syntax rather than opaque data.

That is the boundary where a valid ref becomes a vulnerability.

## Additional discussion aids

- `docs/boundary-matrix.md`
  A compact mapping from Git refs to downstream sinks such as shells, CLI parsers, prompts, and approval UIs.

- `docs/ai-agent-boundaries.md`
  A short note focused on agentic workflows: prompt construction, plan generation, typed tool calls, and why Git metadata remains untrusted once it enters agent context.

- `docs/agent-threat-model.md`
  A lightweight trust-boundary and STRIDE-based threat model for AI-agent and CI/CD workflows that consume repository metadata.

- `docs/security-review-checklist.md`
  A concrete review checklist for agent builders and CI/CD owners covering trust boundaries, prompt safety, execution sinks, display handling, auditability, and STRIDE-oriented checks.

- `docs/agent-input-surface.md`
  A short note showing that the same agent-boundary problem applies to PR titles, commit messages, issue comments, file names, and workflow-dispatch inputs.

- `scripts/demo_ci_cd_flows.py`
  A small non-executing simulation that shows how the same branch looks when reused in shell strings, argv-style calls, task text, and Unicode-sensitive display paths.

- `scripts/demo_agent_boundary.py`
  A non-executing simulation that contrasts unsafe freeform prompt construction with safer structured task data and typed tool plans.

- `scripts/demo_agent_inputs.py`
  A non-executing simulation that shows how different metadata types become risky when flattened into freeform agent context.
