from dcsim.framework import *
from dcsim.sleepy import *
from dcsim.sleepy.HonestNode import HonestNode
from dcsim.sleepy.ConsistencyAttack import ConsistencyAttack
from dcsim.sleepy.CorruptedNode import  CorruptedNode
from dcsim.sleepy.Measurement import Measurement
from dcsim.sleepy.Experiment import Experiment
from .Configuration import Configuration
from dcsim.authentication_service.hash import HashBasedAuthenticationService
from dcsim.authentication_service.rsa import RsaBasedAuthenticationService
from dcsim.authentication_service.none import NoAuthenticationService


config = Configuration(honest_node_type= HonestNode,
                       corrupt_node_type=CorruptedNode,
                       adversary_controller_type=ConsistencyAttack,
                       measurement_type=Measurement,
                       num_nodes=10,
                       ratio_corrupted=0.6,
                       max_delay=2,
                       confirm_time=6,
                       probability=0.1,
                       max_round=50,
                       authentication_service_type=HashBasedAuthenticationService)
experiment = Experiment(config)
experiment.run()
