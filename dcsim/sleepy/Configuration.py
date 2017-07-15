from typing import *
from dcsim.framework import *
from .AdversaryController import AdversaryController
from .SelfishMining import SelfishMining
from .CorruptedNode import CorruptedNode
from .HonestNode import HonestNode
from .Measurement import Measurement


class Configuration(ConfigurationBase):
    honest_node_type = HonestNode
    corrupted_node_type = CorruptedNode

    # Consistency Attack
    # adversary_controller_type = AdversaryController

    # Selfish Mining Attack
    adversary_controller_type = SelfishMining

    measurement_type = Measurement
    num_nodes = 10
    ratio_corrupted = 0.3
    max_delay = 3
    confirm_time = 5
