from typing import *

import logging

from dcsim.framework import *
from .HonestNode import HonestNode
if TYPE_CHECKING:
    from .ConsistencyAttack import ConsistencyAttack
    from .Configuration import Configuration


class ConsistencyMeasurement(MeasurementBase):
    def should_stop(self, round) -> bool:
        return self.stop or round >= self.max_round

    def __init__(self, honest_nodes: List['NodeBase'], adversary: 'AdversaryControllerBase',
                 trusted_third_parties: 'TrustedThirdPartyBase', config: 'Configuration') -> None:
        """
        Initialize the MeasurementBase, incluing set the corrupted nodes, honest nodes, adversary Controller, te Configuration

        :param corrupted_nodes: the corrupted nodes
        :param honest_nodes: the honest nodes
        :param adversary: the adversary controller is used
        :param config: the configuration is used
        """
        super().__init__(honest_nodes, adversary, trusted_third_parties, config)
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
        logging.info("----------------------------------------------------------------")
        logging.info("@ Round %d" % round)
        found = -1
        for node in self._honest_nodes:
            chain = cast(HonestNode, node).main_chain
            for i in range(max(0, min(len(chain), len(self._log_for_honest[node])) - self._config.confirm_time)):
                logging.debug("Measurement.report_round: checking chain of NodeId %d index %d" % (node.id, i))
                if chain[i].hashval != self._log_for_honest[node][i].hashval:
                    found = node.id
                    break
            logging.debug("The chain of node %d is:" % node.id)
            for block in chain:
                logging.debug(block.hashval)
            self._log_for_honest[node] = chain
        if found != -1:
            logging.info("Inconsistency detected on node %d!" % found)
            self.stop = True

    def report_final(self):
        """
        report the all the conditions and the result in the end
        """
        logging.info('''Trivial Consistency Attack:
    Honest Nodes: {num_honest}
    Corrupted Nodes: {num_corrupt}
    Corrupted Ratio: {ratio}'''.format(
            num_honest=self._config.num_honest_nodes,
            num_corrupt=self._config.num_corrupted_nodes,
            ratio=self._config.num_corrupted_nodes / (
                self._config.num_corrupted_nodes + self._config.num_honest_nodes)))
        if not self.stop:
            logging.info('Attack failed after {} rounds.'.format(self.max_round))
            return False
        else:
            logging.info('Attack succeeded!')
            return True
