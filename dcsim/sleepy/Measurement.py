from typing import *
from dcsim.framework import *


class Measurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return round > 50

    def __init__(self, corrupted_nodes: List[Type[NodeBase]], honest_nodes: List[Type[NodeBase]],
                 network: Type[NetworkControllerBase], adv: Type[AdversaryControllerBase],
                 confirm_time: int) -> None:
        super().__init__(corrupted_nodes, honest_nodes, network, adv)
        self.corrupted_nodes = corrupted_nodes
        self.honest_nodes = honest_nodes
        self.num_corrupted_nodes = len(corrupted_nodes)
        self.num_honest_nodes = len(honest_nodes)
        self.num_nodes = self.num_corrupted_nodes + self.num_honest_nodes
        self.log_for_honest = {}
        for node in self.honest_nodes:
            self.log_for_honest[node] = []
        self.confirm_time = confirm_time

    def report_every(self, honest_nodes, corrupt_nodes, round):
        print("----------------------------------------------------------------")
        print("@ Round %d" % round)
        found = -1
        for node in honest_nodes:
            chain = node.main_chain
            for i in range(max(0, min(len(chain), len(self.log_for_honest[node])) - self.confirm_time)):
                print("Measurement.report_every: checking chain of NodeId %d index %d" % (node.id, i))
                if chain[i].hashval != self.log_for_honest[node][i].hashval:
                    found = node.id
                    break
            print("The chain of node %d is:" % node.id)
            for block in chain:
                print(block.hashval)
            self.log_for_honest[node] = chain
        if found != -1:
            print("Inconsistency detected on node %d!" % found)
        print("----------------------------------------------------------------")


    def report(self) -> None:
        print('''Trivial Consistency Attack:
# Honest Nodes: {num_honest}
# Corrupted Nodes: {num_corrupt}
Corrupted Ratio: {ratio} '''.format(
            num_honest=self.num_honest_nodes,
            num_corrupt=self.num_corrupted_nodes,
            ratio=self.num_corrupted_nodes / self.num_nodes))
