from __future__ import annotations
from typing import Dict, Set, Any, Optional


class Dependency:
    def __init__(self, values: Optional[Set[Any]] = None, priority: int = 0):
        self.values: Set[Any] = values if values is not None else set()
        self.priority = priority

    def __add__(self, other: Dependency):
        return Dependency(
            {*self.values, *other.values}, self.priority + other.priority
        )

    def __repr__(self):
        return f"Dependency(values={self.values}, priority={self.priority})"

    @staticmethod
    def sorted(dependencies: Dict[str, Dependency], reverse: bool = False):
        return dict(
            sorted(
                dependencies.items(),
                key=lambda item: item[1].priority,
                reverse=reverse,
            )
        )
