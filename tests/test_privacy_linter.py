"""
test_privacy_linter.py
Verifies privacy checking using deterministic Luhn validation and keyword token checks.
Zero regexes.
"""

import unittest
from tools.verify_privacy import check_line_privacy, is_luhn_valid

class TestPrivacyLinter(unittest.TestCase):
    def test_luhn_card_validation(self):
        # Deterministic check for valid vs invalid cards
        self.assertTrue(is_luhn_valid("4532015498741237"))  # Valid Luhn 16-digit
        self.assertFalse(is_luhn_valid("4532015498741238")) # Invalid Luhn 16-digit

    def test_detect_unredacted_pii_marker(self):
        sample = "Employee Details - National Insurance: QQ123456C"
        findings = check_line_privacy(sample)
        self.assertEqual(len(findings), 1)
        self.assertIn("National Insurance", findings[0][0])

    def test_redacted_marker_passes(self):
        sample = "Employee Details - National Insurance: [REDACTED_NI]"
        findings = check_line_privacy(sample)
        self.assertEqual(len(findings), 0)

    def test_clean_case_text_passes(self):
        sample = "Grievance submitted by Claimant against Organisation Ltd."
        findings = check_line_privacy(sample)
        self.assertEqual(len(findings), 0)

if __name__ == "__main__":
    unittest.main()
