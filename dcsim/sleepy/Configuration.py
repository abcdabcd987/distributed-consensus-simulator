from typing import *
from dcsim.framework import *
from .ConsistencyAttack import ConsistencyAttack
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement


class Configuration(RunnerBase):

    def __init__(self,
                 honest_node_type,
                 corrupt_node_type,
                 adversary_controller_type,
                 measurement_type,
                 num_nodes,
                 ratio_corrupted,
                 max_delay,
                 confirm_time,
                 probability,
                 max_round):
        self._honest_node_type = honest_node_type
        self._corrupted_node_type = corrupt_node_type
        self._adversary_controller_type = adversary_controller_type
        self._measurement_type = measurement_type
        self._num_nodes = num_nodes
        self._ratio_corrupted = ratio_corrupted
        self._max_delay = max_delay
        self._confirm_time = confirm_time
        self._probability = probability
        self._max_round = max_round

    @property
    def honest_node_type(self):
        return self._honest_node_type

    @property
    def corrupted_node_type(self):
        return self._corrupted_node_type

    @property
    def adversary_controller_type(self):
        return self._adversary_controller_type

    @property
    def measurement_type(self):
        return self._measurement_type

    @property
    def num_nodes(self):
        return self._num_nodes

    @property
    def ratio_corrupted(self):
        return self._ratio_corrupted

    @property
    def max_delay(self):
        return self._max_delay

    @property
    def confirm_time(self):
        return self._confirm_time

    @property
    def probability(self):
        return self._probability

    @property
    def max_round(self):
        return self._max_round

