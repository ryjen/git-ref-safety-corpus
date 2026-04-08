#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9._/\-${}()]+$")

SUSPICIOUS_MARKERS = [
    "$(",
    "`",
    ";",
    "&&",
    "|",
    "${IFS}",
    "\u200b",
    "\u2060",
    "\u3000",
    "\u202e",
]

def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFKC", value)

def find_issues(ref_name: str) -> list[str]:
    issues: list[str] = []
    normalized = normalize_text(ref_name)

    if ref_name != normalized:
        issues.append("changes under Unicode normalization (NFKC)")

    for marker in SUSPICIOUS_MARKERS:
        if marker in ref_name:
            issues.append(
                f"contains suspicious marker: {marker.encode('unicode_escape').decode()}"
            )

    if not ALLOWED_PATTERN.match(ref_name):
        issues.append("contains characters outside demonstration allowlist")

    if any(ord(ch) < 32 for ch in ref_name):
        issues.append("contains control characters")

    return issues

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_refs.py <path-to-ref-list>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    had_warnings = False

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        ref_name = raw_line.strip()
        if not ref_name or ref_name.startswith("#"):
            continue

        issues = find_issues(ref_name)
        if issues:
            had_warnings = True
            print(f"[WARN] line {line_no}: {ref_name}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[OK]   line {line_no}: {ref_name}")

    return 1 if had_warnings else 0

if __name__ == "__main__":
    raise SystemExit(main())
