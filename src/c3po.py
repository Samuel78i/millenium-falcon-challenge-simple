"""
C3PO - Mission Probability Calculator

This module provides the main interface for calculating the odds of successfully
reaching Endor before the Death Star destroys it.

The C3PO class matches the exact specification from the challenge:
- Constructor takes millennium-falcon.json path
- giveMeTheOdds() method takes empire.json path and returns success probability
"""

from typing import Optional, List

from .parser import parse_millennium_falcon, parse_empire
from .galaxy import Galaxy
from .pathfinder import PathFinder, calculate_success_probability
from .models import SearchState


class C3PO:
    """
    Protocol droid programmed to compute mission success probabilities.

    This class encapsulates all the logic needed to:
    1. Load and validate Millennium Falcon specifications
    2. Build a galaxy graph from routes
    3. Process Empire intelligence
    4. Calculate optimal routes
    5. Compute success probabilities

    Usage:
        >>> c3po = C3PO("millennium-falcon.json")
        >>> odds = c3po.giveMeTheOdds("empire.json")
        >>> print(f"Success probability: {odds}")
    """

    def __init__(self, millenniumFalconJsonFilePath: str):
        """
        Initialize C3PO with Millennium Falcon specifications.

        This constructor:
        1. Parses the millennium-falcon.json file
        2. Validates the data
        3. Builds the galaxy graph
        4. Stores configuration for later use

        Args:
            millenniumFalconJsonFilePath: Path to the millennium-falcon.json file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ParseError: If the JSON is invalid or missing required fields
            ValueError: If the data validation fails

        Design note:
            Following the exact signature from the challenge specification.
            We use camelCase for the parameter name to match the spec.
        """
        # Parse the Millennium Falcon configuration
        self.falcon_data = parse_millennium_falcon(millenniumFalconJsonFilePath)

        # Build the galaxy graph from routes
        self.galaxy = Galaxy(self.falcon_data.routes)

        # Store for later reference
        self.autonomy = self.falcon_data.autonomy

        # These will be set when giveMeTheOdds() is called
        self._last_optimal_path: Optional[List[SearchState]] = None
        self._last_encounters: Optional[int] = None

    def giveMeTheOdds(self, empireJsonFilePath: str) -> float:
        """
        Calculate the probability of successfully reaching Endor.

        This method:
        1. Parses Empire intelligence data
        2. Runs the pathfinding algorithm to find the optimal route
        3. Calculates the success probability based on bounty hunter encounters

        The algorithm finds the path from Tatooine to Endor that:
        - Arrives within the countdown deadline
        - Minimizes bounty hunter encounters
        - Respects fuel constraints

        Args:
            empireJsonFilePath: Path to the empire.json file

        Returns:
            Probability of success as a float between 0.0 and 1.0:
            - 0.0: Impossible to reach Endor in time
            - 0.0 < x < 1.0: Possible but risky (will encounter bounty hunters)
            - 1.0: Can reach Endor without any bounty hunter encounters

        Raises:
            FileNotFoundError: If the empire.json file doesn't exist
            ParseError: If the JSON is invalid
            ValueError: If planet names don't exist in the galaxy

        Example:
            >>> c3po = C3PO("examples/example1/millennium-falcon.json")
            >>> odds = c3po.giveMeTheOdds("examples/example1/empire.json")
            >>> print(odds)
            0.0

        Design note:
            Following the exact signature from the challenge specification.
            Using camelCase for the parameter name to match the spec.
        """
        # Parse Empire intelligence
        empire_data = parse_empire(empireJsonFilePath)

        # Get bounty hunter schedule as a fast lookup structure
        bounty_hunter_schedule = empire_data.get_bounty_hunter_schedule()

        # Initialize pathfinder with current mission parameters
        pathfinder = PathFinder(
            galaxy=self.galaxy,
            autonomy=self.autonomy,
            bounty_hunter_schedule=bounty_hunter_schedule
        )

        # Find the optimal path (minimum encounters)
        # Hardcoded: Start = "Tatooine", Destination = "Endor" (from problem statement)
        min_encounters, optimal_path = pathfinder.find_min_encounters(
            start="Tatooine",
            destination="Endor",
            countdown=empire_data.countdown
        )

        # Store for debugging/display purposes
        self._last_encounters = min_encounters
        self._last_optimal_path = optimal_path

        # If no path found, return 0
        if min_encounters == -1:
            return 0.0

        # Calculate success probability from encounters
        probability = calculate_success_probability(min_encounters)

        return probability

    def get_last_optimal_path(self) -> Optional[List[SearchState]]:
        """
        Get the optimal path found in the last giveMeTheOdds() call.

        This is useful for debugging and displaying the route to users.

        Returns:
            List of SearchState objects representing the path, or None if
            no path was found or giveMeTheOdds() hasn't been called yet.

        Example:
            >>> c3po = C3PO("millennium-falcon.json")
            >>> odds = c3po.giveMeTheOdds("empire.json")
            >>> path = c3po.get_last_optimal_path()
            >>> for state in path:
            ...     print(f"Day {state.day}: {state.planet}")
        """
        return self._last_optimal_path

    def get_last_encounters(self) -> Optional[int]:
        """
        Get the number of bounty hunter encounters in the last optimal path.

        Returns:
            Number of encounters, or None if giveMeTheOdds() hasn't been called yet.
            Returns -1 if no path was found.
        """
        return self._last_encounters

    def format_optimal_path(self) -> str:
        """
        Format the last optimal path as a human-readable string.

        This is a nice-to-have feature that makes the output more user-friendly.
        It shows the exact route taken, fuel management decisions, and risks.

        Returns:
            Formatted string describing the journey, or a message if no path exists.

        Example output:
            Day 0: Depart from Tatooine (Fuel: 6/6)
            Day 6: Arrive at Hoth (Fuel: 0/6) ⚠️ BOUNTY HUNTERS!
            Day 7: Refuel on Hoth (Fuel: 6/6) ⚠️ BOUNTY HUNTERS!
            Day 8: Arrive at Endor (Fuel: 5/6)

            Total encounters: 2
            Success probability: 81.0%
        """
        if self._last_optimal_path is None:
            return "No path calculated yet. Call giveMeTheOdds() first."

        if self._last_encounters == -1:
            return "No valid path found within the countdown."

        lines = []
        prev_state = None

        for i, state in enumerate(self._last_optimal_path):
            # Determine action taken
            if i == 0:
                action = "Depart from"
            elif prev_state and prev_state.planet != state.planet:
                action = "Arrive at"
            elif prev_state and state.fuel > prev_state.fuel:
                action = "Refuel on"
            elif prev_state and state.fuel == prev_state.fuel:
                action = "Wait on"
            else:
                action = "At"

            # Format fuel level
            fuel_info = f"(Fuel: {state.fuel}/{self.autonomy})"

            # Check for bounty hunters
            warning = ""
            if i > 0:  # Don't check starting state
                prev_day = prev_state.day if prev_state else 0
                if state.encounters > (prev_state.encounters if prev_state else 0):
                    warning = " ⚠️  BOUNTY HUNTERS!"

            lines.append(f"Day {state.day}: {action} {state.planet} {fuel_info}{warning}")
            prev_state = state

        # Add summary
        lines.append("")
        lines.append(f"Total encounters: {self._last_encounters}")

        probability = calculate_success_probability(self._last_encounters)
        lines.append(f"Success probability: {probability * 100:.1f}%")

        return "\n".join(lines)
