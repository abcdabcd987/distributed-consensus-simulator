import abc
import sys
import random
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .Context import Context
    from .NodeId import NodeId


class NodeBase(metaclass=abc.ABCMeta):
    def __init__(self, config: Type['ConfigurationBase']):
        self._config = config
        self._id = random.randint(1, sys.maxsize)

    @abc.abstractmethod
    def round_action(self, ctx: 'Context') -> None:
        pass

    @property
    def id(self) -> 'NodeId':
        return self._id
