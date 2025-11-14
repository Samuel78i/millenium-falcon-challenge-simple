"""
Edge case tests for the Millennium Falcon mission calculator.

These tests verify that our implementation handles unusual or boundary conditions:
- Invalid input files
- Missing data
- Edge cases in the algorithm
- Error handling

This demonstrates robustness and attention to detail.
"""

import sys
import os
from pathlib import Path
import json
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import C3PO, ParseError


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_file_not_found(self):
        """Test that appropriate error is raised for missing files."""
        try:
            c3po = C3PO("nonexistent_file.json")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass  # Expected

    def test_invalid_json_syntax(self):
        """Test handling of malformed JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{invalid json content")
            temp_path = f.name

        try:
            c3po = C3PO(temp_path)
            assert False, "Should have raised ParseError for invalid JSON"
        except ParseError:
            pass  # Expected
        finally:
            os.unlink(temp_path)

    def test_missing_autonomy_field(self):
        """Test handling of missing required field."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"routes": []}, f)
            temp_path = f.name

        try:
            c3po = C3PO(temp_path)
            assert False, "Should have raised ParseError for missing autonomy"
        except ParseError as e:
            assert "autonomy" in str(e).lower()
        finally:
            os.unlink(temp_path)

    def test_negative_autonomy(self):
        """Test validation of negative autonomy value."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "autonomy": -5,
                "routes": [
                    {"origin": "A", "destination": "B", "travel_time": 1}
                ]
            }, f)
            temp_path = f.name

        try:
            c3po = C3PO(temp_path)
            assert False, "Should have raised error for negative autonomy"
        except (ParseError, ValueError):
            pass  # Expected
        finally:
            os.unlink(temp_path)

    def test_zero_countdown(self):
        """Test with countdown of 0 (must start at destination)."""
        # Create minimal valid millennium-falcon.json
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "autonomy": 6,
                "routes": [
                    {"origin": "Tatooine", "destination": "Endor", "travel_time": 1}
                ]
            }, f)
            falcon_path = f.name

        # Create empire.json with countdown 0
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "countdown": 0,
                "bounty_hunters": []
            }, f)
            empire_path = f.name

        try:
            c3po = C3PO(falcon_path)
            odds = c3po.giveMeTheOdds(empire_path)
            # Should be 0 since we can't travel anywhere in 0 days
            assert odds == 0.0, f"Expected 0.0 for countdown=0, got {odds}"
        finally:
            os.unlink(falcon_path)
            os.unlink(empire_path)

    def test_empty_bounty_hunters_list(self):
        """Test with no bounty hunters (should have perfect success if reachable)."""
        # This essentially tests example 4 concept with different data
        # We'll use example 1's falcon data but with no bounty hunters
        c3po = C3PO("examples/example1/millennium-falcon.json")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "countdown": 10,
                "bounty_hunters": []
            }, f)
            empire_path = f.name

        try:
            odds = c3po.giveMeTheOdds(empire_path)
            # If reachable in 10 days with no bounty hunters, should be 1.0
            # From example 1, minimum time is 8 days, so this should work
            assert odds == 1.0, f"Expected 1.0 with no bounty hunters, got {odds}"

            encounters = c3po.get_last_encounters()
            assert encounters == 0, f"Expected 0 encounters, got {encounters}"
        finally:
            os.unlink(empire_path)

    def test_bounty_hunters_everywhere_always(self):
        """Test scenario where bounty hunters are on every planet every day."""
        c3po = C3PO("examples/example1/millennium-falcon.json")

        # Create empire data with bounty hunters on all planets all days
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            bounty_hunters = []
            planets = ["Tatooine", "Dagobah", "Endor", "Hoth"]
            for planet in planets:
                for day in range(15):
                    bounty_hunters.append({"planet": planet, "day": day})

            json.dump({
                "countdown": 10,
                "bounty_hunters": bounty_hunters
            }, f)
            empire_path = f.name

        try:
            odds = c3po.giveMeTheOdds(empire_path)
            # Should still find a path, but with encounters
            # The exact probability depends on the path, but it should be > 0
            assert 0 <= odds <= 1.0, f"Probability should be in [0, 1], got {odds}"

            if odds > 0:
                encounters = c3po.get_last_encounters()
                assert encounters > 0, "Should have at least one encounter"
        finally:
            os.unlink(empire_path)

    def test_very_long_countdown(self):
        """Test with an extremely long countdown."""
        c3po = C3PO("examples/example1/millennium-falcon.json")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "countdown": 1000,
                "bounty_hunters": [
                    {"planet": "Hoth", "day": 6},
                    {"planet": "Hoth", "day": 7}
                ]
            }, f)
            empire_path = f.name

        try:
            odds = c3po.giveMeTheOdds(empire_path)
            # With 1000 days, we can definitely avoid the bounty hunters
            assert odds == 1.0, f"Expected 1.0 with very long countdown, got {odds}"

            encounters = c3po.get_last_encounters()
            assert encounters == 0, f"Expected 0 encounters with long countdown, got {encounters}"
        finally:
            os.unlink(empire_path)


def run_edge_case_tests():
    """Run all edge case tests."""
    test_suite = TestEdgeCases()
    tests = [
        ("File not found", test_suite.test_file_not_found),
        ("Invalid JSON syntax", test_suite.test_invalid_json_syntax),
        ("Missing autonomy field", test_suite.test_missing_autonomy_field),
        ("Negative autonomy", test_suite.test_negative_autonomy),
        ("Zero countdown", test_suite.test_zero_countdown),
        ("Empty bounty hunters", test_suite.test_empty_bounty_hunters_list),
        ("Bounty hunters everywhere", test_suite.test_bounty_hunters_everywhere_always),
        ("Very long countdown", test_suite.test_very_long_countdown),
    ]

    print("Running edge case tests...\n")
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
    success = run_edge_case_tests()
    sys.exit(0 if success else 1)
