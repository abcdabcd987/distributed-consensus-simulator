import matplotlib.pyplot as plt
from dcsim.framework import *
from dcsim.sleepy.HonestNode import HonestNode
from dcsim.sleepy.ConsistencyAttack import ConsistencyAttack
from dcsim.sleepy.SelfishMining import SelfishMining
from dcsim.sleepy.ConsistencyMeasurement import ConsistencyMeasurement
from dcsim.sleepy.ChainQualityMeasurement import ChainQualityMeasurement
from .Configuration import Configuration
from dcsim.utils import *
import logging
logging.basicConfig(level=logging.DEBUG)
FSign = FSignHash
# FSign = FSignRSA


def evaluateConsistency(config, rounds):
    results = []
    for idx in range(rounds):
        runner = Runner(config)
        runner.add_trusted_third_party(FSign('FSign'))
        runner.init()
        res = runner.run()
        results.append(res)
    probability_of_success = results.count(True) / len(results)
    print("Probability of Success: {}".format(probability_of_success))
    return probability_of_success


def evaluateChainQuality(config, rounds):
    results = []
    for idx in range(rounds):
        runner = Runner(config)
        runner.add_trusted_third_party(FSign('FSign'))
        runner.init()
        res = runner.run()
        results.append(res)
    average_chain_quality = sum(results) / len(results)
    print("Average Chain Quality: {}".format(average_chain_quality))
    return average_chain_quality


def runConsistencyExperiment():
    #corrupt_ratios = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    corrupt_ratios = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.95, 1.0]
    success_probabilities = []
    total_nodes = 20
    for prob in corrupt_ratios:
        num_corrupted_nodes = int(total_nodes * prob)
        num_honest_nodes = total_nodes - num_corrupted_nodes
        config = Configuration(honest_node_type=HonestNode,
                               adversary_controller_type=ConsistencyAttack,
                               measurement_type=ConsistencyMeasurement,
                               num_honest_nodes=num_honest_nodes,
                               num_corrupted_nodes=num_corrupted_nodes,
                               max_delay=2,
                               confirm_time=6,
                               probability=0.05,
                               max_round=50)
        print("running: {}".format(prob))
        success_probabilities.append(evaluateConsistency(config, 100))
    with open('./consistency.csv','w') as f:
        f.write("Ratio of Corrupted Nodes, Probability of Sucess\n")
        for x,y in zip(corrupt_ratios, success_probabilities):
            f.write("{}, {}\n".format(x,y))
    '''
    plt.plot(corrupt_ratios, success_probabilities)
    plt.ylabel('Probability of Success')
    plt.xlabel('Ratio of Corrupted Nodes')
    plt.show()
    '''

def runSelfishMiningExperiment():
    #corrupt_ratios = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    #corrupt_ratios = [0.6, 0.65 ,0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    corrupt_ratios = [0.8]
    average_chain_quality = []
    total_nodes = 20
    for prob in corrupt_ratios:
        num_corrupted_nodes = int(total_nodes * prob)
        num_honest_nodes = total_nodes - num_corrupted_nodes
        config = Configuration(honest_node_type=HonestNode,
                               adversary_controller_type=SelfishMining,
                               measurement_type=ChainQualityMeasurement,
                               num_honest_nodes=num_honest_nodes,
                               num_corrupted_nodes=num_corrupted_nodes,
                               max_delay=2,
                               confirm_time=6,
                               probability=0.05,
                               max_round=50)
        print("running: {}".format(prob))
        average_chain_quality.append(evaluateChainQuality(config, 100))
    with open('./selfishMining.csv', 'w') as f:
        f.write("Ratio of Corrupted Nodes, Chain Quality\n")
        for x, y in zip(corrupt_ratios, average_chain_quality):
            f.write("{}, {}\n".format(x, y))
    '''  
    plt.plot(corrupt_ratios, average_chain_quality)
    plt.ylabel('Chain Quality')
    plt.xlabel('Ratio of Corrupted Nodes')
    plt.show()
    '''



#runConsistencyExperiment()
runSelfishMiningExperiment()
