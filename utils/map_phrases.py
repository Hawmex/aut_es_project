import re

from typing import Callable


def map_phrases(expression: str, mapper: Callable[[str], str]):
    phrases = re.findall(r"[^(),|]+", expression)
    phrases = [p.strip() for p in phrases if p.strip()]

    result = expression

    for phrase in phrases:
        result = result.replace(phrase, mapper(phrase))

    return result
