from typing import Set

from .rule import Rule
from .dependency import Dependencies


class Rulebase:
    def __init__(self, path: str, *rules: Rule):
        if not rules:
            raise ValueError("Expected at least one rule.")

        self.rules = rules
        self.io = self._io

        try:
            with open(path, "w") as file:
                file.write(str(self))
        except OSError as e:
            raise OSError(f"Failed to write to file: {path}") from e

    def __repr__(self):
        return "\n\n".join(
            f"# {i + 1}\n{rule}" for i, rule in enumerate(self.rules)
        )

    @property
    def _io(self):
        all_deps = Dependencies()
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
                    all_deps.add(key, value)

        return (
            Dependencies(
                {
                    key: all_deps[key]
                    for key in antecedent_dep_keys - consequent_dep_keys
                }
            ),
            Dependencies(
                {
                    key: all_deps[key]
                    for key in consequent_dep_keys - antecedent_dep_keys
                }
            ),
        )
