import abc
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .MessageTuple import MessageTuple


class NetworkControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, config: 'ConfigurationBase') -> None:
        self._config = config

    @abc.abstractmethod
    def round_filter(self,
                     messages_to_send: Tuple['MessageTuple', ...],
                     current_round: int) -> List[bool]:
        pass
