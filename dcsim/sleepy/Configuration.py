from typing import *
from dcsim.framework import *
from .AdversaryController import AdversaryController
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement
from .NetworkController import NetworkController


class Configuration(ConfigurationBase):
    @property
    def get_measurement_type(self) -> Type[MeasurementBase]:
        return Measurement

    @property
    def get_honest_node_type(self) -> Type[NodeBase]:
        return HonestNode

    @property
    def get_adversary_controller_type(self) -> Type[AdversaryControllerBase]:
        return AdversaryController

    @property
    def get_ratio_corrupted(self) -> float:
        return 0.4

    @property
    def get_max_delay(self) -> int:
        return 10

    @property
    def get_num_nodes(self) -> int:
        return 100

    @property
    def get_network_controller_type(self) -> Type[NetworkControllerBase]:
        return NetworkController

    @property
    def get_corrupted_node_type(self) -> Type[NodeBase]:
        return CorruptedNode
