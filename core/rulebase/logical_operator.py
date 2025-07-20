import random

from collections import defaultdict

from .expression import Assignment, Evaluation
from .types import Dependencies, State
from .dependency import Dependency
from .statement import Statement


class LogicalOperator(Statement):
    def __init__(self, *statements: Statement):
        self.statements = statements

    @property
    def stype(self):
        def is_assignment(item: Statement):
            return (
                item.stype == "Assignment"
                if isinstance(item, LogicalOperator)
                else isinstance(item, Assignment)
            )

        def is_evaluation(item: Statement):
            return (
                item.stype == "Evaluation"
                if isinstance(item, LogicalOperator)
                else isinstance(item, Evaluation)
            )

        if all(is_assignment(item) for item in self.statements):
            return "Assignment"
        elif all(is_evaluation(item) for item in self.statements):
            return "Evaluation"
        else:
            raise TypeError()

    @property
    def dependencies(self):
        result: Dependencies = defaultdict(Dependency)

        for statement in self.statements:
            for key, value in statement.dependencies.items():
                result[key] += value

        return result


class LogicalAnd(LogicalOperator):
    def exec(self, state: State):
        results = [statement.exec(state) for statement in self.statements]

        if self.stype == "Evaluation":
            if False in results:
                return False

            if None not in results:
                return True

    def __repr__(self):
        return f'({" AND ".join(map(str, self.statements))})'


class LogicalOr(LogicalOperator):
    def exec(self, state: State):
        if self.stype == "Assignment":
            random.choice(self.statements).exec(state)

            return

        results = [statement.exec(state) for statement in self.statements]

        if True in results:
            return True

        if None not in results:
            return False

    def __repr__(self):
        return f'({" OR ".join(map(str, self.statements))})'
