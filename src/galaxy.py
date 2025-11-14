"""
Galaxy graph representation and navigation utilities.

This module builds a graph structure from the routes data, allowing efficient
pathfinding and neighbor lookups.

Key design decisions:
- Use adjacency list for O(1) neighbor lookups
- Support bidirectional routes automatically
- Validate graph connectivity
"""

from typing import Dict, List, Set
from collections import defaultdict

from .models import Route


class Galaxy:
    """
    Represents the galaxy as a graph of planets connected by hyperspace routes.

    The graph is undirected (routes work both ways) and weighted (each route
    has a travel time).

    Attributes:
        _adjacency: Maps each planet to a list of (neighbor_planet, travel_time) tuples
        _planets: Set of all planet names in the galaxy
    """

    def __init__(self, routes: List[Route]):
        """
        Build the galaxy graph from a list of routes.

        Args:
            routes: List of Route objects representing hyperspace connections

        Raises:
            ValueError: If routes list is empty
        """
        if not routes:
            raise ValueError("Cannot create galaxy with no routes")

        # Adjacency list: planet -> [(neighbor, travel_time), ...]
        # Using defaultdict avoids KeyError when accessing planets
        self._adjacency: Dict[str, List[tuple[str, int]]] = defaultdict(list)
        self._planets: Set[str] = set()

        # Build bidirectional graph
        for route in routes:
            # Add edge in both directions since routes are bidirectional
            self._adjacency[route.origin].append((route.destination, route.travel_time))
            self._adjacency[route.destination].append((route.origin, route.travel_time))

            # Track all planet names
            self._planets.add(route.origin)
            self._planets.add(route.destination)

    def get_neighbors(self, planet: str) -> List[tuple[str, int]]:
        """
        Get all planets reachable from the given planet via a single hyperspace jump.

        Args:
            planet: Name of the planet to get neighbors for

        Returns:
            List of (neighbor_planet, travel_time) tuples

        Example:
            >>> galaxy.get_neighbors("Tatooine")
            [("Dagobah", 6), ("Hoth", 6)]
        """
        return self._adjacency.get(planet, [])

    def has_planet(self, planet: str) -> bool:
        """
        Check if a planet exists in the galaxy.

        Args:
            planet: Name of the planet to check

        Returns:
            True if the planet exists in the route network
        """
        return planet in self._planets

    def get_all_planets(self) -> Set[str]:
        """
        Get the set of all planets in the galaxy.

        Returns:
            Set of planet names
        """
        return self._planets.copy()

    def is_connected(self, start: str, end: str) -> bool:
        """
        Check if there's any path between two planets (ignoring fuel/time constraints).

        This uses BFS to determine graph connectivity.

        Args:
            start: Starting planet
            end: Destination planet

        Returns:
            True if any path exists between the planets

        Note:
            This doesn't consider fuel or time constraints - it only checks
            if the planets are in the same connected component of the graph.
        """
        if not self.has_planet(start) or not self.has_planet(end):
            return False

        if start == end:
            return True

        # BFS for connectivity check
        visited: Set[str] = {start}
        queue: List[str] = [start]

        while queue:
            current = queue.pop(0)

            for neighbor, _ in self.get_neighbors(current):
                if neighbor == end:
                    return True

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Galaxy(planets={len(self._planets)}, routes={sum(len(neighbors) for neighbors in self._adjacency.values()) // 2})"
