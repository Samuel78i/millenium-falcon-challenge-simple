# Millennium Falcon Challenge - Simple Solution

This is my solution for the Dataiku technical challenge.

## How to Run

### Test all examples:
```bash
python3 c3po_simple.py
```

### Use in code:
```python
from c3po_simple import C3PO

c3po = C3PO("examples/example2/millennium-falcon.json")
odds = c3po.giveMeTheOdds("examples/example2/empire.json")
print(f"Success probability: {odds}")
```

## My Approach

I used a **Breadth-First Search (BFS)** algorithm to explore all possible paths from Tatooine to Endor.

### Key Ideas:

1. **State**: Each state tracks (planet, day, fuel, encounters)

2. **Actions**: From each state, I can:
   - Travel to a neighbor planet (if I have enough fuel)
   - Refuel (takes 1 day)
   - Wait (takes 1 day, useful to avoid bounty hunters)

3. **Goal**: Find the path that reaches Endor within the countdown with minimum bounty hunter encounters

4. **Probability**: Calculate using formula `0.9^k` where k is number of encounters

### Algorithm Steps:

1. Start at Tatooine on day 0 with full fuel
2. Use BFS queue to explore all possible states
3. For each state, try traveling, refueling, or waiting
4. Track visited states to avoid redundant exploration
5. Find minimum encounters needed to reach Endor
6. Calculate probability from encounters

### Time Complexity:
O(P × D × F) where:
- P = number of planets
- D = countdown days
- F = fuel levels (0 to autonomy)

For the examples given, this runs very fast (under 10ms).

## Testing

All 4 examples pass:
- Example 1: 0.0 (impossible - can't reach in time)
- Example 2: 0.81 (2 encounters)
- Example 3: 0.9 (1 encounter)
- Example 4: 1.0 (0 encounters - waiting strategy works!)

## Files

- `c3po_simple.py` - Main solution (single file, ~150 lines)
- `README_SIMPLE.md` - This file

## Notes

The algorithm handles all the tricky parts:
- Bidirectional routes (can travel both ways)
- Fuel management (must refuel when needed)
- Strategic waiting (Example 4 shows this working)
- Bounty hunter encounters (both when arriving and refueling)

---

**Time spent**: About 2-3 hours including testing and debugging.

**Language choice**: Python - good for quick implementation and easy to understand.
