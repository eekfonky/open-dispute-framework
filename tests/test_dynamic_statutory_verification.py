"""
test_dynamic_statutory_verification.py
Tests that dynamic statutory frameworks gathered for ANY country/region and sector
adhere to strict, verifiable structural criteria (No Hallucination standard).
"""

import re
import unittest

class StatutoryDocValidator:
    @staticmethod
    def validate_content(content: str) -> dict:
        return {
            "has_primary_statute": bool(re.search(r"(Act|Code|Statute|Law|Decree|Order)\s+(\d{4}|\bCap\b)", content, re.I)),
            "has_specific_sections": bool(re.search(r"(s\.\s*\d+|section\s+\d+|article\s+\d+|clause\s+\d+)", content, re.I)),
            "has_dispute_body": bool(re.search(r"(Tribunal|Court|Commission|Arbitration|Board|Panel)", content, re.I)),
            "has_limitation_fuse": bool(re.search(r"(\d+\s*(day|month|year|week)s?|limitation|deadline|time limit)", content, re.I)),
            "has_prescribed_regulator": bool(re.search(r"(Inspectorate|Council|Executive|Authority|Commission|Ombudsman)", content, re.I)),
        }

class TestDynamicStatutoryVerification(unittest.TestCase):
    def test_valid_scottish_care_framework(self):
        sample = """
        # Statutory Framework: Scotland (Care Sector)
        * Primary Act: Employment Rights Act 1996 (ERA 1996)
        * Whistleblowing Detriment: s.47B and s.103A
        * Dispute Body: Employment Tribunals (Scotland)
        * Limitation Fuse: 3 months less 1 day from trigger event
        * Sector Regulator: Care Inspectorate (SCSWIS) and SSSC
        """
        results = StatutoryDocValidator.validate_content(sample)
        for check, passed in results.items():
            self.assertTrue(passed, f"Check failed: {check}")

    def test_valid_nigeria_nursing_framework(self):
        sample = """
        # Statutory Framework: Nigeria (Nursing Sector)
        * Primary Act: Labour Act Cap L1 LFN 2004
        * Specific Provisions: Section 9, Section 11 (Notice and Termination)
        * Dispute Body: National Industrial Court of Nigeria (NICN)
        * Limitation Fuse: 3 months limitation under Public Officers Protection Act
        * Sector Regulator: Nursing and Midwifery Council of Nigeria (NMCN)
        """
        results = StatutoryDocValidator.validate_content(sample)
        for check, passed in results.items():
            self.assertTrue(passed, f"Check failed: {check}")

    def test_reject_vague_hallucinated_framework(self):
        sample_hallucination = """
        # Some Generic Framework
        Workers have general human rights and the employer must be fair.
        You can sue them if they break company policy.
        """
        results = StatutoryDocValidator.validate_content(sample_hallucination)
        self.assertFalse(results["has_primary_statute"])
        self.assertFalse(results["has_specific_sections"])
        self.assertFalse(results["has_dispute_body"])

if __name__ == "__main__":
    unittest.main()
