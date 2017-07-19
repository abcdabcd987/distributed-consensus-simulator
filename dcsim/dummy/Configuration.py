from typing import *
from dcsim.framework import *

class Configuration(ConfigurationBase):

    def __init__(self,
                 honest_node_type,
                 adversary_controller_type,
                 measurement_type,
                 num_honest_nodes,
                 num_corrupted_nodes):
        self._honest_node_type = honest_node_type
        self._adversary_controller_type = adversary_controller_type
        self._measurement_type = measurement_type
        self._num_honest_nodes = num_honest_nodes
        self._num_corrupted_nodes = num_corrupted_nodes

    @property
    def honest_node_type(self):
        return self._honest_node_type

    @property
    def adversary_controller_type(self):
        return self._adversary_controller_type

    @property
    def measurement_type(self):
        return self._measurement_type

    @property
    def num_honest_nodes(self):
        return self._num_honest_nodes

    @property
    def num_corrupted_nodes(self):
        return self._num_corrupted_nodes
