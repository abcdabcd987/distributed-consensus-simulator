import abc
import sys
import random
from typing import *
from .NodeId import NodeId
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .Context import Context
    from .TrustedThirdPartyCaller import TrustedThirdPartyCaller


class NodeBase(metaclass=abc.ABCMeta):
    def __init__(self, config: 'ConfigurationBase') -> None:
        """
        intitialze a Node, including the configuration

        :param config: the configuration of this node
        """
        self._config = config
        self._id = NodeBase.generate_node_id()

    def set_trusted_third_party(self, trusted_third_party: 'TrustedThirdPartyCaller'):
        self._trusted_third_party = trusted_third_party

    @staticmethod
    def generate_node_id() -> 'NodeId':
        return cast(NodeId, random.randint(1, sys.maxsize))

    def set_node_list(self, node_ids: Tuple['NodeId', ...]) -> None:
        """
        set the node list using a tuple contains all the nodes

        :param node_ids:
        """
        self._nodes = node_ids

    @abc.abstractmethod
    def round_action(self, ctx: 'Context') -> None:
        """
        the action of a node in each round

        """
        pass

    @property
    def id(self) -> 'NodeId':
        """
        :return: node_id
        """
        return self._id
