from dcsim.framework import *
from dcsim.sleepy import *
from dcsim.sleepy.HonestNode import HonestNode
from dcsim.sleepy.ConsistencyAttack import ConsistencyAttack
from dcsim.sleepy.CorruptedNode import  CorruptedNode
from dcsim.sleepy.Measurement import Measurement
from dcsim.sleepy.Runner import Runner
from .Configuration import Configuration
from dcsim.authentication_service.hash import HashBasedAuthenticationService
from dcsim.authentication_service.rsa import RsaBasedAuthenticationService
from dcsim.authentication_service.none import NoAuthenticationService
import matplotlib.pyplot as plt
def evaluate(config):
    results = []
    for idx in range(10):
        experiment = Runner(config)
        results.append(experiment.run())
    probability_of_success = 1.0 * results.count(True) / len(results)
    print("Probability of Success: {}".format(probability_of_success))
    return probability_of_success
configs = []
corrupt_ratios = [0.5, 0.6, 0.7, 0.8, 0.9]
success_probabilities = []
for prob in corrupt_ratios:
    config = Configuration(honest_node_type= HonestNode,
                           corrupt_node_type=CorruptedNode,
                           adversary_controller_type=ConsistencyAttack,
                           measurement_type=Measurement,
                           num_nodes=10,
                           ratio_corrupted=prob,
                           max_delay=2,
                           confirm_time=6,
                           probability=0.1,
                           max_round=50,
                           authentication_service_type=HashBasedAuthenticationService)
    success_probabilities.append(evaluate(config))
plt.plot(corrupt_ratios, success_probabilities)
plt.show()
