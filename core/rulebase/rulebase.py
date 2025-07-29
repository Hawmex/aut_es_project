from collections import defaultdict
from typing import Set

from .rule import Rule
from .types import State, Dependencies
from .dependency import Dependency


class Rulebase:
    def __init__(self, path: str, *rules: Rule):
        self.rules = rules
        self.state: State = {}
        self.io = self._io()

        try:
            with open(path, "w") as file:
                file.write(str(self))
        except IOError as e:
            raise IOError(f"Failed to write to file {path}: {e}")

    def __repr__(self):
        return "\n\n".join(
            map(
                lambda rule: f"# {rule[0] + 1}\n{rule[1]}",
                enumerate(self.rules),
            )
        )

    def _io(self):
        all_deps: Dependencies = defaultdict(Dependency)
        antecedent_dep_keys: Set[str] = set()
        consequent_dep_keys: Set[str] = set()

        for rule in self.rules:
            antecedent_dep_keys.update(rule.antecedent.dependencies.keys())
            consequent_dep_keys.update(rule.consequent.dependencies.keys())

            for dependencies in [
                rule.antecedent.dependencies,
                rule.consequent.dependencies,
            ]:

                for key, value in dependencies.items():
                    all_deps[key] += value

        return (
            {
                key: all_deps[key]
                for key in antecedent_dep_keys - consequent_dep_keys
            },
            {
                key: all_deps[key]
                for key in consequent_dep_keys - antecedent_dep_keys
            },
        )
