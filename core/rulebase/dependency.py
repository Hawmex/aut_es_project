from __future__ import annotations
from typing import Dict, Literal, Set, Optional, Union

DVal = Union[int, float, str]
DType = Literal["numerical", "categorical"]


class Dependency:
    def __init__(self, values: Optional[Set[DVal]] = None, priority: int = 0):
        if priority < 0:
            raise ValueError("Priority must be non-negative.")

        self.values: Set[DVal] = set(values) if values is not None else set()
        self.priority = priority
        self.dtype: DType = self._dtype

    def __add__(self, other: Dependency):
        if self.values and other.values and self.dtype != other.dtype:
            raise TypeError(
                "Cannot add two non-empty dependencies of different dtypes."
            )

        return Dependency(
            {*self.values, *other.values}, self.priority + other.priority
        )

    def __repr__(self):
        return f"Dependency(values={self.values}, priority={self.priority})"

    @property
    def _dtype(self) -> DType:
        if not self.values or all(
            isinstance(value, (int, float)) for value in self.values
        ):
            return "numerical"

        if all(isinstance(value, str) for value in self.values):
            return "categorical"

        raise TypeError("Dependency must be either numerical or categorical.")


class Dependencies:
    def __init__(self, collection: Optional[Dict[str, Dependency]] = None):
        self._collection: Dict[str, Dependency] = (
            dict(collection) if collection is not None else {}
        )

    def __getitem__(self, key: str):
        return self._collection[key]

    def __contains__(self, key: str):
        return key in self._collection

    def add(self, key: str, dependency: Dependency):
        try:
            if key not in self._collection:
                self._collection[key] = Dependency()

            self._collection[key] += dependency
        except TypeError as e:
            values = {*dependency.values, *self._collection[key].values}

            raise TypeError(
                f'Mismatch in types. Key: "{key}", values: {values}'
            ) from e

    def items(self):
        return self._collection.items()

    def keys(self):
        return self._collection.keys()

    def values(self):
        return self._collection.values()

    def sorted(self, reverse: bool = False):
        return Dependencies(
            dict(
                sorted(
                    self.items(),
                    key=lambda item: item[1].priority,
                    reverse=reverse,
                )
            )
        )
