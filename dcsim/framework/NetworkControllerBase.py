import abc
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .MessageTuple import MessageTuple


class NetworkControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, config: Type['ConfigurationBase']):
        self._config = config

    @abc.abstractmethod
    def round_filter(self,
                     messages_to_send: List['MessageTuple'],
                     current_round: int) -> List[bool]:
        pass
