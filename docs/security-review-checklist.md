# Security Review Checklist

This checklist turns the threat model in [docs/agent-threat-model.md](/home/ryjen/Projects/git-ref-safety-corpus/git-ref-safety-corpus/docs/agent-threat-model.md) into concrete review questions.

Use it for:

- AI-agent orchestration reviews
- CI/CD workflow reviews
- internal assistant or bot reviews
- design discussions about repository metadata handling

## Scope and inputs

- Does the system consume branch names, PR titles, commit messages, issue comments, file names, workflow inputs, or repo config values?
- Are those values explicitly classified as untrusted once they leave Git or the collaboration layer?
- Is there a clear inventory of which metadata fields can influence prompts, plans, commands, paths, templates, or approvals?

## Trust boundaries

- Where does repository metadata first enter workflow context?
- Where is metadata copied into freeform text?
- Where is metadata converted into executable intent, shell commands, CLI args, or deployment actions?
- Are trust-boundary crossings documented?

## Prompt and planning safety

- Is raw repository metadata embedded into freeform prompts?
- Can the agent confuse repository metadata with user intent?
- Is metadata preserved as typed fields rather than flattened prose where possible?
- Does the system preserve provenance so the agent can distinguish metadata from instructions?
- Can retry or fallback logic broaden agent discretion after parse failures?

## Tool and execution safety

- Are downstream actions expressed as typed tool calls or argv-style execution rather than shell-built strings?
- Is shell usage avoided where possible?
- If shell usage exists, are untrusted values kept out of command text?
- Are explicit field names such as `--branch` used instead of positional parsing where relevant?
- Are sink-specific validations applied for shells, CLIs, paths, templates, and artifact names?

## Display and approval safety

- Do operators see the raw value and an escaped or normalized form for suspicious metadata?
- Can UI truncation hide important suffixes or invisible characters?
- Can normalization change the apparent meaning of a value?
- Can the same metadata influence both machine execution and human approval?

## Logging and auditability

- Are raw values logged for audit?
- Are escaped or normalized values logged for human review?
- Can the team reconstruct exactly what the agent saw and what operators saw?
- Are approval events tied to the raw underlying metadata value?

## STRIDE-oriented checks

### Spoofing

- Could metadata appear visually similar to a trusted branch, environment, or release target?

### Tampering

- Could metadata alter generated plans, scripts, or command lines?

### Repudiation

- Would truncation, normalization, or missing logs make investigation difficult?

### Information disclosure

- Could metadata influence the agent into exposing secrets, token-bearing URLs, or internal paths?

### Denial of service

- Could parser-confusion values or retry loops repeatedly break workflows?

### Elevation of privilege

- Could metadata influence an agent or runner to take privileged actions it would not otherwise perform?

## Outcome

If any answer above is unclear or negative, the system should be treated as requiring additional controls before repository metadata is allowed to influence agent planning or CI/CD execution.
