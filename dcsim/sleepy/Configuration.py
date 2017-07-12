from typing import *
from dcsim.framework import *
from .AdversaryController import AdversaryController
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement
from .NetworkController import NetworkController


class Configuration(ConfigurationBase):
    honest_node_type = HonestNode
    corrupted_node_type = CorruptedNode
    network_controller_type = NetworkController
    adversary_controller_type = AdversaryController
    measurement_type = Measurement
    num_nodes = 10
    ratio_corrupted = 0.8
    max_delay = 5
    confirm_time = 2
