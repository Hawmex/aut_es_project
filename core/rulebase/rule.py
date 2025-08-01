from __future__ import annotations
from typing import Iterable, Literal


from .state import State
from .statement import Statement


class Rule:
    def __init__(self, antecedent: Statement, consequent: Statement):
        if antecedent.stype != "evaluation":
            raise TypeError("Antecedent must be an evaluation statement")

        if consequent.stype != "assignment":
            raise TypeError("Consequent must be an assignment statement")

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
