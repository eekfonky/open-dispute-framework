#!/usr/bin/env python3
"""
limitation_calc.py
Calculates critical statutory limitation fuses from evidence/facts.json.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

FACTS_FILE = Path(__file__).parent.parent / "evidence" / "facts.json"

def parse_date(d_str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(d_str, fmt)
        except ValueError:
            pass
    return None

def main():
    if not FACTS_FILE.exists():
        print(f"[-] Error: {FACTS_FILE} not found. Run setup.py first.")
        sys.exit(1)

    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    jurisdiction = data.get("jurisdiction", {}).get("name", "Unknown")
    dates = data.get("dates", {})
    last_event_str = dates.get("last_incident_or_dismissal")

    print("=" * 60)
    print(f" STATUTORY LIMITATION & DISPUTE FUSE CALCULATOR")
    print(f" Jurisdiction: {jurisdiction}")
    print("=" * 60)

    if not last_event_str:
        print("[!] No 'last_incident_or_dismissal' date found in facts.json.")
        sys.exit(0)

    last_event = parse_date(last_event_str)
    if not last_event:
        print(f"[-] Invalid date format for: {last_event_str}")
        sys.exit(1)

    print(f"Trigger Event Date: {last_event.strftime('%d %B %Y')}\n")

    # UK Standard Rules
    if "scotland" in jurisdiction.lower() or "england" in jurisdiction.lower():
        # 3 months less 1 day
        # Calculate ~3 months (90-92 days approximation or exact calendar month)
        month = last_event.month + 3
        year = last_event.year
        if month > 12:
            month -= 12
            year += 1
        day = min(last_event.day, 28)
        limit_date = datetime(year, month, day) - timedelta(days=1)

        print(f"1. ACAS Early Conciliation Hard Deadline (3 months less 1 day):")
        print(f"   --> DEADLINE: {limit_date.strftime('%A, %d %B %Y')}")
        days_left = (limit_date.date() - datetime.now().date()).days
        if days_left < 0:
            print(f"   --> STATUS: EXPIRED ({abs(days_left)} days ago) [CRITICAL]")
        else:
            print(f"   --> STATUS: {days_left} days remaining")

        # 7-day Interim Relief for Whistleblowing (ERA 1996 s.128)
        interim_date = last_event + timedelta(days=7)
        print(f"\n2. Whistleblowing Interim Relief Application Fuse (7 days):")
        print(f"   --> DEADLINE: {interim_date.strftime('%A, %d %B %Y')}")

    # General / International Fallback
    else:
        limit_months = data.get("jurisdiction", {}).get("limitation_months", 3)
        limit_date = last_event + timedelta(days=int(limit_months * 30.4))
        print(f"1. Statutory Limitation Deadline ({limit_months} months rule):")
        print(f"   --> DEADLINE: {limit_date.strftime('%A, %d %B %Y')}")

    # 10-day Settlement consideration window (if proposal served)
    proposal_str = dates.get("settlement_proposal_served")
    if proposal_str:
        prop_date = parse_date(proposal_str)
        if prop_date:
            ten_day_date = prop_date + timedelta(days=10)
            print(f"\n3. ACAS Minimum Settlement Consideration Window (10 calendar days):")
            print(f"   --> Offer Served: {prop_date.strftime('%d %B %Y')}")
            print(f"   --> Consideration Expiry: {ten_day_date.strftime('%A, %d %B %Y')}")

    print("=" * 60)

if __name__ == "__main__":
    main()
