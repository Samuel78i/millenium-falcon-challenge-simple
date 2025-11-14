#!/usr/bin/env python3
"""
Command-line interface for the Millennium Falcon mission calculator.

This script provides an easy-to-use CLI for computing mission success odds.

Usage:
    python give-me-the-odds.py <millennium-falcon.json> <empire.json>

Example:
    python give-me-the-odds.py examples/example1/millennium-falcon.json examples/example1/empire.json

Features:
- Displays success probability
- Shows the optimal route taken
- Provides detailed journey information
- Handles errors gracefully with helpful messages
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import C3PO, ParseError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate the odds of the Millennium Falcon successfully reaching Endor.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s examples/example1/millennium-falcon.json examples/example1/empire.json
  %(prog)s data/falcon.json data/empire.json --verbose

May the Force be with you!
        """
    )

    parser.add_argument(
        "millennium_falcon",
        help="Path to the millennium-falcon.json file"
    )

    parser.add_argument(
        "empire",
        help="Path to the empire.json file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed path information"
    )

    parser.add_argument(
        "--path-only",
        action="store_true",
        help="Only show the path, not the probability"
    )

    args = parser.parse_args()

    try:
        # Initialize C3PO with Millennium Falcon data
        print(f"Loading Millennium Falcon specifications from {args.millennium_falcon}...")
        c3po = C3PO(args.millennium_falcon)

        # Calculate odds
        print(f"Analyzing Empire intelligence from {args.empire}...")
        odds = c3po.giveMeTheOdds(args.empire)

        print()
        print("=" * 60)

        # Display results
        if odds == 0.0:
            print("❌ MISSION IMPOSSIBLE")
            print()
            print("The Millennium Falcon cannot reach Endor within the countdown.")
            print("Perhaps we should negotiate with the Empire... or run!")
        else:
            if not args.path_only:
                print(f"✓ Success Probability: {odds * 100:.1f}%")
                print()

                # Qualitative assessment
                if odds == 1.0:
                    print("🎯 Perfect! We can avoid all bounty hunters.")
                elif odds >= 0.9:
                    print("⭐ Excellent odds! Low risk mission.")
                elif odds >= 0.7:
                    print("👍 Good odds. Acceptable risk.")
                elif odds >= 0.5:
                    print("⚠️  Moderate risk. Proceed with caution.")
                else:
                    print("⚠️  HIGH RISK! Consider alternative strategies.")

            # Show path if requested or if verbose
            if args.verbose or args.path_only:
                print()
                print("-" * 60)
                print("OPTIMAL ROUTE:")
                print("-" * 60)
                print(c3po.format_optimal_path())

        print("=" * 60)

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)

    except ParseError as e:
        print(f"❌ Error: Invalid JSON data - {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"❌ Error: Invalid data - {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
