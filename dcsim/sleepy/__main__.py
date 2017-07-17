import matplotlib.pyplot as plt
from dcsim.framework import *
from dcsim.sleepy.HonestNode import HonestNode
from dcsim.sleepy.ConsistencyAttack import ConsistencyAttack
from dcsim.sleepy.Measurement import Measurement
from .Configuration import Configuration
from dcsim.utils import *
# from dcsim.authentication_service.hash import HashBasedAuthenticationService
# from dcsim.authentication_service.rsa import RsaBasedAuthenticationService
# from dcsim.authentication_service.none import NoAuthenticationService

def evaluate(config):
    results = []
    for idx in range(10):
        runner = Runner(config)
        runner.add_trusted_third_party(FSign('FSign'))
        runner.init()
        res = runner.run()
        results.append(res)
    probability_of_success = 1.0 * results.count(True) / len(results)
    print("Probability of Success: {}".format(probability_of_success))
    return probability_of_success

configs = []
corrupt_ratios = [0.5, 0.6, 0.7, 0.8, 0.9]
success_probabilities = []
total_nodes = 10
for prob in corrupt_ratios:
    num_corrupted_nodes = int(total_nodes * prob)
    num_honest_nodes = total_nodes - num_corrupted_nodes
    config = Configuration(honest_node_type=HonestNode,
                           adversary_controller_type=ConsistencyAttack,
                           measurement_type=Measurement,
                           num_honest_nodes=num_honest_nodes,
                           num_corrupted_nodes=num_corrupted_nodes,
                           max_delay=2,
                           confirm_time=6,
                           probability=0.1,
                           max_round=50)
    success_probabilities.append(evaluate(config))
plt.plot(corrupt_ratios, success_probabilities)
plt.show()

# config = Configuration(honest_node_type=HonestNode,
#                        adversary_controller_type=ConsistencyAttack,
#                        measurement_type=Measurement,
#                        num_honest_nodes=4,
#                        num_corrupted_nodes=6,
#                        max_delay=2,
#                        confirm_time=6,
#                        probability=0.1,
#                        max_round=50)
# runner = Runner(config)
# runner.add_trusted_third_party(FSign('FSign'))
# runner.init()
# runner.run()
