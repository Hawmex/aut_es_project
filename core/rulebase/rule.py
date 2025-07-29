from __future__ import annotations
from typing import Iterable, Literal

from .types import State
from .statement import Statement
from .expression import Evaluation, Assignment
from .logical_operator import LogicalOperator


class Rule:
    def __init__(self, antecedent: Statement, consequent: Statement):
        if not (
            isinstance(antecedent, Evaluation)
            or (
                isinstance(antecedent, LogicalOperator)
                and antecedent.stype == "evaluation"
            )
        ):
            raise ValueError("Antecedent must be an evaluation statement")

        if not (
            isinstance(consequent, Assignment)
            or (
                isinstance(consequent, LogicalOperator)
                and consequent.stype == "assignment"
            )
        ):
            raise ValueError("Consequent must be an assignment statement")

        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"IF {self.antecedent}\nTHEN {self.consequent}"

    def exec(self, state: State):
        antecedent_result = self.antecedent.exec(state)

        if antecedent_result:
            self.consequent.exec(state)

        return antecedent_result

    @staticmethod
    def sorted(
        rules: Iterable[Rule],
        by: Literal["antecedence", "consequence"],
        reverse: bool = False,
    ):
        def key(rule: Rule):
            deps = {
                "antecedence": rule.antecedent.dependencies,
                "consequence": rule.consequent.dependencies,
            }

            return sum(value.priority for value in deps[by].values())

        return sorted(rules, key=key, reverse=reverse)
