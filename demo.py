#!/usr/bin/env python3
"""
Quick demonstration of the Millennium Falcon mission calculator.

This script shows both the library API and CLI usage.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import C3PO


def demo_library_usage():
    """Demonstrate using C3PO as a library."""
    print("=" * 70)
    print(" LIBRARY API DEMONSTRATION")
    print("=" * 70)
    print()

    examples = [
        ("Example 1 (Impossible)", "examples/example1/millennium-falcon.json", "examples/example1/empire.json"),
        ("Example 2 (81%)", "examples/example2/millennium-falcon.json", "examples/example2/empire.json"),
        ("Example 3 (90%)", "examples/example3/millennium-falcon.json", "examples/example3/empire.json"),
        ("Example 4 (100%)", "examples/example4/millennium-falcon.json", "examples/example4/empire.json"),
    ]

    for name, falcon_file, empire_file in examples:
        print(f"Testing: {name}")
        print("-" * 70)

        # Create C3PO instance
        c3po = C3PO(falcon_file)

        # Calculate odds
        odds = c3po.giveMeTheOdds(empire_file)

        # Display results
        print(f"Success Probability: {odds * 100:.1f}%")

        if odds > 0:
            encounters = c3po.get_last_encounters()
            print(f"Bounty Hunter Encounters: {encounters}")

            # Show the path
            print("\nOptimal Route:")
            path = c3po.get_last_optimal_path()
            for state in path:
                print(f"  Day {state.day}: {state.planet} (Fuel: {state.fuel})")
        else:
            print("No valid path found within countdown")

        print()

    print("=" * 70)
    print()


def demo_cli_usage():
    """Show CLI usage examples."""
    print("=" * 70)
    print(" CLI USAGE EXAMPLES")
    print("=" * 70)
    print()

    print("Basic usage:")
    print("  python3 give-me-the-odds.py millennium-falcon.json empire.json")
    print()

    print("Verbose output (shows route):")
    print("  python3 give-me-the-odds.py millennium-falcon.json empire.json --verbose")
    print()

    print("Show only the path:")
    print("  python3 give-me-the-odds.py millennium-falcon.json empire.json --path-only")
    print()

    print("Example with actual files:")
    print("  python3 give-me-the-odds.py \\")
    print("    examples/example2/millennium-falcon.json \\")
    print("    examples/example2/empire.json \\")
    print("    --verbose")
    print()

    print("=" * 70)
    print()


if __name__ == "__main__":
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     MILLENNIUM FALCON MISSION CALCULATOR - DEMONSTRATION        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    # Demo library usage
    demo_library_usage()

    # Show CLI examples
    demo_cli_usage()

    print("For more information, see SOLUTION.md")
    print()
