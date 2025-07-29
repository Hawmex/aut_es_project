import random

from collections import defaultdict

from .types import Dependencies, State
from .dependency import Dependency
from .statement import Statement


class LogicalOperator(Statement):
    def __init__(self, *statements: Statement):
        self.statements = statements

        super().__init__()

    def _stype(self):
        if all(stmt.stype == "assignment" for stmt in self.statements):
            return "assignment"

        if all(stmt.stype == "evaluation" for stmt in self.statements):
            return "evaluation"

        raise TypeError("Mixed statement types not allowed")

    def _dependencies(self):
        result: Dependencies = defaultdict(Dependency)

        for stmt in self.statements:
            for key, value in stmt.dependencies.items():
                result[key] += value

        return dict(result)


class LogicalAnd(LogicalOperator):
    def exec(self, state: State):
        results = [stmt.exec(state) for stmt in self.statements]

        if self.stype == "evaluation":
            if False in results:
                return False

            if None not in results:
                return True

    def __repr__(self):
        return f'({" AND ".join(map(str, self.statements))})'


class LogicalOr(LogicalOperator):
    def exec(self, state: State):
        if self.stype == "assignment":
            random.choice(self.statements).exec(state)

            return

        results = [stmt.exec(state) for stmt in self.statements]

        if True in results:
            return True

        if None not in results:
            return False

    def __repr__(self):
        return f'({" OR ".join(map(str, self.statements))})'
