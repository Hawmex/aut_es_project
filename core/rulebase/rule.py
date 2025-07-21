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
                and antecedent.stype == "Evaluation"
            )
        ):
            raise ValueError()

        if not (
            isinstance(consequent, Assignment)
            or (
                isinstance(consequent, LogicalOperator)
                and consequent.stype == "Assignment"
            )
        ):
            raise ValueError()

        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"IF {self.antecedent}\nTHEN {self.consequent}"

    def exec(self, state: State):
        antecedent_result = self.antecedent.exec(state)

        if antecedent_result:
            self.consequent.exec(state)

        return antecedent_result
