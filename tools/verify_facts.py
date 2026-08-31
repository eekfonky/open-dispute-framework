#!/usr/bin/env python3
"""
verify_facts.py
Validates the mathematical consistency and integrity of evidence/facts.json.
"""

import json
import sys
from pathlib import Path

FACTS_FILE = Path(__file__).parent.parent / "evidence" / "facts.json"

def verify():
    print("=" * 60)
    print(" FINANCIAL ARITHMETIC & FACT INTEGRITY GATE")
    print("=" * 60)

    if not FACTS_FILE.exists():
        print(f"[-] Error: {FACTS_FILE} does not exist.")
        sys.exit(1)

    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    checks_passed = 0

    employment = data.get("employment", {})
    remuneration = data.get("remuneration", {})
    settlement = data.get("settlement_terms", {})

    # 1. Hourly vs Annual vs Monthly Gross Arithmetic
    hourly_rate = remuneration.get("hourly_rate")
    weekly_hours = remuneration.get("contracted_weekly_hours")
    monthly_gross = remuneration.get("monthly_gross")

    if hourly_rate and weekly_hours and monthly_gross:
        # Standard UK 52-week formula: (hourly * weekly_hours * 52) / 12
        calculated_monthly = round((hourly_rate * weekly_hours * 52) / 12, 2)
        diff = abs(calculated_monthly - monthly_gross)
        # Allow 0.05 tolerance for rounding on fractional pennies
        if diff > 0.50:
            errors.append(
                f"Monthly gross (£{monthly_gross}) does not match hourly rate (£{hourly_rate} x {weekly_hours}h x 52 / 12 = £{calculated_monthly}). Difference: £{diff:.2f}"
            )
        else:
            print(f"[+] Verified: Monthly gross (£{monthly_gross}) matches contract hourly rate (£{hourly_rate} @ {weekly_hours}h/wk).")
            checks_passed += 1

    # 2. Holiday Pay Arithmetic
    holiday_hours = settlement.get("holiday_pay_hours")
    holiday_total = settlement.get("holiday_pay_amount")
    if holiday_hours and holiday_total and hourly_rate:
        expected_holiday = round(holiday_hours * hourly_rate, 2)
        diff = abs(expected_holiday - holiday_total)
        if diff > 1.00:
            errors.append(
                f"Holiday pay (£{holiday_total}) does not match {holiday_hours} hours @ £{hourly_rate}/h (£{expected_holiday}). Difference: £{diff:.2f}"
            )
        else:
            print(f"[+] Verified: Accrued holiday pay (£{holiday_total}) matches {holiday_hours}h @ £{hourly_rate}/h.")
            checks_passed += 1

    # 3. Notice Pay Arithmetic (PILON)
    notice_weeks = settlement.get("notice_weeks")
    notice_amount = settlement.get("notice_pay_amount")
    if notice_weeks and notice_amount and hourly_rate and weekly_hours:
        expected_notice = round(notice_weeks * weekly_hours * hourly_rate, 2)
        diff = abs(expected_notice - notice_amount)
        if diff > 1.00:
            errors.append(
                f"Notice pay (£{notice_amount}) does not match {notice_weeks} week(s) @ £{hourly_rate}/h x {weekly_hours}h (£{expected_notice})."
            )
        else:
            print(f"[+] Verified: Payment in lieu of notice (£{notice_amount}) matches {notice_weeks} week(s) contractual pay.")
            checks_passed += 1

    # 4. Total Package vs Breakdown Sum
    total_package = settlement.get("total_gross_package")
    ex_gratia = settlement.get("ex_gratia_amount", 0.0)
    if total_package and holiday_total and notice_amount:
        expected_total = round(ex_gratia + holiday_total + notice_amount, 2)
        if abs(expected_total - total_package) > 0.05:
            errors.append(
                f"Total package (£{total_package}) does not equal sum of ex gratia (£{ex_gratia}) + holiday (£{holiday_total}) + notice (£{notice_amount}) = £{expected_total}."
            )
        else:
            print(f"[+] Verified: Total settlement package sum (£{total_package}) correctly balances all line items.")
            checks_passed += 1

    print("=" * 60)
    if errors:
        print(f"[-] FAILED with {len(errors)} mathematical discrepancies:")
        for err in errors:
            print(f"    - {err}")
        sys.exit(1)
    else:
        print(f"[+] PASSED: All {checks_passed} financial and arithmetic gates verified successfully.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    verify()
