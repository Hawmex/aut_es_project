from typing import Any, Literal

from .types import State, Dependency
from .statement import Statement


class Expression(Statement):
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    @property
    def dependencies(self):
        return {self.key: Dependency({self.value}, 1)}


class Assignment(Expression):
    def exec(self, state: State):
        state[self.key] = self.value

    def __repr__(self):
        return f"{self.key} = '{self.value}'"


class Evaluation(Expression):
    def __init__(
        self,
        key: str,
        op: Literal["==", ">=", "<=", ">", "<", "!="],
        value: Any,
    ):
        super().__init__(key, value)

        self.op = op

    def exec(self, state: State):
        if self.key not in state:
            return

        actual = state[self.key]

        match self.op:
            case "==":
                return actual == self.value
            case ">=":
                return actual >= self.value
            case "<=":
                return actual <= self.value
            case ">":
                return actual > self.value
            case "<":
                return actual < self.value
            case "!=":
                return actual != self.value
            case _:
                raise ValueError()

    def __repr__(self):
        return f"{self.key} {self.op} '{self.value}'"
