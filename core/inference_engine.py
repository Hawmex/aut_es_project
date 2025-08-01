import textwrap

from typing import Dict, List, Literal, Tuple

from .rulebase import Rulebase, State, Rule, DType, Dependencies, DVal
from .utils import print_headline, NaS


class InferenceEngine:
    def __init__(self, rulebase: Rulebase):
        self.rulebase = rulebase
        self.working_memory: State = {}
        self.reasoning_trace: List[Tuple[State, Rule]] = []

    @property
    def output(self):
        result = {
            key: value
            for key, value in self.working_memory.items()
            if key in self.rulebase.io[1]
        }

        return result

    def _ask(self, question: str):
        print(f"\n{question}:")

        prompts: Dict[DType, str] = {
            "numerical": "Your answer (number): ",
            "categorical": "Your choice (number): ",
        }

        default_values: Dict[DType, DVal] = {
            "numerical": float("nan"),
            "categorical": NaS(),
        }

        dep = self.rulebase.io[0][question]
        options = sorted(list(dep.values))

        if dep.dtype == "categorical":
            for i, option in enumerate(options):
                print(f'  {i+1}. "{option}"')

        while True:
            try:
                response = input(prompts[dep.dtype])

                if response.lower() == "why?":
                    self._explain_why(question)

                    break

                if response == "":
                    self.working_memory[question] = default_values[dep.dtype]

                    break

                if dep.dtype == "numerical":
                    self.working_memory[question] = float(response)

                    break

                if dep.dtype == "categorical":
                    choice_idx = int(response) - 1

                    if 0 <= choice_idx < len(options):
                        self.working_memory[question] = options[choice_idx]

                        break

                print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _exec(self, rule: Rule):
        state_snapshot = self.working_memory.copy()
        result = rule.exec(self.working_memory)

        if result:
            self.reasoning_trace.append((state_snapshot, rule))

        return result

    def _infer_forward(self):
        unused_rules = set(self.rulebase.rules)

        while unused_rules:
            for rule in Rule.sorted(
                unused_rules, by="antecedence", reverse=True
            ):
                if self._exec(rule) is not None:
                    unused_rules.remove(rule)

                    continue

                missing_inputs = Dependencies(
                    {
                        key: value
                        for key, value in self.rulebase.io[0].items()
                        if key not in self.working_memory
                        and key in rule.antecedent.dependencies
                    }
                ).sorted(reverse=True)

                for key in missing_inputs.keys():
                    self._ask(key)

                    if self._exec(rule) is not None:
                        unused_rules.remove(rule)

                        break

    def _infer_backward(self):
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

                for key in rule.antecedent.dependencies.sorted(
                    reverse=True
                ).keys():
                    if self._exec(rule) is not None:
                        break

                    solve(key)
                else:
                    self._exec(rule)

        for key in self.rulebase.io[1].sorted(reverse=True).keys():
            solve(key)

    def _explain_why(self, question: str):
        print(
            "\nAnswering this question will help with the "
            "execution of the following rules:"
        )

        for rule in self.rulebase.rules:
            if question in rule.antecedent.dependencies:
                print(f"\n{rule}")

        self._ask(question)

    def _explain_how(self):
        print_headline("How were the outputs derived?")

        for i, (state_snapshot, rule) in enumerate(self.reasoning_trace, 1):
            print(f"\nStep {i}:")
            print("  State:")

            for key, value in state_snapshot.items():
                print(
                    f"    {key}: {f'"{value}"' if isinstance(value, str) else value}"
                )

            print(f"  Rule:\n{textwrap.indent(str(rule), "    ")}")

    def infer(self, chaining: Literal["forward", "backward"]):
        print_headline(f"{chaining.upper()}-Chaining Inference", char="=")

        print_headline(
            "Please answer the following questions. "
            "Press Enter to skip a question. "
            "Press Ctrl+Z+Enter to exit the inference process. "
            'Answer "Why?" To see why a question is being asked.'
        )

        self.working_memory.clear()
        self.reasoning_trace.clear()

        try:
            match chaining:
                case "forward":
                    self._infer_forward()
                case "backward":
                    self._infer_backward()
                case _:
                    raise ValueError("Unknown inference chaining method.")
        except EOFError:
            print_headline("Inference process interrupted by user.")

        if len(self.output) == 0:
            print_headline("Insufficient information to infer an output.")

            return

        while True:
            should_explain = input(
                "\nDo you want to know how the conclusion was achieved? (yes/no) "
            ).lower()

            if should_explain == "no":
                break

            if should_explain == "yes":
                self._explain_how()

                break

            print('Please answer with "yes" or "no".')
