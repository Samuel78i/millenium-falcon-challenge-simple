"""
Millennium Falcon Mission Calculator

A solution to the Dataiku technical challenge: computing the odds of the
Millennium Falcon successfully reaching Endor before the Death Star strikes.

Main interface:
    >>> from src import C3PO
    >>> c3po = C3PO("millennium-falcon.json")
    >>> odds = c3po.giveMeTheOdds("empire.json")
"""

from .c3po import C3PO
from .models import (
    Route,
    BountyHunter,
    MillenniumFalconData,
    EmpireData,
    SearchState
)
from .parser import parse_millennium_falcon, parse_empire, ParseError
from .galaxy import Galaxy
from .pathfinder import PathFinder, calculate_success_probability

__all__ = [
    'C3PO',
    'Route',
    'BountyHunter',
    'MillenniumFalconData',
    'EmpireData',
    'SearchState',
    'parse_millennium_falcon',
    'parse_empire',
    'ParseError',
    'Galaxy',
    'PathFinder',
    'calculate_success_probability',
]

__version__ = '1.0.0'
