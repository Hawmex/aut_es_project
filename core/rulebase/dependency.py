from __future__ import annotations
from typing import Dict, Literal, Set, Optional, Union

DVal = Union[int, float, str]
DType = Literal["numerical", "categorical"]


class Dependency:
    def __init__(self, values: Optional[Set[DVal]] = None, priority: int = 0):
        self.values: Set[DVal] = set(values) if values is not None else set()
        self.priority = priority
        self.dtype: DType = self._dtype()

    def __add__(self, other: Dependency):
        if self.values and other.values and self.dtype != other.dtype:
            raise ValueError(
                "Cannot add two non-empty dependencies of different dtypes."
            )

        return Dependency(
            {*self.values, *other.values}, self.priority + other.priority
        )

    def __repr__(self):
        return f"Dependency(values={self.values}, priority={self.priority})"

    def _dtype(self) -> DType:
        if not self.values or all(
            isinstance(value, (int, float)) for value in self.values
        ):
            return "numerical"

        if all(isinstance(value, str) for value in self.values):
            return "categorical"

        raise ValueError("Dependency must be either numerical or categorical.")

    @staticmethod
    def sorted(dependencies: Dict[str, Dependency], reverse: bool = False):
        return dict(
            sorted(
                dependencies.items(),
                key=lambda item: item[1].priority,
                reverse=reverse,
            )
        )
