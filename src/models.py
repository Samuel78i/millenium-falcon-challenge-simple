"""
Data models for the Millennium Falcon mission.

This module defines the data structures used to represent:
- Routes between planets
- Millennium Falcon specifications (autonomy, available routes)
- Empire intelligence (countdown, bounty hunter locations)
- Bounty hunter encounters

Using dataclasses provides:
- Clear type hints
- Automatic __init__, __repr__, __eq__ methods
- Immutability (frozen=True) for safety
"""

from dataclasses import dataclass
from typing import List, Dict, Set


@dataclass(frozen=True)
class Route:
    """
    Represents a bidirectional hyperspace route between two planets.

    Attributes:
        origin: Name of the origin planet
        destination: Name of the destination planet
        travel_time: Number of days needed to travel this route

    Note: Routes are bidirectional - you can travel from origin to destination
    or vice versa with the same travel time.
    """
    origin: str
    destination: str
    travel_time: int

    def __post_init__(self):
        """Validate route data after initialization."""
        if not self.origin or not self.destination:
            raise ValueError("Origin and destination cannot be empty")
        if self.travel_time <= 0:
            raise ValueError(f"Travel time must be positive, got {self.travel_time}")


@dataclass(frozen=True)
class BountyHunter:
    """
    Represents a bounty hunter's planned location.

    Attributes:
        planet: Name of the planet where bounty hunters will be present
        day: Day number when bounty hunters will be there (0 = mission start)
    """
    planet: str
    day: int

    def __post_init__(self):
        """Validate bounty hunter data."""
        if not self.planet:
            raise ValueError("Planet name cannot be empty")
        if self.day < 0:
            raise ValueError(f"Day must be non-negative, got {self.day}")


@dataclass
class MillenniumFalconData:
    """
    Contains all data about the Millennium Falcon's capabilities.

    Attributes:
        autonomy: Maximum days the ship can travel without refueling
        routes: List of all available hyperspace routes in the galaxy
    """
    autonomy: int
    routes: List[Route]

    def __post_init__(self):
        """Validate Millennium Falcon data."""
        if self.autonomy <= 0:
            raise ValueError(f"Autonomy must be positive, got {self.autonomy}")
        if not self.routes:
            raise ValueError("Routes list cannot be empty")


@dataclass
class EmpireData:
    """
    Contains intercepted intelligence about Empire's plans.

    Attributes:
        countdown: Number of days before Death Star destroys Endor
        bounty_hunters: List of known bounty hunter locations and schedules
    """
    countdown: int
    bounty_hunters: List[BountyHunter]

    def __post_init__(self):
        """Validate Empire data."""
        if self.countdown < 0:
            raise ValueError(f"Countdown must be non-negative, got {self.countdown}")

    def get_bounty_hunter_schedule(self) -> Dict[str, Set[int]]:
        """
        Create a fast lookup structure for bounty hunter presence.

        Returns:
            Dictionary mapping planet names to sets of days when bounty hunters
            are present. This allows O(1) lookup to check if a planet is dangerous
            on a given day.

        Example:
            {"Hoth": {6, 7, 8}, "Dagobah": {5}}
        """
        schedule: Dict[str, Set[int]] = {}
        for hunter in self.bounty_hunters:
            if hunter.planet not in schedule:
                schedule[hunter.planet] = set()
            schedule[hunter.planet].add(hunter.day)
        return schedule


@dataclass(frozen=True)
class SearchState:
    """
    Represents a state in the pathfinding search space.

    This is used during the BFS/Dijkstra search to track all relevant
    information about a particular point in the journey.

    Attributes:
        planet: Current planet location
        day: Current day number (0 = mission start)
        fuel: Remaining fuel (in days of travel)
        encounters: Number of times we've encountered bounty hunters so far

    Note: This class is frozen (immutable) so it can be used as a dictionary key
    for efficient duplicate detection during search.
    """
    planet: str
    day: int
    fuel: int
    encounters: int

    def __post_init__(self):
        """Validate state data."""
        if self.day < 0:
            raise ValueError(f"Day must be non-negative, got {self.day}")
        if self.fuel < 0:
            raise ValueError(f"Fuel must be non-negative, got {self.fuel}")
        if self.encounters < 0:
            raise ValueError(f"Encounters must be non-negative, got {self.encounters}")
