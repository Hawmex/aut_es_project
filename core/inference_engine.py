from typing import Any, Set

from .rulebase import Rulebase, State, Rule


class InferenceEngine:
    def __init__(self, rulebase: Rulebase):
        self.rulebase = rulebase

    @staticmethod
    def ask(question: str, values: Set[Any]):
        options = sorted(list(values))

        print(f"\n{question}:")

        for i, option in enumerate(options):
            print(f"  {i+1}. {option}")

        while True:
            try:
                choice = input("Your choice (number): ")

                if choice == "":
                    return None

                choice_idx = int(choice) - 1

                if 0 <= choice_idx < len(options):
                    return options[choice_idx]

                print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def infer(self):
        if (
            not self.rulebase.rules
            or not self.rulebase.io[0]
            or not self.rulebase.io[1]
        ):
            raise ValueError(
                "Invalid rulebase: missing rules or I/O specifications"
            )

        print(
            "Please answer the following questions. Press Enter to skip a question."
        )

        working_memory: State = {}

        agenda: Set[Rule] = {
            rule
            for rule in self.rulebase.rules
            if rule.exec(working_memory) is None
        }

        max_iterations = len(self.rulebase.rules) * 2

        for _ in range(max_iterations):
            if not agenda:
                break

            selected_rule = max(
                agenda,
                key=lambda rule: sum(
                    value.priority
                    for key, value in self.rulebase.io[0].items()
                    if key in rule.antecedent.dependencies
                ),
            )

            missing_inputs = {
                key: value
                for key, value in self.rulebase.io[0].items()
                if key in selected_rule.antecedent.dependencies
                and key not in working_memory
            }

            for key, value in missing_inputs.items():
                working_memory[key] = InferenceEngine.ask(key, value.values)

            agenda = {
                rule for rule in agenda if rule.exec(working_memory) is None
            }
        else:
            print(
                "Maximum iterations reached. Possible cyclic dependencies or insufficient inputs."
            )

        output = {
            key: value
            for key, value in working_memory.items()
            if key in self.rulebase.io[1]
        }

        if len(output) == 0:
            print("\nInsufficient information to infer an output.")

            return None

        return output
