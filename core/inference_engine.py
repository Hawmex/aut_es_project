from typing import Literal

from .rulebase import Rulebase, State, Rule, Dependency
from .utils import print_headline


class InferenceEngine:
    def __init__(self, rulebase: Rulebase):
        self.rulebase = rulebase
        self.working_memory: State = {}

    def _start_inference(self):
        self.working_memory.clear()

        print_headline(
            "Please answer the following questions. "
            "Press Enter to skip a question."
        )

    def _ask(self, question: str):
        options = sorted(list(self.rulebase.io[0][question].values))

        print(f"\n{question}:")

        for i, option in enumerate(options):
            print(f"  {i+1}. {option}")

        while True:
            try:
                choice = input("Your choice (number): ")

                if choice == "":
                    self.working_memory[question] = None

                    break

                choice_idx = int(choice) - 1

                if 0 <= choice_idx < len(options):
                    self.working_memory[question] = options[choice_idx]

                    break

                print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _get_output(self):
        output = {
            key: value
            for key, value in self.working_memory.items()
            if key in self.rulebase.io[1]
        }

        if len(output) == 0:
            print("\nInsufficient information to infer an output.")

            return None

        return output

    def _infer_forward(self):
        self._start_inference()

        unused_rules = set(self.rulebase.rules)

        while unused_rules:
            for rule in Rule.sorted(
                unused_rules, by="antecedence", reverse=True
            ):
                if rule.exec(self.working_memory) is not None:
                    unused_rules.remove(rule)

                    continue

                missing_inputs = Dependency.sorted(
                    {
                        key: value
                        for key, value in self.rulebase.io[0].items()
                        if key not in self.working_memory
                        and key in rule.antecedent.dependencies
                    },
                    reverse=True,
                )

                for key in missing_inputs:
                    self._ask(key)

                    if rule.exec(self.working_memory) is not None:
                        unused_rules.remove(rule)

                        break

        return self._get_output()

    def _infer_backward(self):
        self._start_inference()

        unused_rules = set(self.rulebase.rules)

        def solve(key: str):
            if key in self.rulebase.io[0] and key not in self.working_memory:
                self._ask(key)

            agenda = Rule.sorted(
                {
                    rule
                    for rule in unused_rules
                    if key in rule.consequent.dependencies
                },
                by="consequence",
                reverse=True,
            )

            for rule in agenda:
                unused_rules.remove(rule)

                for key in Dependency.sorted(
                    rule.antecedent.dependencies, reverse=True
                ):
                    if rule.exec(self.working_memory) is not None:
                        break

                    solve(key)
                else:
                    rule.exec(self.working_memory)

        for key in Dependency.sorted(self.rulebase.io[1], reverse=True):
            solve(key)

        return self._get_output()

    def infer(self, chaining: Literal["forward", "backward"]):
        print_headline(f"{chaining.upper()}-Chaining Inference", char="%")

        match chaining:
            case "forward":
                return self._infer_forward()
            case "backward":
                return self._infer_backward()
            case _:
                raise ValueError("Unknown inference chaining method.")
