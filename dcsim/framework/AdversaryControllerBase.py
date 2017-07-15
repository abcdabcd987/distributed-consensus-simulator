import abc
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .MessageTuple import MessageTuple


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, corrupted_nodes: Tuple['NodeBase', ...], config: 'ConfigurationBase') -> None:
        self._corrupted_nodes = corrupted_nodes
        self._config = config

    @abc.abstractmethod
    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        pass

    @abc.abstractmethod
    def give_instruction(self, round: int) -> None:
        pass

    @abc.abstractmethod
    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        pass

    @abc.abstractmethod
    def add_corrupted_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        pass
