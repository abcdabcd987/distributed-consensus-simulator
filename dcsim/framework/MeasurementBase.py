import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase


class MeasurementBase(metaclass=abc.ABCMeta):
    def __init__(self,
                 corrupted_nodes: Tuple['NodeBase', ...],
                 honest_nodes: Tuple['NodeBase', ...],
                 adversary: 'AdversaryControllerBase',
                 config: 'ConfigurationBase') -> None:
        self._corrupted_nodes = corrupted_nodes
        self._honest_nodes = honest_nodes
        self._adversary = adversary
        self._config = config

    @abc.abstractmethod
    def should_stop(self, round: int) -> bool:
        pass

    @abc.abstractmethod
    def report_final(self) -> None:
        pass

    @abc.abstractmethod
    def report_round(self, round: int) -> None:
        pass
