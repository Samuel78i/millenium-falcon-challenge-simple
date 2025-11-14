#!/usr/bin/env python3
"""
Master test runner - runs all test suites.

This script runs both the example tests and edge case tests,
providing a comprehensive validation of the solution.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import test runners
from tests.test_examples import run_all_tests as run_examples
from tests.test_edge_cases import run_edge_case_tests


def main():
    """Run all test suites."""
    print("=" * 70)
    print(" MILLENNIUM FALCON MISSION CALCULATOR - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()

    # Run example tests
    print("PART 1: Required Examples")
    print("-" * 70)
    examples_passed = run_examples()
    print()

    # Run edge case tests
    print("PART 2: Edge Cases & Error Handling")
    print("-" * 70)
    edge_cases_passed = run_edge_case_tests()
    print()

    # Summary
    print("=" * 70)
    print(" OVERALL RESULTS")
    print("=" * 70)

    if examples_passed and edge_cases_passed:
        print("✓ ALL TESTS PASSED!")
        print()
        print("The solution correctly handles:")
        print("  • All 4 required examples")
        print("  • Edge cases and error conditions")
        print("  • Input validation")
        print("  • Algorithm correctness")
        print()
        print("Ready for submission! 🚀")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print()
        if not examples_passed:
            print("  ⚠️  Required examples failed - fix these first!")
        if not edge_cases_passed:
            print("  ⚠️  Edge cases failed - review error handling")
        return 1


if __name__ == "__main__":
    sys.exit(main())
