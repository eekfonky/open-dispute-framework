#!/usr/bin/env python3
"""
setup.py
Interactive onboarding wizard for Open Dispute Framework.
Initialises case architecture, calculates service length, and configures ground truth facts.json.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent
EVIDENCE_DIR = ROOT_DIR / "evidence"
CASE_DIR = ROOT_DIR / "case"
FACTS_FILE = EVIDENCE_DIR / "facts.json"
LOG_FILE = CASE_DIR / "log.md"

def prompt(text, default=""):
    val = input(f"{text} [{default}]: ").strip()
    return val if val else default

def main():
    print("=" * 65)
    print("      OPEN DISPUTE FRAMEWORK (ODF) - INITIALISATION WIZARD      ")
    print("=" * 65)
    print("This wizard configures an immutable, verified case architecture for AI agents.\n")

    # 1. Jurisdiction & Sector
    print("--- [Step 1: Jurisdiction & Industry Sector] ---")
    jurisdiction = prompt("Location / Jurisdiction (e.g. Scotland, England & Wales, Nigeria, Canada)", "Scotland")
    sector = prompt("Industry / Sector (e.g. Care / Social Care, Nursing, Office Admin, Tech)", "Care / Social Care")

    # 2. Employment Facts
    print("\n--- [Step 2: Employment Basics] ---")
    start_date_str = prompt("Continuous Employment Start Date (YYYY-MM-DD)", "2025-04-21")
    contracted_hours = float(prompt("Contracted Weekly Hours", "25.0"))
    hourly_rate = float(prompt("Hourly Rate (£ or local currency)", "13.45"))
    monthly_gross = float(prompt("Monthly Gross Pay (from payslip)", "1457.08"))

    # Calculate Service Length
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        now = datetime.now()
        months_service = (now.year - start_date.year) * 12 + (now.month - start_date.month)
    except Exception:
        months_service = 0

    # 3. Dispute & Key Dates
    print("\n--- [Step 3: Dispute Timeline & Fuses] ---")
    incident_date = prompt("Date of Last Incident / Detriment / Dismissal (YYYY-MM-DD)", datetime.now().strftime("%Y-%m-%d"))
    settlement_offered = prompt("Has a settlement agreement proposal been received? (y/n)", "y").lower() == "y"

    ex_gratia = 0.0
    holiday_hours = 0.0
    holiday_amount = 0.0
    notice_weeks = 1
    notice_amount = 0.0
    total_package = 0.0
    legal_contrib = 0.0
    proposal_date = ""

    if settlement_offered:
        proposal_date = prompt("Date Settlement Proposal Received (YYYY-MM-DD)", datetime.now().strftime("%Y-%m-%d"))
        ex_gratia = float(prompt("Ex-gratia / Termination Payment Offered", "3922.00"))
        holiday_hours = float(prompt("Accrued Holiday Hours to Pay", "99.0"))
        holiday_amount = float(prompt("Accrued Holiday Pay Amount", str(round(holiday_hours * hourly_rate, 2))))
        notice_weeks = int(prompt("Notice Weeks to be Paid in Lieu (PILON)", "1"))
        notice_amount = float(prompt("Notice Pay Amount", str(round(notice_weeks * contracted_hours * hourly_rate, 2))))
        total_package = round(ex_gratia + holiday_amount + notice_amount, 2)
        legal_contrib = float(prompt("Employer Legal Contribution (+ VAT)", "350.00"))

    # Construct facts.json
    facts_data = {
        "_comment": "Ground truth facts for AI agents. Edit with care; verified by tools/verify_facts.py.",
        "jurisdiction": {
            "name": jurisdiction,
            "sector": sector,
            "limitation_months": 3
        },
        "employment": {
            "start_date": start_date_str,
            "calculated_service_months": months_service,
            "continuous_service_over_2_years": months_service >= 24
        },
        "remuneration": {
            "contracted_weekly_hours": contracted_hours,
            "hourly_rate": hourly_rate,
            "monthly_gross": monthly_gross
        },
        "dates": {
            "last_incident_or_dismissal": incident_date,
            "settlement_proposal_served": proposal_date if settlement_offered else None
        },
        "settlement_terms": {
            "offered": settlement_offered,
            "ex_gratia_amount": ex_gratia,
            "holiday_pay_hours": holiday_hours,
            "holiday_pay_amount": holiday_amount,
            "notice_weeks": notice_weeks,
            "notice_pay_amount": notice_amount,
            "total_gross_package": total_package,
            "employer_legal_contribution": legal_contrib
        }
    }

    EVIDENCE_DIR.mkdir(exist_ok=True, parents=True)
    CASE_DIR.mkdir(exist_ok=True, parents=True)

    with open(FACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(facts_data, f, indent=2)

    # Initialise log.md if not present
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Case Chronological Ledger\n")
            f.write(f"> Append-only historical log for case memory across AI sessions.\n\n")
            f.write(f"## [{datetime.now().strftime('%Y-%m-%d')}] Case Initialised via ODF Wizard\n")
            f.write(f"- Jurisdiction: **{jurisdiction}**\n")
            f.write(f"- Industry / Sector: **{sector}**\n")
            f.write(f"- Service Length: **{months_service} months** (Start: {start_date_str})\n")
            f.write(f"- Ground truth financial arithmetic written to `evidence/facts.json`.\n")

    print("\n" + "=" * 65)
    print("[+] Case architecture initialised successfully!")
    print(f"[+] Ground truth written to: evidence/facts.json")
    print(f"[+] Case ledger created: case/log.md")
    print("=" * 65)
    print("\nNext step: Run verification tools:")
    print("  python tools/verify_facts.py")
    print("  python tools/limitation_calc.py")
    print("=" * 65)

if __name__ == "__main__":
    main()
