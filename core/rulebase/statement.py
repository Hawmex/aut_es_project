from abc import ABC, abstractmethod
from typing import Literal, Union

from .state import State
from .dependency import Dependencies

SType = Literal["assignment", "evaluation"]


class Statement(ABC):
    def __init__(self) -> None:
        self.stype: SType = self._stype
        self.dependencies: Dependencies = self._dependencies

    @property
    @abstractmethod
    def _dependencies(self) -> Dependencies:
        pass

    @property
    @abstractmethod
    def _stype(self) -> SType:
        pass

    @abstractmethod
    def exec(self, state: State) -> Union[None, bool]:
        pass
