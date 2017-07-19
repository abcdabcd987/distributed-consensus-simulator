import matplotlib.pyplot as plt
from .Configuration import Configuration
from .HonestNode import HonestNode
from .DummyAttack import DummyAttack
from .Measurement import Measurement
from dcsim.framework.Runner import Runner

def evalSuccess(config):
    results = []
    for idx in range(100):
        runner = Runner(config)
        runner.init()
        res = runner.run()
        results.append(res)

    prob_of_success = results.count(True) / len(results)
    print("Probability of Success: {}".format(prob_of_success))
    return prob_of_success

def runDummyAttackExperiment():
    corrupt_ratios = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    success_probs = []
    total_nodes = 20
    for prob in corrupt_ratios:
        num_corrupted_nodes = int(total_nodes * prob)
        num_honest_nodes = total_nodes - num_corrupted_nodes
        config = Configuration(honest_node_type=HonestNode,
                               adversary_controller_type=DummyAttack,
                               measurement_type=Measurement,
                               num_honest_nodes=num_honest_nodes,
                               num_corrupted_nodes=num_corrupted_nodes)

        print("running: {}".format(prob))
        success_probs.append(evalSuccess(config))

    plt.plot(corrupt_ratios, success_probs)
    plt.ylabel('Probability of Success')
    plt.xlabel('Ratio of Corrupted Nodes')
    plt.show()


runDummyAttackExperiment()