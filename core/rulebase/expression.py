from abc import ABC
from typing import Literal, Union

from .dependency import DType, DVal, Dependencies, Dependency
from .state import State
from .statement import Statement


class Expression(Statement, ABC):
    def __init__(self, key: str, value: DVal):
        self.key = key
        self.value = value

        super().__init__()

        self.dtype: DType = self.dependencies[self.key].dtype

    @property
    def _dependencies(self):
        return Dependencies({self.key: Dependency({self.value}, 1)})

    @property
    def _val_str(self):
        return (
            f'"{self.value}"'
            if self.dtype == "categorical"
            else f"{self.value}"
        )


class Assignment(Expression):
    def __repr__(self):
        return f"{self.key} = {self._val_str}"

    @property
    def _stype(self):
        return "assignment"

    def exec(self, state: State):
        state[self.key] = self.value


class Evaluation(Expression):
    def __init__(
        self,
        key: str,
        op: Literal["==", "!=", ">=", "<=", ">", "<"],
        value: DVal,
    ):
        if op not in ["==", "!=", ">=", "<=", ">", "<"]:
            raise ValueError(f"Unknown operator: {op}")

        self.op = op

        super().__init__(key, value)

        if op in [">=", "<=", ">", "<"] and self.dtype != "numerical":
            raise TypeError(f"Operator {op} requires numerical value.")

    def __repr__(self):
        return f"{self.key} {self.op} {self._val_str}"

    @property
    def _stype(self):
        return "evaluation"

    def exec(self, state: State) -> Union[None, bool]:
        if self.key not in state:
            return

        actual = state[self.key]

        if not (
            (isinstance(actual, str) and self.dtype == "categorical")
            or (isinstance(actual, (int, float)) and self.dtype == "numerical")
        ):
            raise TypeError(
                f'Unexpected type in state for key "{self.key}". '
                f"Got value: {f'"{actual}"' if isinstance(actual, str) else actual}, "
                f'expected type: "{self.dtype}".'
            )

        match self.op:
            case "==":
                return actual == self.value
            case "!=":
                return actual != self.value
            case ">=":
                assert isinstance(self.value, (int, float))
                assert isinstance(actual, (int, float))

                return actual >= self.value
            case "<=":
                assert isinstance(self.value, (int, float))
                assert isinstance(actual, (int, float))

                return actual <= self.value
            case ">":
                assert isinstance(self.value, (int, float))
                assert isinstance(actual, (int, float))

                return actual > self.value
            case "<":
                assert isinstance(self.value, (int, float))
                assert isinstance(actual, (int, float))

                return actual < self.value
            case _:
                return False
