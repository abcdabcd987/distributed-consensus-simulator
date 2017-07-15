import abc
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .Context import Context
    from .MessageTuple import MessageTuple


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, corrupted_nodes: Tuple['NodeBase', ...], config: 'ConfigurationBase') -> None:
        self._corrupted_nodes = corrupted_nodes
        self._config = config

    @abc.abstractmethod
    def round_instruction(self,
                          ctx: 'Context',
                          new_messages: Tuple['MessageTuple', ...],
                          old_messages: Tuple['MessageTuple', ...],
                          current_round: int):
        pass
