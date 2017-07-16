from typing import *
from dcsim.framework import *
from .HonestNode import HonestNode
if TYPE_CHECKING:
   from .AdversaryController import AdversaryController
   from .Configuration import Configuration
   from .CorruptedNode import CorruptedNode


class Measurement(MeasurementBase):

    def should_stop(self, round: int) -> bool:
        self._f = int(self._config.num_nodes * self._config.ratio_corrupted) + 1
        return round >= self._f

    def report_round(self, round: int) -> None:
        pass

    def __init__(self,
                    corrupted_nodes: Tuple['CorruptedNode', ...],
                    honest_nodes: Tuple['HonestNode', ...],
                    adversary: 'AdversaryController',
                    config: 'Configuration') -> None:
        super().__init__(corrupted_nodes, honest_nodes, adversary, config)
        self._honest_nodes = honest_nodes
        self.stop = False
        self._f = 0

    def report_final(self) -> None:
        print('''Trivial Consistency Attack:
Honest Nodes: {num_honest}
Corrupted Nodes: {num_corrupt}
Corrupted Ratio: {ratio}
Max_round: {max_round}'''.format(
            num_honest=len(self._honest_nodes),
            num_corrupt=len(self._corrupted_nodes),
            ratio=len(self._corrupted_nodes) / (len(self._honest_nodes) + len(self._corrupted_nodes)),
            max_round = self._f))
        ans = []
        for h_node in self._honest_nodes:
            get_ans = h_node.get_ans()
            if get_ans not in ans:
                ans.append(get_ans)
        if (len(ans) < 2):
            print("Consensus established!", ans)
        else:
            print("Fail to establish the consensus...", len(ans))



