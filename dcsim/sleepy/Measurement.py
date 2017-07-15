from typing import *
from dcsim.framework import *
from .HonestNode import HonestNode
if TYPE_CHECKING:
    from .AdversaryController import AdversaryController
    from .Configuration import Configuration
    from .CorruptedNode import CorruptedNode


class Measurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return self.stop or round >= self.max_round

    def __init__(self,
                 corrupted_nodes: Tuple['CorruptedNode', ...],
                 honest_nodes: Tuple['HonestNode', ...],
                 adversary: 'AdversaryController',
                 config: 'Configuration') -> None:
        super().__init__(corrupted_nodes, honest_nodes, adversary, config)
        self._log_for_honest = {}  # type: Dict[NodeBase, Any]
        for node in self._honest_nodes:
            self._log_for_honest[node] = []
        self.stop = False
        self.max_round = 50

    def report_round(self, round: int) -> None:
        print("----------------------------------------------------------------")
        print("@ Round %d Start" % round)
        print("Detecting Consistency...")
        found = -1
        for node in self._honest_nodes:
            chain = cast(HonestNode, node).main_chain
            for i in range(max(0, min(len(chain), len(self._log_for_honest[node])) - self._config.confirm_time)):
                # print("Measurement.report_round: checking chain of NodeId %d index %d" % (node.id, i))
                if chain[i].hashval != self._log_for_honest[node][i].hashval:
                    found = node.id
                    break
            # print("The chain of node %d is:" % node.id)
            # for block in chain:
            #     print(block.hashval)
            self._log_for_honest[node] = chain
        if found != -1:
            print("Inconsistency detected on node %d!" % found)
            self.stop = True
        print("----------------------------------------------------------------")

    def report_selfish(self, round: int) -> None:
        print("Calculating Chain Quality...")
        # print("@ Round %d" % round)

        print("- - - - -")
        corrupted_set = set([c.id for c in self._corrupted_nodes])

        for node in self._honest_nodes:
            chain_quality = []
            chain_T = []
            cnt = 0
            chain = cast(HonestNode, node).main_chain
            max_len = max(0, len(chain) - self._config.confirm_time)
            for i in range(1, len(chain)):
                if (i <= max_len):
                    if chain[i].pid in corrupted_set:
                        cnt += 1
                        chain_quality.append("corrupted")
                    else:
                        chain_quality.append("honest")
                else:
                    if chain[i].pid in corrupted_set:
                        chain_T.append("corrupted")
                    else:
                        chain_T.append("honest")

            cnt = min(cnt, max_len)
            if max_len <= 1:
                print("Chain Quality: 1.000000")
            else:
                print("Chain Quality: %f" % (1 - cnt / (max_len - 1)))
            print(list(chain_quality), list(chain_T))

        print("- - - - -")

        # chain = self._adversary.main_chain
        # cnt = 0
        # chain_quality = []
        # corrupted_set = set([c.id for c in self._corrupted_nodes])
        # max_len = max(0, len(chain))  # - self._config.confirm_time)
        # for i in range(1, max_len):
        #     if chain[i].pid in corrupted_set:
        #         cnt += 1
        #         chain_quality.append("corrupted")
        #     else:
        #         chain_quality.append("honest")
        # cnt = min(cnt, max_len)
        # if max_len <= 1:
        #     print("Chain Quality: 1.000000")
        # else:
        #     print("Chain Quality: %f" % (1 - cnt / (max_len - 1)))
        # print(list(chain_quality))
        print("@ Round %d end" % round)
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
