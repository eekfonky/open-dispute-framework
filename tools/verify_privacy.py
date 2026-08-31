#!/usr/bin/env python3
"""
verify_privacy.py
Deterministic PII and privacy verification using structural token analysis and Luhn validation.
Zero brittle regexes.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
IGNORE_DIRS = {".git", ".venv", "__pycache__", "node_modules"}

def is_luhn_valid(card_num_str: str) -> bool:
    """Deterministic Luhn algorithm check for credit/debit card numbers."""
    digits = [int(d) for d in card_num_str if d.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def check_line_privacy(line: str) -> list:
    """Token-based scanner checking for unredacted sensitive values."""
    findings = []
    
    # 1. Check for unredacted 16-digit cards using deterministic Luhn checksum
    clean_digits = "".join(ch for ch in line if ch.isdigit())
    if len(clean_digits) >= 15:
        # Check substrings of length 15 and 16
        for length in (16, 15):
            for i in range(len(clean_digits) - length + 1):
                chunk = clean_digits[i:i+length]
                if is_luhn_valid(chunk):
                    findings.append(("Payment Card Number (Luhn Validated)", chunk))
                    break

    # 2. Check for explicit unredacted sensitive keywords with raw numbers
    lower_line = line.lower()
    sensitive_markers = ["national insurance:", "ni number:", "sort code:", "account number:", "ssn:"]
    for marker in sensitive_markers:
        if marker in lower_line:
            idx = lower_line.find(marker) + len(marker)
            sub = line[idx:].strip()
            # If it's not redacted with standard placeholders [REDACTED...
            if sub and not sub.startswith("[") and not sub.startswith("<"):
                tokens = [t for t in sub.split() if any(c.isalnum() for c in t)]
                if tokens:
                    findings.append((f"Unredacted {marker.replace(':', '').title()}", tokens[0]))

    return findings

def scan_file(path: Path):
    findings = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for line_no, line in enumerate(content.splitlines(), start=1):
        line_findings = check_line_privacy(line)
        for leak_type, val in line_findings:
            findings.append((line_no, leak_type, line.strip()))
    return findings

def main():
    print("=" * 60)
    print(" PRIVACY & PII PRE-FLIGHT LINTER (DETERMINISTIC)")
    print("=" * 60)
    
    total_leaks = 0
    scanned_files = 0

    for p in ROOT_DIR.rglob("*"):
        if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts):
            if p.suffix in {".md", ".json", ".txt", ".html", ".py", ".sh"}:
                scanned_files += 1
                leaks = scan_file(p)
                if leaks:
                    print(f"\n[!] PRIVACY LEAK in {p.relative_to(ROOT_DIR)}:")
                    for line_no, pii_type, snippet in leaks:
                        print(f"    Line {line_no} [{pii_type}]: {snippet[:70]}...")
                        total_leaks += 1

    print("\n" + "=" * 60)
    if total_leaks > 0:
        print(f"[-] FAILED: {total_leaks} sensitive items detected across {scanned_files} files.")
        print("[!] Use standard tokens like [REDACTED_NI], [REDACTED_ACC] before committing.")
        sys.exit(1)
    else:
        print(f"[+] PASSED: {scanned_files} files verified. Zero unredacted PII leaks.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
