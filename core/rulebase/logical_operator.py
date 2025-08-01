import random
import textwrap

from abc import ABC, abstractmethod

from .state import State
from .dependency import Dependencies
from .statement import Statement


class LogicalOperator(Statement, ABC):
    def __init__(self, *statements: Statement):
        self.statements = statements

        super().__init__()

        if not statements:
            raise ValueError("Expected at least one statement.")

    def __repr__(self):
        return (
            "(\n"
            + textwrap.indent(
                f"\n{self._name} ".join(map(str, self.statements)),
                "  ",
            )
            + "\n)"
        )

    @property
    def _stype(self):
        if all(stmt.stype == "assignment" for stmt in self.statements):
            return "assignment"

        if all(stmt.stype == "evaluation" for stmt in self.statements):
            return "evaluation"

        raise TypeError(
            "All statements in LogicalOperator must have the same stype "
            f"(got: {[stmt.stype for stmt in self.statements]})."
        )

    @property
    def _dependencies(self):
        result = Dependencies()

        for stmt in self.statements:
            for key, value in stmt.dependencies.items():
                result.add(key, value)

        return result

    @property
    @abstractmethod
    def _name(self) -> str:
        pass


class LogicalAnd(LogicalOperator):
    @property
    def _name(self):
        return "AND"

    def exec(self, state: State):
        results = [stmt.exec(state) for stmt in self.statements]

        if self.stype == "evaluation":
            if False in results:
                return False

            if None not in results:
                return True


class LogicalOr(LogicalOperator):
    @property
    def _name(self):
        return "OR"

    def exec(self, state: State):
        if self.stype == "assignment":
            random.choice(self.statements).exec(state)

            return

        results = [stmt.exec(state) for stmt in self.statements]

        if True in results:
            return True

        if None not in results:
            return False
