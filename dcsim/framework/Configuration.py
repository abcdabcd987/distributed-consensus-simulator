from .ConfigurationBase import ConfigurationBase
from typing import *
if TYPE_CHECKING:
    from .AdversaryControllerBase import AdversaryControllerBase
    from .MeasurementBase import MeasurementBase
    from .NetworkControllerBase import NetworkControllerBase
    from .NodeBase import NodeBase


class Configuration(ConfigurationBase):

    def __init__(self, num_nodes: int, num_corrupted_nodes: int,
                 honest_node_type: Type['NodeBase'],
                 corrupted_node_type: Type['NodeBase'],
                 network_controller_type: Type['NetworkControllerBase'],
                 max_delay: int,
                 adversary_controller_type: Type['AdversaryControllerBase'],
                 measurement_type: Type['MeasurementBase']):
        self.m_num_nodes = num_nodes
        self.m_num_corrupted_nodes = num_corrupted_nodes
        self.m_honest_node_type = honest_node_type
        self.m_corrupted_node_type = corrupted_node_type
        self.m_network_controller_type = network_controller_type
        self.m_max_delay = max_delay
        self.m_adversary_controller_type = adversary_controller_type
        self.m_measurement_type = measurement_type
        
    # @property
    def get_num_nodes(self) -> int:
        return self.m_num_nodes
    
    def get_num_honest_nodes(self) -> int:
        return self.m_num_nodes - self.m_num_corrupted_nodes

    def get_num_corrupted_nodes(self) -> int:
        return self.m_num_corrupted_nodes

    # @property
    def get_measurement_type(self) -> Type['MeasurementBase']:
        return self.m_measurement_type

    # @property
    def get_max_delay(self) -> int:
        return self.m_max_delay

    # @property
    def get_corrupted_node_type(self) -> Type['NodeBase']:
        return self.m_corrupted_node_type

    # @property
    def get_ratio_corrupted(self) -> float:
        return self.m_num_corrupted_nodes / self.m_num_nodes

    # @property
    def get_network_controller_type(self) -> Type['NetworkControllerBase']:
        return self.m_network_controller_type

    # @property
    def get_honest_node_type(self) -> Type['NodeBase']:
        return self.m_honest_node_type

    # @property
    def get_adversary_controller_type(self) -> Type['AdversaryControllerBase']:
        return self.m_adversary_controller_type