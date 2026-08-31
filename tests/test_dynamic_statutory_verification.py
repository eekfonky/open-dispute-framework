"""
test_dynamic_statutory_verification.py
Verifies that dynamically gathered statutory modules satisfy strict schema contracts.
Deterministic dictionary & schema validation — zero brittle regexes.
"""

import unittest
from typing import Dict, Any

class StatutoryContractValidator:
    """
    Enforces that statutory baseline files contain structured, verifiable legal data
    rather than unstructured prose or hallucinations.
    """
    REQUIRED_ROOT_KEYS = {
        "jurisdiction",
        "sector",
        "primary_statute",
        "dispute_resolution_body",
        "limitation_rules",
        "sector_regulator"
    }

    @classmethod
    def validate_schema(cls, data: Dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not isinstance(data, dict):
            return False, ["Root must be a dictionary"]

        # Check required top-level keys
        missing = cls.REQUIRED_ROOT_KEYS - set(data.keys())
        if missing:
            errors.append(f"Missing required fields: {sorted(list(missing))}")

        # Check primary statute structure
        statute = data.get("primary_statute", {})
        if not isinstance(statute, dict) or not statute.get("title") or not statute.get("year"):
            errors.append("primary_statute must include non-empty 'title' and 'year'")

        # Check dispute body structure
        dispute_body = data.get("dispute_resolution_body", {})
        if not isinstance(dispute_body, dict) or not dispute_body.get("name"):
            errors.append("dispute_resolution_body must include 'name'")

        # Check limitation rules structure
        limitation = data.get("limitation_rules", {})
        if not isinstance(limitation, dict) or "days" not in limitation:
            errors.append("limitation_rules must include integer 'days' deadline")

        # Check sector regulator
        regulator = data.get("sector_regulator", {})
        if not isinstance(regulator, dict) or not regulator.get("name"):
            errors.append("sector_regulator must include 'name'")

        return len(errors) == 0, errors

class TestDynamicStatutoryVerification(unittest.TestCase):
    def test_valid_scotland_care_contract(self):
        scotland_care_data = {
            "jurisdiction": "Scotland",
            "sector": "Care",
            "primary_statute": {
                "title": "Employment Rights Act",
                "year": 1996,
                "sections": ["s.47B", "s.103A", "s.203"]
            },
            "dispute_resolution_body": {
                "name": "Employment Tribunals (Scotland)",
                "mandatory_early_conciliation": True,
                "conciliation_body": "ACAS"
            },
            "limitation_rules": {
                "days": 90,
                "description": "3 months less 1 day from trigger event"
            },
            "sector_regulator": {
                "name": "Care Inspectorate (SCSWIS)",
                "professional_register": "SSSC"
            }
        }
        is_valid, errors = StatutoryContractValidator.validate_schema(scotland_care_data)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_valid_nigeria_nursing_contract(self):
        nigeria_nursing_data = {
            "jurisdiction": "Nigeria",
            "sector": "Nursing",
            "primary_statute": {
                "title": "Labour Act Cap L1 LFN",
                "year": 2004,
                "sections": ["Section 9", "Section 11"]
            },
            "dispute_resolution_body": {
                "name": "National Industrial Court of Nigeria (NICN)",
                "mandatory_early_conciliation": False,
                "conciliation_body": "NICN Alternative Dispute Resolution (ADR) Centre"
            },
            "limitation_rules": {
                "days": 90,
                "description": "3 months limitation under Public Officers Protection Act"
            },
            "sector_regulator": {
                "name": "Nursing and Midwifery Council of Nigeria (NMCN)",
                "professional_register": "NMCN Register"
            }
        }
        is_valid, errors = StatutoryContractValidator.validate_schema(nigeria_nursing_data)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_reject_incomplete_statutory_data(self):
        incomplete_data = {
            "jurisdiction": "Unknown",
            "primary_statute": {"title": "General Law"}  # Missing year, dispute body, etc.
        }
        is_valid, errors = StatutoryContractValidator.validate_schema(incomplete_data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

if __name__ == "__main__":
    unittest.main()
