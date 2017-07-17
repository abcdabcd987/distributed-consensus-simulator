import abc
from typing import *

if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
    from .NodeBase import NodeBase


class ConfigurationBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def honest_node_type(self) -> Type['NodeBase']:
        """
            return the type of the hoest node
        """
        pass

    @property
    @abc.abstractmethod
    def adversary_controller_type(self) -> Type['AdversaryControllerBase']:
        """
            return the type of the adversary controller's type
        """
        pass

    @property
    @abc.abstractmethod
    def measurement_type(self) -> Type['MeasurementBase']:
        """
            return the type of the Measurement(Base)
        """
        pass

    @property
    @abc.abstractmethod
    def num_honest_nodes(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def num_corrupted_nodes(self) -> int:
        pass
