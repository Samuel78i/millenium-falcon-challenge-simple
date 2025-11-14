# Solution Verification Guide

This document provides step-by-step instructions to verify the solution works correctly.

---

## ✅ Verification Checklist

### 1. Run All Tests
```bash
python3 run_all_tests.py
```

**Expected result:**
```
✓ ALL TESTS PASSED!
Ready for submission! 🚀
```

**What this verifies:**
- ✅ All 4 required examples produce correct probabilities
- ✅ Edge cases are handled properly
- ✅ Error handling works correctly

---

### 2. Verify Example 1 (Impossible)
```bash
python3 give-me-the-odds.py examples/example1/millennium-falcon.json examples/example1/empire.json
```

**Expected output:**
```
❌ MISSION IMPOSSIBLE
The Millennium Falcon cannot reach Endor within the countdown.
```

**Expected probability:** `0.0`

**Why:** Minimum travel time is 8 days (need to refuel), but countdown is only 7 days.

---

### 3. Verify Example 2 (81%)
```bash
python3 give-me-the-odds.py examples/example2/millennium-falcon.json examples/example2/empire.json --verbose
```

**Expected probability:** `0.81`

**Expected encounters:** `2`

**Route:** Tatooine → Hoth (day 6, encounter #1) → Refuel (day 7, encounter #2) → Endor

**Calculation:** 0.9^2 = 0.81 ✓

---

### 4. Verify Example 3 (90%)
```bash
python3 give-me-the-odds.py examples/example3/millennium-falcon.json examples/example3/empire.json --verbose
```

**Expected probability:** `0.9`

**Expected encounters:** `1`

**Route:** Tatooine → Dagobah → Refuel → Hoth (day 8, encounter #1) → Endor

**Calculation:** 0.9^1 = 0.9 ✓

---

### 5. Verify Example 4 (100%)
```bash
python3 give-me-the-odds.py examples/example4/millennium-falcon.json examples/example4/empire.json --verbose
```

**Expected probability:** `1.0`

**Expected encounters:** `0`

**Route:** Includes waiting on Dagobah to avoid bounty hunters on Hoth during days 6-8

**Calculation:** 0.9^0 = 1.0 ✓

**Key insight:** This example demonstrates the "waiting" strategy to avoid bounty hunters.

---

## 🔍 Manual Testing

### Test the Library API

Create a test file `test_manual.py`:
```python
from src import C3PO

# Test Example 2
c3po = C3PO("examples/example2/millennium-falcon.json")
odds = c3po.giveMeTheOdds("examples/example2/empire.json")

print(f"Probability: {odds}")  # Should print: 0.81
print(f"Encounters: {c3po.get_last_encounters()}")  # Should print: 2
print(c3po.format_optimal_path())  # Should show the route
```

Run it:
```bash
python3 test_manual.py
```

---

## 🧪 Testing Edge Cases

### Test Invalid File
```bash
python3 give-me-the-odds.py nonexistent.json empire.json
```

**Expected:** Error message about file not found

### Test Invalid JSON
Create a file with invalid JSON and test error handling.

---

## 📊 Performance Verification

### Check Algorithm Speed
```python
import time
from src import C3PO

start = time.time()
c3po = C3PO("examples/example4/millennium-falcon.json")
odds = c3po.giveMeTheOdds("examples/example4/empire.json")
elapsed = time.time() - start

print(f"Computation time: {elapsed*1000:.2f}ms")
# Should be well under 100ms for these small examples
```

---

## 📝 Code Quality Checks

### Check Type Hints (Optional - requires mypy)
```bash
# Install mypy if available
pip install mypy

# Run type checker
mypy src/ --strict
```

### Check Code Style (Optional - requires pylint)
```bash
# Install pylint if available
pip install pylint

# Check code quality
pylint src/
```

---

## ✨ Visual Verification

### Compare Output Format

**Example 2 with verbose flag should show:**
```
============================================================
✓ Success Probability: 81.0%

👍 Good odds. Acceptable risk.

------------------------------------------------------------
OPTIMAL ROUTE:
------------------------------------------------------------
Day 0: Depart from Tatooine (Fuel: 6/6)
Day 6: Arrive at Hoth (Fuel: 0/6) ⚠️  BOUNTY HUNTERS!
Day 7: Refuel on Hoth (Fuel: 6/6) ⚠️  BOUNTY HUNTERS!
Day 8: Arrive at Endor (Fuel: 5/6)

Total encounters: 2
Success probability: 81.0%
============================================================
```

---

## 🎯 Final Verification Matrix

| Test | Command | Expected Result | Status |
|------|---------|----------------|--------|
| All Tests | `python3 run_all_tests.py` | All pass | ✅ |
| Example 1 | CLI with example1 | 0.0 | ✅ |
| Example 2 | CLI with example2 | 0.81 | ✅ |
| Example 3 | CLI with example3 | 0.9 | ✅ |
| Example 4 | CLI with example4 | 1.0 | ✅ |
| Edge Cases | Edge case test suite | All pass | ✅ |
| Library API | Python import | Works | ✅ |
| Error Handling | Invalid input | Graceful error | ✅ |

---