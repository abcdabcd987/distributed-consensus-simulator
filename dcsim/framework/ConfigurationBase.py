import abc
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
    from .NetworkControllerBase import NetworkControllerBase
    from .NodeBase import NodeBase


class ConfigurationBase(metaclass=abc.ABCMeta):
    # @property
    @abc.abstractmethod
    def get_honest_node_type(self) -> Type['NodeBase']:
        pass

    # @property
    @abc.abstractmethod
    def get_corrupted_node_type(self) -> Type['NodeBase']:
        pass

    # @property
    @abc.abstractmethod
    def get_network_controller_type(self) -> Type['NetworkControllerBase']:
        pass

    # @property
    @abc.abstractmethod
    def get_adversary_controller_type(self) -> Type['AdversaryControllerBase']:
        pass

    # @property
    @abc.abstractmethod
    def get_measurement_type(self) -> Type['MeasurementBase']:
        pass

    # @property
    @abc.abstractmethod
    def get_num_nodes(self) -> int:
        pass

    @abc.abstractmethod
    def get_num_honest_nodes(self) -> int:
        pass

    @abc.abstractmethod
    def get_num_corrupted_nodes(self) -> int:
        pass

    # @property
    @abc.abstractmethod
    def get_ratio_corrupted(self) -> float:
        pass

    # @property
    @abc.abstractmethod
    def get_max_delay(self) -> int:
        pass