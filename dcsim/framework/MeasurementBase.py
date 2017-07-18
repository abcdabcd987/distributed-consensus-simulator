import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .TrustedThirdPartyBase import TrustedThirdPartyBase


class MeasurementBase(metaclass=abc.ABCMeta):
    def __init__(self,
                 honest_nodes: List['NodeBase'],
                 adversary: 'AdversaryControllerBase',
                 trusted_third_parties: 'TrustedThirdPartyBase',
                 config: 'ConfigurationBase') -> None:
        """
        Initialize the MeasurementBase, incluing set the corrupted nodes, honest nodes, adversary Controller, te Configuration
        :param honest_nodes: the honest nodes
        :param adversary: the adversary controller is used
        :param config: the configuration is used
        """
        self._honest_nodes = honest_nodes
        self._adversary = adversary
        self._trusted_third_parties = trusted_third_parties
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

    @abc.abstractmethod
    def report_selfish(self, round: int, adversary) -> None:
        pass
