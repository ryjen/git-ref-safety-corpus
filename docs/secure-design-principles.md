# Secure Design Principles Mapping

This document maps the corpus to classic secure design principles, especially the Saltzer and Schroeder principles.

The goal is to show that this class of issue is not only about unusual branch names. It is also about violations of long-standing security design principles.

## Relevant classic principles

### Economy of mechanism

Keep the security design as simple and small as possible.

Application here:

- complex chains such as metadata -> prompt -> plan -> shell increase interpretation risk
- each extra translation layer creates new ambiguity

Takeaway:

- simpler structured flows are safer than freeform prompt-to-command pipelines

### Fail-safe defaults

Default behavior should be deny or safe-fail rather than permissive execution.

Application here:

- suspicious or parser-confusing metadata should not silently continue through privileged workflows
- fallback logic should not broaden agent discretion when parsing fails

Takeaway:

- suspicious metadata should block, downgrade, or require review rather than execute by default

### Complete mediation

Every access to every object should be checked.

Application here:

- validating a branch name once at ingestion is not enough
- the same value may later reach a shell, CLI, path, prompt, template, or approval UI

Takeaway:

- metadata must be validated at each sink where interpretation occurs

### Open design

Security should not depend on secrecy of implementation details.

Application here:

- security should not rely on attackers not knowing prompt formats, wrapper behavior, or parser edge cases

Takeaway:

- systems should remain safe even when workflow structure is understood

### Separation of privilege

Sensitive actions should require multiple independent conditions where possible.

Application here:

- a single metadata value should not be able to influence both planning and privileged execution
- approval and execution should not hinge on the same ambiguous representation

Takeaway:

- separate metadata handling, policy decisions, and privileged execution paths

### Least privilege

Each component should operate with the minimum privileges necessary.

Application here:

- agents, wrappers, and CI/CD runners should not have broad privileges when acting on metadata-derived actions

Takeaway:

- even if metadata handling fails, blast radius should remain limited

### Least common mechanism

Minimize shared mechanisms used by different users or purposes.

Application here:

- reusing the same raw metadata string across prompts, cache keys, file paths, UI labels, and command construction creates unnecessary coupling

Takeaway:

- different sinks should use separate representations and controls

### Psychological acceptability

Security mechanisms should be understandable and usable.

Application here:

- Unicode-confusable or truncated values can mislead reviewers
- operators need raw, escaped, and normalized views where relevant

Takeaway:

- approval and audit paths must be human-comprehensible, not just machine-valid

## Additional modern principles

### Defense in depth

Application here:

- do not rely only on ref filtering
- combine typed execution, sink-specific validation, privilege reduction, and audit logging

### Minimize attack surface

Application here:

- reduce the number of places where repository metadata can shape prompts, plans, or shell text

### Data versus control separation

Application here:

- Git metadata is data at the source-control layer
- the system fails when later layers let it become control input

This is the most important principle for this corpus.

## Principle-to-corpus mapping

| Principle | What failure looks like here | Example |
| --- | --- | --- |
| Economy of mechanism | Too many text-reinterpretation layers | prompt -> plan -> shell |
| Fail-safe defaults | Suspicious metadata still executes | permissive retry or fallback |
| Complete mediation | Validated once, then reused everywhere | branch safe for Git but unsafe for shell |
| Separation of privilege | One value influences both review and execution | display and execution share ambiguous metadata |
| Least privilege | Metadata-driven actions run with broad CI/CD access | privileged runner executes generated plan |
| Least common mechanism | Same raw value reused across many sinks | branch reused in prompt, path, label, command |
| Psychological acceptability | Humans cannot safely review what machines execute | Unicode or truncated display confusion |

## Practical outcome

This corpus can be summarized through secure design principles like this:

- the issue violates complete mediation because metadata is not revalidated at each sink
- it violates economy of mechanism by passing through too many freeform reinterpretation layers
- it violates psychological acceptability when humans review misleading or normalized labels
- it violates least privilege when metadata-influenced actions run with elevated automation credentials

So the right fix is not only "sanitize refs." The fix is to restore secure design discipline across the whole path from repository metadata to execution.
