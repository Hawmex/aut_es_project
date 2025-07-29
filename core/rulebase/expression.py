from typing import Literal, Union

from .types import State, Dependency, DVal
from .statement import Statement


class Expression(Statement):
    def __init__(self, key: str, value: DVal):
        self.key = key
        self.value = value

        super().__init__()

    def _dependencies(self):
        return {self.key: Dependency({self.value}, 1)}


class Assignment(Expression):
    def exec(self, state: State):
        state[self.key] = self.value

    def __repr__(self):
        return f"{self.key} = '{self.value}'"

    def _stype(self):
        return "assignment"


class Evaluation(Expression):
    def __init__(
        self,
        key: str,
        op: Literal["==", ">=", "<=", ">", "<", "!="],
        value: DVal,
    ):
        super().__init__(key, value)

        self.op = op

    def exec(self, state: State) -> Union[None, bool]:
        if self.key not in state:
            return

        actual = state[self.key]

        match self.op:
            case "==":
                return actual == self.value
            case ">=":
                return actual >= self.value  # type: ignore
            case "<=":
                return actual <= self.value  # type: ignore
            case ">":
                return actual > self.value  # type: ignore
            case "<":
                return actual < self.value  # type: ignore
            case "!=":
                return actual != self.value
            case _:
                raise ValueError(f"Unknown operator: {self.op}")

    def __repr__(self):
        return f"{self.key} {self.op} '{self.value}'"

    def _stype(self):
        return "evaluation"
