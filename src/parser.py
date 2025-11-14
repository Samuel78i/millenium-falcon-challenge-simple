"""
JSON file parsers for Millennium Falcon and Empire data.

This module handles reading and validating JSON input files, converting them
into typed data structures with proper error handling.

Design decisions:
- Fail fast with clear error messages for invalid input
- Separate parsing logic from business logic
- Use type hints for clarity
"""

import json
from typing import Any, Dict
from pathlib import Path

from .models import (
    Route,
    BountyHunter,
    MillenniumFalconData,
    EmpireData
)


class ParseError(Exception):
    """Raised when JSON parsing or validation fails."""
    pass


def parse_millennium_falcon(file_path: str) -> MillenniumFalconData:
    """
    Parse the Millennium Falcon configuration from a JSON file.

    Args:
        file_path: Path to the millennium-falcon.json file

    Returns:
        MillenniumFalconData object containing autonomy and routes

    Raises:
        ParseError: If file doesn't exist, is invalid JSON, or has missing/invalid fields
        FileNotFoundError: If the file doesn't exist

    Example JSON format:
        {
          "autonomy": 6,
          "routes": [
            {"origin": "Tatooine", "destination": "Dagobah", "travel_time": 4}
          ]
        }
    """
    try:
        # Read the file
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r') as f:
            data: Dict[str, Any] = json.load(f)

        # Validate required fields
        if 'autonomy' not in data:
            raise ParseError("Missing required field: 'autonomy'")
        if 'routes' not in data:
            raise ParseError("Missing required field: 'routes'")

        # Parse autonomy
        autonomy = data['autonomy']
        if not isinstance(autonomy, int):
            raise ParseError(f"'autonomy' must be an integer, got {type(autonomy).__name__}")

        # Parse routes
        routes_data = data['routes']
        if not isinstance(routes_data, list):
            raise ParseError(f"'routes' must be a list, got {type(routes_data).__name__}")

        routes = []
        for i, route_data in enumerate(routes_data):
            try:
                # Note: JSON uses "travelTime" (camelCase) but we use "travel_time" (snake_case)
                # We'll support both for flexibility
                travel_time = route_data.get('travel_time') or route_data.get('travelTime')

                route = Route(
                    origin=route_data.get('origin', ''),
                    destination=route_data.get('destination', ''),
                    travel_time=travel_time or 0
                )
                routes.append(route)
            except (KeyError, ValueError) as e:
                raise ParseError(f"Invalid route at index {i}: {str(e)}")

        return MillenniumFalconData(autonomy=autonomy, routes=routes)

    except json.JSONDecodeError as e:
        raise ParseError(f"Invalid JSON in {file_path}: {str(e)}")
    except ValueError as e:
        raise ParseError(f"Validation error in {file_path}: {str(e)}")


def parse_empire(file_path: str) -> EmpireData:
    """
    Parse the Empire intelligence data from a JSON file.

    Args:
        file_path: Path to the empire.json file

    Returns:
        EmpireData object containing countdown and bounty hunter locations

    Raises:
        ParseError: If file doesn't exist, is invalid JSON, or has missing/invalid fields
        FileNotFoundError: If the file doesn't exist

    Example JSON format:
        {
          "countdown": 7,
          "bounty_hunters": [
            {"planet": "Hoth", "day": 6}
          ]
        }
    """
    try:
        # Read the file
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r') as f:
            data: Dict[str, Any] = json.load(f)

        # Validate required fields
        if 'countdown' not in data:
            raise ParseError("Missing required field: 'countdown'")
        if 'bounty_hunters' not in data:
            raise ParseError("Missing required field: 'bounty_hunters'")

        # Parse countdown
        countdown = data['countdown']
        if not isinstance(countdown, int):
            raise ParseError(f"'countdown' must be an integer, got {type(countdown).__name__}")

        # Parse bounty hunters
        hunters_data = data['bounty_hunters']
        if not isinstance(hunters_data, list):
            raise ParseError(f"'bounty_hunters' must be a list, got {type(hunters_data).__name__}")

        bounty_hunters = []
        for i, hunter_data in enumerate(hunters_data):
            try:
                hunter = BountyHunter(
                    planet=hunter_data.get('planet', ''),
                    day=hunter_data.get('day', -1)
                )
                bounty_hunters.append(hunter)
            except (KeyError, ValueError) as e:
                raise ParseError(f"Invalid bounty hunter at index {i}: {str(e)}")

        return EmpireData(countdown=countdown, bounty_hunters=bounty_hunters)

    except json.JSONDecodeError as e:
        raise ParseError(f"Invalid JSON in {file_path}: {str(e)}")
    except ValueError as e:
        raise ParseError(f"Validation error in {file_path}: {str(e)}")
