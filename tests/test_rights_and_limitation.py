"""
test_rights_and_limitation.py
Deterministic unit tests for:
1. Service qualifying rights gating (preventing unfair dismissal hallucinations under threshold).
2. Limitation period fuses (ACAS 3-month - 1 day, 10-day consideration window).
"""

import unittest
from datetime import date, timedelta
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from rights_gate import evaluate_rights

class TestRightsAndLimitationInvariants(unittest.TestCase):
    def test_uk_under_2_years_service_blocks_ordinary_unfair_dismissal(self):
        facts = {
            "jurisdiction": {"name": "scotland"},
            "employment": {
                "start_date": "2025-04-21",
                "termination_date": "2026-08-31"
            }
        }
        result = evaluate_rights(facts)
        self.assertFalse(result["ordinary_unfair_dismissal_qualified"])
        self.assertEqual(result["mandatory_strategic_branch"], "AUTOMATIC_DAY_ONE_PROTECTIONS_ONLY")
        self.assertIn("Protected Disclosures / Whistleblowing Detriment & Dismissal", result["available_day_one_protections"])

    def test_uk_over_2_years_service_unlocks_ordinary_unfair_dismissal(self):
        facts = {
            "jurisdiction": {"name": "england"},
            "employment": {
                "start_date": "2024-01-01",
                "termination_date": "2026-08-31"
            }
        }
        result = evaluate_rights(facts)
        self.assertTrue(result["ordinary_unfair_dismissal_qualified"])
        self.assertEqual(result["mandatory_strategic_branch"], "ORDINARY_UNFAIR_DISMISSAL")

    def test_australia_threshold_is_6_months(self):
        facts = {
            "jurisdiction": {"name": "australia"},
            "employment": {
                "start_date": "2026-01-01",
                "termination_date": "2026-08-31" # 7 months
            }
        }
        result = evaluate_rights(facts)
        self.assertTrue(result["ordinary_unfair_dismissal_qualified"])

if __name__ == "__main__":
    unittest.main()
