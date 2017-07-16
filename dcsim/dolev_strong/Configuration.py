from typing import *
from dcsim.framework import *
from .AdversaryController import AdversaryController
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement


class Configuration(ConfigurationBase):
    honest_node_type = HonestNode
    corrupted_node_type = CorruptedNode
    adversary_controller_type = AdversaryController
    measurement_type = Measurement
    num_nodes = 100
    ratio_corrupted = 0.98
    num_round0_sender = 1