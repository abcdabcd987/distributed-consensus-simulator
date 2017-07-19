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
    corrupt_ratios = [0.02 * x for x in range(49)]
    success_probs = []
    total_nodes = 50
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
    
    with open('./dummyattack.csv', 'w') as f:
        f.write("Ratio of Corrupted Nodes, Ratio of Successful Attack\n")
        for x, y in zip(corrupt_ratios, success_probs):
            f.write("{}, {}\n".format(x, y))
    """
    plt.plot(corrupt_ratios, success_probs)
    plt.ylabel('Ratio of Successful Attack')
    plt.xlabel('Ratio of Corrupted Nodes')
    plt.show()
    """


runDummyAttackExperiment()