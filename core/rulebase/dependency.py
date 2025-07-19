from __future__ import annotations
from typing import Set, Any


class Dependency:
    def __init__(self, values: Set[Any] = set(), priority: int = 0):
        self.values = values
        self.priority = priority

    def __add__(self, other: Dependency):
        return Dependency(
            {*self.values, *other.values}, self.priority + other.priority
        )
