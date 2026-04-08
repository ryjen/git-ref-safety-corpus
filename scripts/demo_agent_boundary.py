#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unicodedata


def unsafe_prompt(branch: str) -> str:
    return (
        "Repository task:\n"
        f"- Check out branch {branch}\n"
        "- Figure out the commands needed to validate and deploy it.\n"
        "- If anything fails, retry with an equivalent command.\n"
    )


def safer_structured_task(branch: str) -> dict[str, object]:
    return {
        "action": "checkout_and_validate",
        "repository": "owner/example-repo",
        "branch": branch,
        "constraints": {
            "treat_branch_as_data": True,
            "require_structured_tool_calls": True,
            "forbid_shell_string_interpolation": True,
        },
    }


def naive_agent_plan_from_prompt(branch: str) -> list[str]:
    return [
        f"git fetch origin {branch}",
        f"git checkout {branch}",
        "run validation and deployment commands",
    ]


def safer_agent_plan(branch: str) -> list[dict[str, object]]:
    return [
        {
            "tool": "git.fetch",
            "args": ["origin", branch],
        },
        {
            "tool": "git.checkout",
            "args": [branch],
        },
        {
            "tool": "workflow.validate",
            "args": [],
        },
    ]


def display_forms(branch: str) -> dict[str, str]:
    return {
        "raw": branch,
        "escaped": branch.encode("unicode_escape").decode(),
        "nfkc": unicodedata.normalize("NFKC", branch),
    }


def print_case(branch: str) -> None:
    print("=" * 72)
    print(f"Branch: {branch}")
    print()

    print("1. Unsafe freeform prompt")
    for line in unsafe_prompt(branch).splitlines():
        print(f"   {line}")
    print()

    print("2. Safer structured task")
    print(json.dumps(safer_structured_task(branch), indent=2))
    print()

    print("3. Naive agent plan from prompt")
    for step in naive_agent_plan_from_prompt(branch):
        print(f"   - {step}")
    print()

    print("4. Safer typed tool plan")
    for step in safer_agent_plan(branch):
        print(f"   - {json.dumps(step)}")
    print()

    print("5. Display / audit forms")
    for key, value in display_forms(branch).items():
        print(f"   {key}: {value}")
    print()


def main() -> int:
    branches = sys.argv[1:] or [
        "feature-$(echo-test)",
        "feature-${IFS}echo-test",
        "feature--help",
        "feature-main-u3000-demo",
    ]

    print("This script demonstrates agent control-boundary issues only.")
    print("It does not execute commands or branch contents.")
    print()

    for branch in branches:
        print_case(branch)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
