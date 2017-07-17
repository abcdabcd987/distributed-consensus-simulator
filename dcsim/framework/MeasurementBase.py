import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .RunnerBase import RunnerBase
    from .NodeBase import NodeBase


class MeasurementBase(metaclass=abc.ABCMeta):
    def __init__(self,
                 corrupted_nodes: Tuple['NodeBase', ...],
                 honest_nodes: Tuple['NodeBase', ...],
                 adversary: 'AdversaryControllerBase',
                 config: 'RunnerBase') -> None:
        """
        Initialize the MeasurementBase, incluing set the corrupted nodes, honest nodes, adversary Controller, te Configuration
        :param corrupted_nodes: the corrupted nodes
        :param honest_nodes: the honest nodes
        :param adversary: the adversary controller is used
        :param config: the configuration is used
        """
        self._corrupted_nodes = corrupted_nodes
        self._honest_nodes = honest_nodes
        self._adversary = adversary
        self._config = config

    @abc.abstractmethod
    def should_stop(self, round: int) -> bool:
        """
        return whether the simulation should stop
        :param round: the round the simulation is at
        """
        pass

    @abc.abstractmethod
    def report_final(self) -> None:
        """
        report the all the conditions and the result in the end
        """
        pass

    @abc.abstractmethod
    def report_round(self, round: int) -> None:
        """
        return the condition of each nodes ar this round
        :param round: the index of the round
        """
        pass
