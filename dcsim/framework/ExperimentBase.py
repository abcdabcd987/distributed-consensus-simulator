import os
import abc
from typing import *
from .RunnerBase import RunnerBase
from .Context import Context
from .MessageTuple import MessageTuple
from .NodeId import NodeId


class ExperimentBase:
    def __init__(self, config: RunnerBase) -> None:
        """
        initialze the simulator, including the number of corrupted/honest nodes, the information of each nodes, the configuration, the measurement
        :param config: the configuration of thel protocol
        """
        num_corrupted_nodes = int(config.num_nodes * config.ratio_corrupted)
        num_honest_nodes = config.num_nodes - num_corrupted_nodes
        self._honest_nodes = tuple(config.honest_node_type(config) for _ in range(0, num_honest_nodes))
        self._corrupted_nodes = tuple(config.corrupted_node_type(config) for _ in range(0, num_corrupted_nodes))
        self._nodes = self._honest_nodes + self._corrupted_nodes
        self._node_ids = tuple(node.id for node in self._nodes)
        self._secret_keys = {id: ExperimentBase._generate_secret_key() for id in self._node_ids}
        for node in self._nodes:
            node.set_node_list(self._node_ids)

        self._config = config
        self._adversary = config.adversary_controller_type(self._corrupted_nodes, config)
        self._measure = config.measurement_type(self._corrupted_nodes, self._honest_nodes, self._adversary, config)

    @staticmethod
    def _generate_secret_key():
        """
        generate the secret key
        :return:
        """
        return os.urandom(16)
    @abc.abstractclassmethod
    def run(self):
       pass
