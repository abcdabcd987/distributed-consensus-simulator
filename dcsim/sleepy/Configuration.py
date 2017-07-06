from typing import *
from dcsim.framework import *
from .AdversaryController import AdversaryController
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement
from .NetworkController import NetworkController


class Configuration(ConfigurationBase):
    @property
    def measurement_type(self) -> Type[MeasurementBase]:
        return Measurement

    @property
    def honest_node_type(self) -> Type[NodeBase]:
        return HonestNode

    @property
    def adversary_controller_type(self) -> Type[AdversaryControllerBase]:
        return AdversaryController

    @property
    def ratio_corrupted(self) -> float:
        return 0.4

    @property
    def max_delay(self) -> int:
        return 10

    @property
    def num_nodes(self) -> int:
        return 100

    @property
    def network_controller_type(self) -> Type[NetworkControllerBase]:
        return NetworkController

    @property
    def corrupted_node_type(self) -> Type[NodeBase]:
        return CorruptedNode
