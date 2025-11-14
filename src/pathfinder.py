"""
Pathfinding algorithm to find the optimal route with minimum bounty hunter encounters.

This module implements a modified Breadth-First Search (BFS) algorithm that explores
the state space of (planet, day, fuel, encounters) to find all paths that reach
the destination within the countdown, then selects the one with minimum risk.

Algorithm complexity:
- Time: O(P × D × F) where P=planets, D=countdown days, F=fuel states
- Space: O(P × D × F) for state tracking

Why BFS instead of Dijkstra?
- All actions (travel, refuel, wait) have unit time cost (1 day or more)
- We want to explore all paths within the countdown
- We track encounters separately and minimize them
- BFS is simpler and sufficient for this problem size
"""

from typing import Dict, Set, List, Optional, Tuple
from collections import deque

from .models import SearchState
from .galaxy import Galaxy


class PathFinder:
    """
    Finds optimal routes through the galaxy considering fuel, time, and risk.

    This class encapsulates the pathfinding logic, separating it from the
    data models and the main C3PO interface.
    """

    def __init__(
        self,
        galaxy: Galaxy,
        autonomy: int,
        bounty_hunter_schedule: Dict[str, Set[int]]
    ):
        """
        Initialize the pathfinder.

        Args:
            galaxy: Galaxy graph containing planets and routes
            autonomy: Maximum days the Millennium Falcon can travel without refueling
            bounty_hunter_schedule: Map of planet -> set of days with bounty hunters
        """
        self.galaxy = galaxy
        self.autonomy = autonomy
        self.bounty_hunter_schedule = bounty_hunter_schedule

    def find_min_encounters(
        self,
        start: str,
        destination: str,
        countdown: int
    ) -> Tuple[int, Optional[List[SearchState]]]:
        """
        Find the path with minimum bounty hunter encounters.

        This is the core algorithm. It uses BFS to explore all possible paths
        from start to destination within the countdown, tracking the minimum
        number of bounty hunter encounters needed.

        Strategy:
        1. Start at the origin planet on day 0 with full fuel
        2. Explore all possible actions at each state:
           - Travel to adjacent planets (if fuel allows)
           - Refuel (takes 1 day)
           - Wait (takes 1 day, useful to avoid bounty hunters)
        3. Track visited states to avoid redundant exploration
        4. Record the minimum encounters needed to reach destination
        5. Reconstruct the optimal path

        Args:
            start: Starting planet (Tatooine)
            destination: Target planet (Endor)
            countdown: Maximum days allowed

        Returns:
            Tuple of:
            - Minimum number of bounty hunter encounters (-1 if impossible)
            - Optimal path as list of SearchState objects (None if impossible)

        Algorithm explanation for beginners:
        - We use a queue (FIFO) to explore states level-by-level (BFS)
        - Each state represents: where we are, what day it is, fuel left, encounters so far
        - We avoid revisiting states we've already explored better
        - We track how we got to each state so we can reconstruct the path
        """
        # Early exit: check if destination exists and is reachable
        if not self.galaxy.has_planet(start):
            raise ValueError(f"Start planet '{start}' not found in galaxy")
        if not self.galaxy.has_planet(destination):
            raise ValueError(f"Destination planet '{destination}' not found in galaxy")

        # Quick check: is there any path at all (ignoring constraints)?
        if not self.galaxy.is_connected(start, destination):
            return -1, None

        # Initial state: at start planet, day 0, full fuel, no encounters
        initial_state = SearchState(
            planet=start,
            day=0,
            fuel=self.autonomy,
            encounters=0
        )

        # BFS queue: stores (state, path_to_state) tuples
        queue: deque = deque([(initial_state, [initial_state])])

        # Track best result found so far
        min_encounters = float('inf')
        best_path: Optional[List[SearchState]] = None

        # Visited tracking: For each (planet, day, fuel), track minimum encounters
        # This prevents exploring worse paths to the same state
        # Key: (planet, day, fuel) -> Value: minimum encounters to reach this state
        visited: Dict[Tuple[str, int, int], int] = {}
        visited[(start, 0, self.autonomy)] = 0

        while queue:
            current_state, path = queue.popleft()

            # If we've exceeded the countdown, skip this path
            if current_state.day > countdown:
                continue

            # If we've already found a better solution, skip worse paths
            if current_state.encounters >= min_encounters:
                continue

            # Success! We've reached the destination
            if current_state.planet == destination:
                if current_state.encounters < min_encounters:
                    min_encounters = current_state.encounters
                    best_path = path
                continue

            # Explore all possible actions from current state:

            # ACTION 1: TRAVEL to adjacent planets
            for neighbor, travel_time in self.galaxy.get_neighbors(current_state.planet):
                # Can we make this jump with our current fuel?
                if travel_time <= current_state.fuel:
                    new_day = current_state.day + travel_time
                    new_fuel = current_state.fuel - travel_time

                    # Check if we encounter bounty hunters at destination
                    new_encounters = current_state.encounters
                    if self._has_bounty_hunters(neighbor, new_day):
                        new_encounters += 1

                    new_state = SearchState(
                        planet=neighbor,
                        day=new_day,
                        fuel=new_fuel,
                        encounters=new_encounters
                    )

                    # Only explore if this is a better path to this state
                    if self._should_visit(new_state, visited):
                        visited[(neighbor, new_day, new_fuel)] = new_encounters
                        queue.append((new_state, path + [new_state]))

            # ACTION 2: REFUEL (takes 1 day, restores fuel to maximum)
            # Only refuel if we're not already at max fuel (optimization)
            if current_state.fuel < self.autonomy:
                new_day = current_state.day + 1

                # Check if bounty hunters are here while we refuel
                new_encounters = current_state.encounters
                if self._has_bounty_hunters(current_state.planet, new_day):
                    new_encounters += 1

                new_state = SearchState(
                    planet=current_state.planet,
                    day=new_day,
                    fuel=self.autonomy,  # Full tank after refueling
                    encounters=new_encounters
                )

                if self._should_visit(new_state, visited):
                    visited[(current_state.planet, new_day, self.autonomy)] = new_encounters
                    queue.append((new_state, path + [new_state]))

            # ACTION 3: WAIT (stay on planet for 1 day without refueling)
            # This is useful to avoid bounty hunters by timing our movements
            # Only wait if we're not at max fuel (otherwise, waiting is same as refueling)
            if current_state.fuel == self.autonomy:
                new_day = current_state.day + 1

                # Check if bounty hunters are here while we wait
                new_encounters = current_state.encounters
                if self._has_bounty_hunters(current_state.planet, new_day):
                    new_encounters += 1

                new_state = SearchState(
                    planet=current_state.planet,
                    day=new_day,
                    fuel=self.autonomy,  # Fuel stays the same
                    encounters=new_encounters
                )

                if self._should_visit(new_state, visited):
                    visited[(current_state.planet, new_day, self.autonomy)] = new_encounters
                    queue.append((new_state, path + [new_state]))

        # Return results
        if min_encounters == float('inf'):
            return -1, None  # No path found within countdown
        else:
            return int(min_encounters), best_path

    def _has_bounty_hunters(self, planet: str, day: int) -> bool:
        """
        Check if bounty hunters are present on a planet on a given day.

        Args:
            planet: Planet name
            day: Day number

        Returns:
            True if bounty hunters are present
        """
        return planet in self.bounty_hunter_schedule and day in self.bounty_hunter_schedule[planet]

    def _should_visit(
        self,
        state: SearchState,
        visited: Dict[Tuple[str, int, int], int]
    ) -> bool:
        """
        Determine if we should explore a state based on visited history.

        We only visit a state if:
        1. We've never been to (planet, day, fuel) before, OR
        2. We've reached (planet, day, fuel) with fewer encounters than before

        Args:
            state: The state to potentially visit
            visited: Map of (planet, day, fuel) -> minimum encounters

        Returns:
            True if we should explore this state
        """
        key = (state.planet, state.day, state.fuel)

        # Never seen this state before
        if key not in visited:
            return True

        # We've found a better path to this state
        if state.encounters < visited[key]:
            return True

        return False


def calculate_success_probability(encounters: int) -> float:
    """
    Calculate the probability of mission success given number of bounty hunter encounters.

    Formula: P(success) = 1 - P(capture)
    Where: P(capture) = 1 - ∏(1 - 0.1)^k = 1 - (0.9)^k

    Mathematical explanation:
    - Each encounter has 10% capture chance (90% escape chance)
    - For k encounters: probability of escaping all = 0.9^k
    - Probability of being captured at least once = 1 - 0.9^k
    - Probability of success = probability of escaping all = 1 - (1 - 0.9^k) = 0.9^k

    Wait, let me recalculate this...
    Actually: P(capture at least once) = 1 - (0.9)^k
    So: P(success) = 1 - P(capture) = 1 - (1 - (0.9)^k) = (0.9)^k

    Hmm, but the examples suggest otherwise. Let me check:
    - 1 encounter: should give 0.9 (90%)
    - 2 encounters: 1 - (1-0.9) * (1-0.9) = 1 - 0.01 = 0.99? No...

    Actually from the problem statement, the formula is:
    P(captured) = 1 - ∏(1 - p_i) where each p_i = 0.1
    P(captured) = 1 - (1 - 0.1)^k = 1 - 0.9^k
    P(success) = 1 - P(captured) = 1 - (1 - 0.9^k) = 0.9^k

    Let's verify:
    - k=1: 0.9^1 = 0.9 ✓ (matches example)
    - k=2: 0.9^2 = 0.81 ✓ (matches example)
    - k=3: 0.9^3 = 0.729 ≈ 0.73... but example shows 0.271

    Wait, I need to re-read the formula. Looking at the images referenced...
    The formula shows k encounters on the SAME planet count as k separate events.

    Actually, re-reading: "if the Millennium Falcon travels via 2 planets with bounty hunters"
    Looking at example 2: encounters on day 6 and 7 on Hoth = 2 encounters
    Result: 0.81 = 0.9^2 ✓

    So the formula is simply: P(success) = 0.9^k

    Args:
        encounters: Number of times bounty hunters were encountered

    Returns:
        Probability of success (0.0 to 1.0)

    Examples:
        >>> calculate_success_probability(0)
        1.0
        >>> calculate_success_probability(1)
        0.9
        >>> calculate_success_probability(2)
        0.81
    """
    if encounters < 0:
        raise ValueError(f"Encounters must be non-negative, got {encounters}")

    if encounters == 0:
        return 1.0

    # P(success) = 0.9^k
    return 0.9 ** encounters
