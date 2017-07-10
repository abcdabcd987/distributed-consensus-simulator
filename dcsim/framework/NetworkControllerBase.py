import abc
from typing import *
if TYPE_CHECKING:
    from .MessageTuple import MessageTuple


class NetworkControllerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def round_filter(self, messages_to_send: List['MessageTuple']) -> List[MessageTuple]:
        pass
