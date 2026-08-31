"""
test_arithmetic_invariants.py
Verifies mathematical invariants across remuneration, holiday pay, notice pay, and settlement totals.
Standard library unittest - universal across all platforms and currencies.
"""

import unittest

def calculate_monthly_gross(hourly_rate: float, weekly_hours: float) -> float:
    return round((hourly_rate * weekly_hours * 52) / 12, 2)

def calculate_holiday_pay(hourly_rate: float, accrued_hours: float) -> float:
    return round(hourly_rate * accrued_hours, 2)

def calculate_notice_pay(hourly_rate: float, weekly_hours: float, notice_weeks: int) -> float:
    return round(hourly_rate * weekly_hours * notice_weeks, 2)

def calculate_total_package(ex_gratia: float, holiday_pay: float, notice_pay: float) -> float:
    return round(ex_gratia + holiday_pay + notice_pay, 2)

class TestArithmeticInvariants(unittest.TestCase):
    def test_monthly_gross_invariants(self):
        cases = [
            (13.45, 25.0, 1457.08),
            (15.00, 37.5, 2437.50),
            (20.00, 40.0, 3466.67),
            (5000.00, 40.0, 866666.67),  # e.g. Naira / Yen
        ]
        for hourly, hours, expected in cases:
            with self.subTest(hourly=hourly, hours=hours):
                calculated = calculate_monthly_gross(hourly, hours)
                self.assertAlmostEqual(calculated, expected, delta=0.05)

    def test_holiday_pay_invariants(self):
        cases = [
            (13.45, 99.0, 1331.55),
            (15.00, 50.0, 750.00),
            (25.50, 10.5, 267.75),
        ]
        for hourly, hours, expected in cases:
            with self.subTest(hourly=hourly, hours=hours):
                self.assertEqual(calculate_holiday_pay(hourly, hours), expected)

    def test_package_reconciliation_invariant(self):
        ex_gratia = 3922.00
        holiday = 1331.00
        notice = 336.25
        total = 5589.25
        self.assertEqual(calculate_total_package(ex_gratia, holiday, notice), total)

if __name__ == "__main__":
    unittest.main()
