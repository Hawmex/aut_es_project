from .types import State
from .statement import Statement


class Rule:
    def __init__(self, antecedent: Statement, consequent: Statement):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"IF({self.antecedent})\nTHEN({self.consequent})"

    def exec(self, state: State):
        antecedent_result = self.antecedent.exec(state)

        if antecedent_result:
            self.consequent.exec(state)

        return antecedent_result
