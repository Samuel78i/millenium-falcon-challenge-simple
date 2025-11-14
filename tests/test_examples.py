"""
Test suite for the 4 provided examples.

These tests verify that our implementation produces the exact expected results
for all the examples given in the challenge specification.

Test design:
- Each example is a separate test method
- We use pytest for clear test output
- We check both the probability AND verify the path makes sense
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import C3PO


class TestExamples:
    """Test cases for the 4 provided examples."""

    def test_example1_impossible_deadline(self):
        """
        Example 1: Impossible to reach Endor in time.

        Scenario:
        - Countdown: 7 days
        - Minimum travel time: 8 days (need to refuel)
        - Expected: 0.0 (impossible)

        This tests that we correctly identify when a mission is impossible.
        """
        c3po = C3PO("examples/example1/millennium-falcon.json")
        odds = c3po.giveMeTheOdds("examples/example1/empire.json")

        assert odds == 0.0, f"Expected 0.0 but got {odds}"

        # Verify no path was found
        path = c3po.get_last_optimal_path()
        assert path is None, "Expected no path for impossible mission"

        encounters = c3po.get_last_encounters()
        assert encounters == -1, "Expected -1 encounters for impossible mission"

    def test_example2_two_encounters(self):
        """
        Example 2: Can reach Endor but must encounter bounty hunters twice.

        Scenario:
        - Countdown: 8 days
        - Optimal route: Tatooine -> Hoth (day 6, encounter) -> refuel (day 7, encounter) -> Endor
        - Encounters: 2
        - Expected: 0.81 (0.9^2)

        This tests:
        - Multi-hop routing
        - Fuel management (must refuel)
        - Unavoidable bounty hunter encounters
        - Probability calculation
        """
        c3po = C3PO("examples/example2/millennium-falcon.json")
        odds = c3po.giveMeTheOdds("examples/example2/empire.json")

        assert odds == 0.81, f"Expected 0.81 but got {odds}"

        # Verify we had exactly 2 encounters
        encounters = c3po.get_last_encounters()
        assert encounters == 2, f"Expected 2 encounters but got {encounters}"

        # Verify a path was found
        path = c3po.get_last_optimal_path()
        assert path is not None, "Expected a valid path"
        assert len(path) > 0, "Path should not be empty"

        # Verify we reached Endor
        assert path[-1].planet == "Endor", "Final destination should be Endor"

        # Verify we finished within countdown
        assert path[-1].day <= 8, "Should finish within countdown of 8 days"

    def test_example3_one_encounter(self):
        """
        Example 3: Can reach Endor with only one bounty hunter encounter.

        Scenario:
        - Countdown: 9 days
        - Optimal route: Tatooine -> Dagobah -> refuel -> Hoth (day 8, encounter) -> Endor
        - Encounters: 1
        - Expected: 0.9 (0.9^1)

        This tests:
        - Alternative route selection
        - Strategic refueling to avoid bounty hunters
        - Minimizing encounters when multiple paths exist
        """
        c3po = C3PO("examples/example3/millennium-falcon.json")
        odds = c3po.giveMeTheOdds("examples/example3/empire.json")

        assert odds == 0.9, f"Expected 0.9 but got {odds}"

        # Verify we had exactly 1 encounter
        encounters = c3po.get_last_encounters()
        assert encounters == 1, f"Expected 1 encounter but got {encounters}"

        # Verify path
        path = c3po.get_last_optimal_path()
        assert path is not None, "Expected a valid path"
        assert path[-1].planet == "Endor", "Should reach Endor"
        assert path[-1].day <= 9, "Should finish within countdown"

    def test_example4_zero_encounters(self):
        """
        Example 4: Can reach Endor while completely avoiding bounty hunters.

        Scenario:
        - Countdown: 10 days
        - Optimal route: Wait/travel strategically to avoid Hoth on days 6, 7, 8
        - Encounters: 0
        - Expected: 1.0 (perfect success)

        This tests:
        - Strategic waiting to avoid bounty hunters
        - Perfect route optimization
        - Probability calculation for zero encounters

        This is the most complex scenario as it requires understanding
        that waiting can be beneficial.
        """
        c3po = C3PO("examples/example4/millennium-falcon.json")
        odds = c3po.giveMeTheOdds("examples/example4/empire.json")

        assert odds == 1.0, f"Expected 1.0 but got {odds}"

        # Verify we had zero encounters
        encounters = c3po.get_last_encounters()
        assert encounters == 0, f"Expected 0 encounters but got {encounters}"

        # Verify path
        path = c3po.get_last_optimal_path()
        assert path is not None, "Expected a valid path"
        assert path[-1].planet == "Endor", "Should reach Endor"
        assert path[-1].day <= 10, "Should finish within countdown"

        # Verify we never visited Hoth on days 6, 7, or 8
        for state in path:
            if state.planet == "Hoth":
                assert state.day not in [6, 7, 8], \
                    f"Should not be on Hoth on days 6, 7, or 8 (was there on day {state.day})"


def run_all_tests():
    """
    Run all tests and print results.

    This is a simple test runner that doesn't require pytest installation.
    """
    test_suite = TestExamples()
    tests = [
        ("Example 1 (Impossible)", test_suite.test_example1_impossible_deadline),
        ("Example 2 (0.81)", test_suite.test_example2_two_encounters),
        ("Example 3 (0.9)", test_suite.test_example3_one_encounter),
        ("Example 4 (1.0)", test_suite.test_example4_zero_encounters),
    ]

    print("Running test suite...\n")
    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name} PASSED")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name} ERROR: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
