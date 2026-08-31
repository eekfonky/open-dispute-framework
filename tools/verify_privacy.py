#!/usr/bin/env python3
"""
verify_privacy.py
Scans repository files for leaked PII, National Insurance numbers, Bank Account/Sort codes,
and sensitive identifiers before committing.
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# Regex Patterns for Common PII
PATTERNS = {
    "UK National Insurance Number": re.compile(r"\b[A-Z]{2}\s*\d{2}\s*\d{2}\s*\d{2}\s*[A-D]\b", re.I),
    "UK Bank Sort Code": re.compile(r"\b\d{2}-\d{2}-\d{2}\b|\b\d{2}\s\d{2}\s\d{2}\b"),
    "UK Bank Account Number (8 digits)": re.compile(r"\b(Account|Acc|A/C)?\s*[:#]?\s*(\d{8})\b", re.I),
    "Credit/Debit Card (16 digits)": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
}

IGNORE_DIRS = {".git", ".venv", "__pycache__", "node_modules"}

def scan_file(path: Path):
    findings = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return findings

    for line_no, line in enumerate(content.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            matches = pattern.findall(line)
            if matches:
                findings.append((line_no, name, line.strip()))
    return findings

def main():
    print("=" * 60)
    print(" PRIVACY & PII PRE-FLIGHT LINTER")
    print("=" * 60)
    
    total_leaks = 0
    scanned_files = 0

    for p in ROOT_DIR.rglob("*"):
        if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts):
            if p.suffix in {".md", ".json", ".txt", ".html", ".py", ".sh"}:
                scanned_files += 1
                leaks = scan_file(p)
                if leaks:
                    print(f"\n[!] WARNING in {p.relative_to(ROOT_DIR)}:")
                    for line_no, pii_type, snippet in leaks:
                        print(f"    Line {line_no} [{pii_type}]: {snippet[:70]}...")
                        total_leaks += len(leaks)

    print("\n" + "=" * 60)
    if total_leaks > 0:
        print(f"[-] FAILED: {total_leaks} sensitive data patterns detected in {scanned_files} files.")
        print("[!] Redact or replace with placeholder tokens before committing.")
        sys.exit(1)
    else:
        print(f"[+] PASSED: {scanned_files} files scanned. Zero unredacted PII leaks found.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
