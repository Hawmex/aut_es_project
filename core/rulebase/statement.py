from typing import Union

from .types import State, Dependencies


class Statement:
    def exec(self, state: State) -> Union[None, bool]:
        raise NotImplementedError()

    @property
    def dependencies(self) -> Dependencies:
        raise NotImplementedError()
