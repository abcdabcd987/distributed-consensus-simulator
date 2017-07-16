import abc
import sys
import random
from typing import *
from .NodeId import NodeId
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .Context import Context


class NodeBase(metaclass=abc.ABCMeta):
    def __init__(self, config: 'ConfigurationBase') -> None:
        self._config = config
        self._id = cast(NodeId, random.randint(1, sys.maxsize))

    def set_node_list(self, node_ids: Tuple['NodeId', ...]) -> None:
        self._nodes = node_ids

    @abc.abstractmethod
    def round_action(self, ctx: 'Context') -> None:
        pass

    @abc.abstractmethod
    def round0_sender_action(self, ctx: 'Context') -> None:
        pass

    @abc.abstractmethod
    def set_round0_senders(self, sender_id: Tuple['NodeId', ...]) -> None:
        pass

    @property
    def id(self) -> 'NodeId':
        return self._id
