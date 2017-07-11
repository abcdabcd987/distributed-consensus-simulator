import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .NetworkControllerBase import NetworkControllerBase
    from .NodeBase import NodeBase


class MeasurementBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self,
                 corrupted_nodes: List[Type['NodeBase']],
                 honest_nodes: List[Type['NodeBase']],
                 network: Type['NetworkControllerBase'],
                 adv: Type['AdversaryControllerBase']) -> None:
        pass

    @abc.abstractmethod
    def should_stop(self, round) -> bool:
        pass

    @abc.abstractmethod
    def report(self) -> None:
        pass

    def report_every(self, honest_nodes, corrupted_nodes, round_counter):
        pass
