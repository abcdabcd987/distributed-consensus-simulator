from dcsim.framework import *
from dcsim.sleepy import *
from dcsim.sleepy.HonestNode import HonestNode
from dcsim.sleepy.ConsistencyAttack import ConsistencyAttack
from dcsim.sleepy.Measurement import Measurement
from .Configuration import Configuration
from dcsim.utils import *


config = Configuration(honest_node_type= HonestNode,
                       adversary_controller_type=ConsistencyAttack,
                       measurement_type=Measurement,
                       num_honest_nodes=4,
                       num_corrupted_nodes=6,
                       max_delay=2,
                       confirm_time=6,
                       probability=0.1,
                       max_round=50)
experiment = ExperimentBase(config)
experiment.add_trusted_third_party(FSign('FSign'))
experiment.init()
experiment.run()
