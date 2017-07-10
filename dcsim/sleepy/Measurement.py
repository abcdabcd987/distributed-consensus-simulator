from typing import *
from dcsim.framework import *


class Measurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return round > 100

    def __init__(self, corrupted_nodes: List[Type[NodeBase]], honest_nodes: List[Type[NodeBase]],
                 network: Type[NetworkControllerBase], adv: Type[AdversaryControllerBase]) -> None:
        super().__init__(corrupted_nodes, honest_nodes, network, adv)
        self.corrupted_nodes = corrupted_nodes
        self.honest_nodes = honest_nodes
        self.num_corrupted_nodes = len(corrupted_nodes)
        self.num_honest_nodes = len(honest_nodes)
        self.num_nodes = self.num_corrupted_nodes + self.num_honest_nodes

    def report(self) -> None:
        print('''Trivial Consistency Attack:
# Honest Nodes: {num_honest}
# Corrupted Nodes: {num_corrupt}
Corrupted Ratio: {ratio} '''.format(
            num_honest=self.num_honest_nodes,
            num_corrupt=self.num_corrupted_nodes,
            ratio=self.num_corrupted_nodes / self.num_nodes))
