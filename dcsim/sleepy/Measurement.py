from typing import *
from dcsim.framework import *


class Measurement(MeasurementBase):
    def should_stop(self) -> bool:
        raise NotImplementedError

    def __init__(self, corrupted_nodes: List[Type[NodeBase]], honest_nodes: List[Type[NodeBase]],
                 network: Type[NetworkControllerBase], adv: Type[AdversaryControllerBase]) -> None:
        super().__init__(corrupted_nodes, honest_nodes, network, adv)
        self.corrupted_nodes = corrupted_nodes
        self.honest_nodes = honest_nodes
        self.num_corrupted_nodes = len(corrupted_nodes)
        self.num_honest_nodes = len(honest_nodes)
        self.num_nodes = self.num_corrupted_nodes + self.num_honest_nodes


    def report(self) -> None:
        s = "Trivial Consistency Attack: \n" \
            + "# Honest Nodes:\t" + self.num_honest_nodes + "\n" \
            + "# Corrupted Nodes:\t" + self.num_corrupted_nodes + "\n" \
            + "Corrupted Ratio:\t" + self.num_corrupted_nodes / self.num_nodes + "\n"
        repr(s)