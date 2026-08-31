#!/usr/bin/env python3
"""
rights_gate.py
Deterministic Qualifying Rights & Statutory Exclusions Gate.
Evaluates continuous service duration and prevents the AI agent from asserting
statutory rights that require qualifying service periods (e.g. 2-yr UK Unfair Dismissal).
Forces branching to Day-1 automatic protections (Whistleblowing, Protected Characteristics, H&S).
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
FACTS_FILE = ROOT_DIR / "evidence" / "facts.json"

# Qualifying thresholds by jurisdiction (in months) for standard Unfair Dismissal
QUALIFYING_THRESHOLDS_MONTHS = {
    "scotland": 24,
    "england": 24,
    "wales": 24,
    "northern_ireland": 12,
    "australia": 6,       # 12 for small businesses (<15 employees)
    "ireland": 12,
    "nigeria": 0,         # Contract / Trade Dispute basis
    "united_states": 0,   # At-will doctrine default
}

def calculate_service_months(start_str: str, end_str: str) -> int:
    fmt = "%Y-%m-%d"
    d_start = datetime.strptime(start_str, fmt).date()
    d_end = datetime.strptime(end_str, fmt).date() if end_str else date.today()
    return (d_end.year - d_start.year) * 12 + (d_end.month - d_start.month)

def evaluate_rights(facts: dict) -> dict:
    emp = facts.get("employment", {})
    jur = facts.get("jurisdiction", {})
    dates = facts.get("dates", {})
    
    start_date = emp.get("continuous_start_date") or emp.get("start_date")
    end_date = emp.get("termination_date") or dates.get("last_incident_or_dismissal") or dates.get("settlement_proposal_served")
    country = jur.get("name", "scotland").lower()
    
    if not start_date:
        return {"error": "Missing start_date in facts.json"}

    service_months = emp.get("calculated_service_months") or calculate_service_months(start_date, end_date)
    threshold = QUALIFYING_THRESHOLDS_MONTHS.get(country, 24)
    
    has_ordinary_unfair_dismissal = service_months >= threshold
    
    return {
        "service_months": service_months,
        "qualifying_threshold_months": threshold,
        "ordinary_unfair_dismissal_qualified": has_ordinary_unfair_dismissal,
        "mandatory_strategic_branch": "ORDINARY_UNFAIR_DISMISSAL" if has_ordinary_unfair_dismissal else "AUTOMATIC_DAY_ONE_PROTECTIONS_ONLY",
        "available_day_one_protections": [
            "Protected Disclosures / Whistleblowing Detriment & Dismissal",
            "Equality Act / Protected Characteristics Discrimination",
            "Health & Safety Retaliation",
            "Statutory Wage Deductions / Holiday Pay Enforcement",
            "Breach of Contract / Wrongful Dismissal (Notice Pay)"
        ] if not has_ordinary_unfair_dismissal else [
            "Ordinary Unfair Dismissal",
            "Automatic Unfair Dismissal",
            "Protected Disclosures",
            "Discrimination"
        ]
    }

def main():
    if not FACTS_FILE.exists():
        print("[-] Error: evidence/facts.json not found.")
        sys.exit(1)
        
    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        facts = json.load(f)
        
    analysis = evaluate_rights(facts)
    print("=" * 65)
    print("   DETERMINISTIC STATUTORY RIGHTS & SERVICE GATE")
    print("=" * 65)
    print(f"[*] Continuous Service Calculated : {analysis['service_months']} months")
    print(f"[*] Jurisdiction Qualifying Bar   : {analysis['qualifying_threshold_months']} months")
    print(f"[*] Ordinary UD Qualified         : {analysis['ordinary_unfair_dismissal_qualified']}")
    print(f"[*] Mandatory Strategic Directive : {analysis['mandatory_strategic_branch']}")
    print("\n[+] Legally Viable Grounds:")
    for ground in analysis["available_day_one_protections"]:
        print(f"    - {ground}")
    print("=" * 65)

if __name__ == "__main__":
    main()
