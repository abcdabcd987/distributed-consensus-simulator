from typing import *

import logging

from dcsim.framework import *
from .HonestNode import HonestNode
if TYPE_CHECKING:
    from .ConsistencyAttack import ConsistencyAttack
    from .Configuration import Configuration


class ChainQualityMeasurement(MeasurementBase):
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
        logging.info("Round {}".format(round))
        logging.info("Calculating Chain Quality...")
        corrupted_set = set([c for c in self._adversary._corrupted_nodes])
        for node in self._honest_nodes:
            logging.debug(node.id)
            chain_quality = []
            chain_T = []
            cnt = 0
            chain = cast(HonestNode, node).main_chain
            max_len = max(0, len(chain) - self._config.confirm_time)
            for i in range(1, len(chain)):
                if (i < max_len):
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

            cnt = min(cnt, max_len - 1)

            if max_len <= 1:
                chain_quality_value = 1.0
            else:
                chain_quality_value = (1 - cnt / (max_len - 1))
            logging.info("Chain Quality: %f" % chain_quality_value)
            logging.debug(list(chain_quality), list(chain_T))

    def report_final(self):
        logging.info("Calculating Chain Quality...")
        corrupted_set = set([c for c in self._adversary._corrupted_nodes])
        for node in self._honest_nodes:
            logging.debug(node.id)
            chain_quality = []
            chain_T = []
            cnt = 0
            chain = cast(HonestNode, node).main_chain
            max_len = max(0, len(chain) - self._config.confirm_time)
            for i in range(1, len(chain)):
                if (i < max_len):
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

            cnt = min(cnt, max_len - 1)

            if max_len <= 1:
                chain_quality_value = 1.0
            else:
                chain_quality_value = (1 - cnt / (max_len - 1))
            logging.info("Chain Quality: %f" % chain_quality_value)
            logging.debug(list(chain_quality), list(chain_T))
            return chain_quality_value
