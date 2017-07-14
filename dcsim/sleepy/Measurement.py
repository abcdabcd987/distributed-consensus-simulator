from typing import *
from dcsim.framework import *


class Measurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return self.stop or round >= self.max_round

    def __init__(self, corrupted_nodes: Iterable[Type[NodeBase]], honest_nodes: Iterable[Type[NodeBase]],
                 network: Type[NetworkControllerBase], adversary: Type[AdversaryControllerBase],
                 config: Type['ConfigurationBase']) -> None:
        super().__init__(corrupted_nodes, honest_nodes, network, adversary, config)
        self._log_for_honest = {}
        for node in self._honest_nodes:
            self._log_for_honest[node] = []
        self.stop = False
        self.max_round = 50

    def report_round(self, round: int) -> None:
        print("----------------------------------------------------------------")
        print("@ Round %d" % round)
        found = -1
        for node in self._honest_nodes:
            chain = node.main_chain
            for i in range(max(0, min(len(chain), len(self._log_for_honest[node])) - self._config.confirm_time)):
                print("Measurement.report_round: checking chain of NodeId %d index %d" % (node.id, i))
                if chain[i].hashval != self._log_for_honest[node][i].hashval:
                    found = node.id
                    break
            print("The chain of node %d is:" % node.id)
            for block in chain:
                print(block.hashval)
            self._log_for_honest[node] = chain
        if found != -1:
            print("Inconsistency detected on node %d!" % found)
            self.stop = True
        print("----------------------------------------------------------------")

    def report_final(self) -> None:
        print('''Trivial Consistency Attack:
Honest Nodes: {num_honest}
Corrupted Nodes: {num_corrupt}
Corrupted Ratio: {ratio}'''.format(
            num_honest=len(self._honest_nodes),
            num_corrupt=len(self._corrupted_nodes),
            ratio=len(self._corrupted_nodes) / (len(self._honest_nodes) + len(self._corrupted_nodes))))
        if not self.stop:
            print('Attack failed after {} rounds.'.format(self.max_round))
        else:
            print('Attack succeeded!')
