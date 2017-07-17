import abc
from typing import *
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
    from .NodeBase import NodeBase


class RunnerBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def honest_node_type(self) -> Type['NodeBase']:
        """
            return the type of the hoest node
        """
        pass

    @property
    @abc.abstractmethod
    def corrupted_node_type(self) -> Type['NodeBase']:
        """
            return the type of the corrupted nodes
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
    def num_nodes(self) -> int:
        """
            return the number of the nodes
        """
        pass

    @property
    @abc.abstractmethod
    def ratio_corrupted(self) -> float:
        """
        return the ratio of the corrupted nodes in all nodes
        """
        pass
