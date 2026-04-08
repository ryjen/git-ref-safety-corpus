#!/usr/bin/env python3
from __future__ import annotations

import shlex
import sys

def unsafe_command(branch: str) -> str:
    return f"git fetch origin {branch}"

def safe_argv(branch: str) -> list[str]:
    return ["git", "fetch", "origin", branch]

def main() -> int:
    branch = sys.argv[1] if len(sys.argv) > 1 else "feature/example"

    print("UNSAFE string command:")
    print(unsafe_command(branch))
    print()

    print("SAFE argv form:")
    print(safe_argv(branch))
    print()

    print("Shell-escaped preview:")
    print(" ".join(shlex.quote(part) for part in safe_argv(branch)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
