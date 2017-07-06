import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
    from .NetworkControllerBase import NetworkControllerBase
    from .NodeBase import NodeBase


class ConfigurationBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def honest_node_type(self) -> Type['NodeBase']:
        pass

    @property
    @abc.abstractmethod
    def corrupted_node_type(self) -> Type['NodeBase']:
        pass

    @property
    @abc.abstractmethod
    def network_controller_type(self) -> Type['NetworkControllerBase']:
        pass

    @property
    @abc.abstractmethod
    def adversary_controller_type(self) -> Type['AdversaryControllerBase']:
        pass

    @property
    @abc.abstractmethod
    def measurement_type(self) -> Type['MeasurementBase']:
        pass

    @property
    @abc.abstractmethod
    def num_nodes(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def ratio_corrupted(self) -> float:
        pass

    @property
    @abc.abstractmethod
    def max_delay(self) -> int:
        pass