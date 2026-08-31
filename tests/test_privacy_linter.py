"""
test_privacy_linter.py
Verifies that the privacy linter actively catches and fails on PII leaks.
"""

import unittest
from tools.verify_privacy import PATTERNS

class TestPrivacyLinter(unittest.TestCase):
    def test_detect_uk_national_insurance_number(self):
        sample = "The employee's NI number is QQ123456C for payroll."
        matches = PATTERNS["UK National Insurance Number"].findall(sample)
        self.assertEqual(len(matches), 1)

    def test_detect_bank_sort_code(self):
        sample = "Transfer pay to sort code 80-22-60."
        matches = PATTERNS["UK Bank Sort Code"].findall(sample)
        self.assertEqual(len(matches), 1)

    def test_detect_credit_card(self):
        sample = "Corporate expenses charged to 4532 0154 9874 1234."
        matches = PATTERNS["Credit/Debit Card (16 digits)"].findall(sample)
        self.assertEqual(len(matches), 1)

    def test_clean_text_passes(self):
        sample = "Employee Claim v Organization Ltd. Case Log initialised."
        for name, pattern in PATTERNS.items():
            matches = pattern.findall(sample)
            self.assertEqual(len(matches), 0, f"False positive on pattern: {name}")

if __name__ == "__main__":
    unittest.main()
