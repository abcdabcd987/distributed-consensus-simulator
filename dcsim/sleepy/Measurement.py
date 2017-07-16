from ctypes import cast
from typing import *
from typing import TYPE_CHECKING, Tuple

from dcsim.framework import *
from .HonestNode import HonestNode
if TYPE_CHECKING:
    from .ConsistencyAttack import ConsistencyAttack
    from .Configuration import Configuration
    from .CorruptedNode import CorruptedNode


class Measurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return self.stop or round >= self.max_round

    def __init__(self,
                 corrupted_nodes: Tuple['CorruptedNode', ...],
                 honest_nodes: Tuple['HonestNode', ...],
                 adversary: 'ConsistencyAttack',
                 config: 'Configuration') -> None:
        """
        Initialize the MeasurementBase, incluing set the corrupted nodes, honest nodes, adversary Controller, te Configuration
        :param corrupted_nodes: the corrupted nodes
        :param honest_nodes: the honest nodes
        :param adversary: the adversary controller is used
        :param config: the configuration is used
        """
        super().__init__(corrupted_nodes, honest_nodes, adversary, config)
        self._log_for_honest = {}  # type: Dict[NodeBase, Any]
        for node in self._honest_nodes:
            self._log_for_honest[node] = []
        self.stop = False
        self.max_round = config.max_round

    def report_round(self, round: int) -> None:
        """
        return the condition of each nodes ar this round
        :param round: the index of the round
        """
        print("----------------------------------------------------------------")
        print("@ Round %d" % round)
        found = -1
        for node in self._honest_nodes:
            chain = cast(HonestNode, node).main_chain
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
        """
        report the all the conditions and the result in the end
        """
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
