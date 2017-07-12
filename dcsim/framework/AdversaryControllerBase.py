import abc
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .MessageTuple import MessageTuple


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, corrupted_nodes: List['NodeBase'], config: Type['ConfigurationBase']):
        self._corrupted_nodes = corrupted_nodes
        self._config = config

    @abc.abstractmethod
    def round_instruction(self,
                          honest_messages_to_send: Dict['NodeId', List['MessageTuple']],
                          corrupted_messages_to_send: Dict['NodeId', List['MessageTuple']],
                          current_round: int):
        pass
