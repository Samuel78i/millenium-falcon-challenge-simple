# Quick Start Guide

**Time to run:** 2 minutes

## Step 1: Verify Python Version

```bash
python3 --version
# Should be Python 3.8 or higher
```

## Step 2: Run Tests

```bash
# Run all tests (required examples + edge cases)
python3 run_all_tests.py
```

Expected output:
```
✓ ALL TESTS PASSED!
Ready for submission! 🚀
```

## Step 3: Try the CLI

```bash
# Example 1 (Impossible mission)
python3 give-me-the-odds.py examples/example1/millennium-falcon.json examples/example1/empire.json

# Example 2 (81% success) with detailed route
python3 give-me-the-odds.py examples/example2/millennium-falcon.json examples/example2/empire.json --verbose

# Example 4 (100% success) with detailed route
python3 give-me-the-odds.py examples/example4/millennium-falcon.json examples/example4/empire.json --verbose
```

## Step 4: See the Demo

```bash
python3 demo.py
```

## Using as a Library

```python
from src import C3PO

# Initialize
c3po = C3PO("millennium-falcon.json")

# Calculate odds
probability = c3po.giveMeTheOdds("empire.json")

print(f"Success: {probability * 100:.1f}%")

# Get detailed path
print(c3po.format_optimal_path())
```

## Project Structure

```
├── src/                      # Source code
│   ├── c3po.py              # Main API class ⭐
│   ├── pathfinder.py        # Core algorithm
│   ├── galaxy.py            # Graph representation
│   ├── models.py            # Data structures
│   └── parser.py            # JSON handling
├── tests/                    # Test suites
│   ├── test_examples.py     # 4 required examples
│   └── test_edge_cases.py   # 8 edge case tests
├── give-me-the-odds.py      # CLI interface
├── run_all_tests.py         # Master test runner
├── demo.py                  # Usage demonstration
└── SOLUTION.md              # Full documentation
```

## Key Features

✅ **Correct:** Passes all 4 required examples
✅ **Robust:** Handles edge cases and errors gracefully
✅ **Well-tested:** 12 comprehensive tests
✅ **Documented:** Full type hints and docstrings
✅ **User-friendly:** CLI with helpful output
✅ **Clean code:** Organized, readable, maintainable

## Need Help?

See **SOLUTION.md** for:
- Full algorithm explanation
- Design decisions
- Complexity analysis
- Python learning points

---

**Ready to submit!** All tests pass and examples work correctly. ✨
