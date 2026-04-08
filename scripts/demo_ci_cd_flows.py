#!/usr/bin/env python3
from __future__ import annotations

import shlex
import sys
import unicodedata


def shell_command_unsafe(branch: str) -> str:
    return f"git fetch origin {branch}"


def shell_command_safe_preview(branch: str) -> str:
    argv = ["git", "fetch", "origin", branch]
    return " ".join(shlex.quote(part) for part in argv)


def parser_confusion_example(branch: str) -> list[str]:
    return ["deploy-tool", branch]


def parser_confusion_safer(branch: str) -> list[str]:
    return ["deploy-tool", "--branch", branch]


def prompt_example(branch: str) -> str:
    return (
        "Workflow task:\n"
        f"- Check out branch: {branch}\n"
        "- Prepare commands for validation and deployment.\n"
    )


def unicode_display(branch: str) -> dict[str, str]:
    normalized = unicodedata.normalize("NFKC", branch)
    escaped = branch.encode("unicode_escape").decode()
    truncated = branch[:18] + ("..." if len(branch) > 18 else "")
    return {
        "raw": branch,
        "escaped": escaped,
        "normalized_nfkc": normalized,
        "truncated_display": truncated,
    }


def print_case(branch: str) -> None:
    print("=" * 72)
    print(f"Branch: {branch}")
    print()

    print("1. Unsafe shell string")
    print(f"   {shell_command_unsafe(branch)}")
    print()

    print("2. Safer argv preview")
    print(f"   {shell_command_safe_preview(branch)}")
    print()

    print("3. Parser boundary")
    print(f"   ambiguous argv: {parser_confusion_example(branch)}")
    print(f"   explicit argv:  {parser_confusion_safer(branch)}")
    print()

    print("4. Prompt / task text")
    for line in prompt_example(branch).splitlines():
        print(f"   {line}")
    print()

    print("5. Display / normalization")
    display = unicode_display(branch)
    for key, value in display.items():
        print(f"   {key}: {value}")
    print()


def main() -> int:
    branches = sys.argv[1:] or [
        "feature-$(echo-test)",
        "feature-${IFS}echo-test",
        "feature--help",
        "feature-main-u3000-demo",
    ]

    print("This script demonstrates interpretation boundaries only.")
    print("It does not execute branch contents.")
    print()

    for branch in branches:
        print_case(branch)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
