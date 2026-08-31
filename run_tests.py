#!/usr/bin/env python3
"""
run_tests.py
Universal test runner for Open Dispute Framework using Python stdlib unittest.
Runs everywhere with zero external dependencies.
"""

import sys
import unittest

def main():
    print("=" * 65)
    print("   OPEN DISPUTE FRAMEWORK — DETERMINISTIC TDD TEST SUITE")
    print("=" * 65)
    
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 65)
    if result.wasSuccessful():
        print("[+] ALL INVARIANT & VERIFICATION TESTS PASSED SUCCESSFULLY.")
        print("=" * 65)
        sys.exit(0)
    else:
        print(f"[-] TEST SUITE FAILED: {len(result.failures)} failures, {len(result.errors)} errors.")
        print("=" * 65)
        sys.exit(1)

if __name__ == "__main__":
    main()
