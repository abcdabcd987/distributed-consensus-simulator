import abc
from typing import *
if TYPE_CHECKING:
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .MessageTuple import MessageTuple


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def round_instruction(self,
                          corrupted_nodes: Type['NodeBase'],
                          pending_messages: List['MessageTuple'],
                          current_round: int) -> Dict['NodeId', Any]:
        pass
