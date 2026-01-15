#!/usr/bin/env python3
"""Scan files for hidden/bidirectional Unicode characters."""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

SUSPICIOUS_CODEPOINTS = {
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
    0x200B,
    0x200C,
    0x200D,
    0xFEFF,
}


def is_suspicious(char: str) -> bool:
    codepoint = ord(char)
    if codepoint in SUSPICIOUS_CODEPOINTS:
        return True
    return unicodedata.category(char) == "Cf"


def scan_file(path: Path) -> list[tuple[int, int, str]]:
    findings: list[tuple[int, int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_index, line in enumerate(lines, start=1):
        for col_index, char in enumerate(line, start=1):
            if is_suspicious(char):
                name = unicodedata.name(char, "UNKNOWN")
                findings.append((line_index, col_index, f"U+{ord(char):04X} {name}"))
    return findings


def clean_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    cleaned = "".join(char for char in text if not is_suspicious(char))
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for hidden Unicode")
    parser.add_argument("--fix", action="store_true", help="Remove suspicious chars")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    args = parser.parse_args()

    had_findings = False
    for input_path in args.paths:
        path = Path(input_path)
        files = [path] if path.is_file() else list(path.rglob("*"))
        for file_path in files:
            if not file_path.is_file():
                continue
            findings = scan_file(file_path)
            if findings:
                had_findings = True
                for line, col, info in findings:
                    print(f"{file_path}:{line}:{col}: {info}")
                if args.fix:
                    clean_file(file_path)

    return 1 if had_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
