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

## Why

Git metadata increasingly flows into:

- CI/CD pipelines
- shell scripts
- agent systems
- templates and prompts

The core issue is not only whether metadata is authorized, but whether it remains safe when interpreted outside Git.
