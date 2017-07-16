import abc
from typing import *

from dcsim.framework.AuthenticationServiceBase import AuthenticationServiceBase

if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
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
    def authentication_service_type(self) -> Type['AuthenticationServiceBase']:
        pass
