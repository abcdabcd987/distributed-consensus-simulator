import abc
from typing import *
if TYPE_CHECKING:
    from .Context import Context
    from .NodeId import NodeId


class NodeBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def round_action(self, ctx: 'Context') -> None:
        pass

    @property
    @abc.abstractmethod
    def id(self) -> 'NodeId':
        pass
