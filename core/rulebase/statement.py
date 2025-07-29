from typing import Literal, Union

from .types import State, Dependencies

SType = Literal["assignment", "evaluation"]


class Statement:
    def __init__(self) -> None:
        self.stype: SType = self._stype()
        self.dependencies: Dependencies = self._dependencies()

    def exec(self, state: State) -> Union[None, bool]:
        raise NotImplementedError()

    def _dependencies(self) -> Dependencies:
        raise NotImplementedError()

    def _stype(self) -> SType:
        raise NotImplementedError()
