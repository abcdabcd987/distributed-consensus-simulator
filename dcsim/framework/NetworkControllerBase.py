import abc
from typing import *
if TYPE_CHECKING:
    from .NodeBase import NodeBase
    from .MessageTuple import MessageTuple


class NetworkControllerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def round_filter(self,
                     messages_to_send: List['MessageTuple'],
                     max_delay: int,
                     current_round: int,
                     corrupted_nodes: List['NodeBase']) -> List[bool]:
        pass
