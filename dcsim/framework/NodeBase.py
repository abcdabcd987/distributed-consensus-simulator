import abc
import sys
import random
from typing import *
from .NodeId import NodeId
if TYPE_CHECKING:
    from .RunnerBase import RunnerBase
    from .Context import Context


class NodeBase(metaclass=abc.ABCMeta):
    def __init__(self, config: 'RunnerBase') -> None:
        """
        intitialze the NodeBase, including the configuration and the nodeid
        :param config: the configuration of this node
        """
        self._config = config
        self._id = cast(NodeId, random.randint(1, sys.maxsize))

    def set_node_list(self, node_ids: Tuple['NodeId', ...]) -> None:
        """
        set the node list using a tuple contains all the nodes
        :param node_ids:
        """
        self._nodes = node_ids

    @abc.abstractmethod
    def round_action(self, ctx: 'Context') -> None:
        """
        the round action of the
        :param ctx:
        """
        pass

    @property
    def id(self) -> 'NodeId':
        return self._id
