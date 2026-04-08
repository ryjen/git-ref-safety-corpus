#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def parse_entries(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " not in line:
            continue
        kind, value = line.split(": ", 1)
        entries.append((kind, value))
    return entries


def unsafe_prompt(kind: str, value: str) -> str:
    return (
        "Agent task:\n"
        f"- Metadata source: {kind}\n"
        f"- Metadata value: {value}\n"
        "- Use the metadata above to decide the next command or action.\n"
    )


def safer_record(kind: str, value: str) -> dict[str, str]:
    return {
        "metadata_source": kind,
        "metadata_value": value,
        "handling": "treat_as_untrusted_data",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("refs/agent-inputs.txt")
    entries = parse_entries(path)

    print("This script demonstrates agent input-surface handling only.")
    print("It does not execute or transform metadata values.")
    print()

    for kind, value in entries:
        print("=" * 72)
        print(f"Source: {kind}")
        print(f"Value:  {value}")
        print()

        print("Unsafe freeform prompt:")
        for line in unsafe_prompt(kind, value).splitlines():
            print(f"  {line}")
        print()

        print("Safer typed record:")
        print(f"  {safer_record(kind, value)}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
