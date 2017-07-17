import os
import abc
from typing import *

from dcsim.framework import RunnerBase
from dcsim.framework import Context
from dcsim.framework import ExperimentBase
from dcsim.framework import AuthenticationServiceBase
from dcsim.sleepy import Configuration


<<<<<<< HEAD:dcsim/sleepy/Runner.py

=======
>>>>>>> 4849f6d6d1051ef332f7431b9cd42b1ca118f6f3:dcsim/sleepy/Runner.py
class Runner(ExperimentBase):
    def __init__(self, config: Configuration) -> None:
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
        self._authentication_service = config.authentication_service_type() # type: AuthenticationServiceBase
        self._authentication_service.generate_keys(self._node_ids)

    def run(self):
        """
        run the simulation, until the measure decides whether it should stop
        """
        round = 0
        while not self._measure.should_stop(round):
            round += 1

            # let the adversary to decide which messages will be delivered at this round
            pending_messages = self._adversary.get_delivered_messages(round)

            # group messages that hasn't been delivered before this round by receiver
            receiver_messages = {node.id: [] for node in self._nodes}  # type: Dict[NodeId, List[MessageTuple]]
            for message in pending_messages:
                receiver_messages[message.receiver].append(message)

            # run honest nodes
            for node in self._honest_nodes:
                # let the node action and collect new messages
                ctx = Context(self._authentication_service, self._node_ids, round, node, receiver_messages[node.id])
                node.round_action(ctx)
                self._adversary.add_honest_node_messages(round, node.id, ctx.messages_to_send)

            # adversary can gives instructions to corrupted nodes according to pending messages
            # and also honest nodes' messages in this round.
            self._adversary.give_instruction(round)

            # run corrupted nodes
            for node in self._corrupted_nodes:
                ctx = Context(self._authentication_service, self._node_ids, round, node, receiver_messages[node.id])
                node.round_action(ctx)
                self._adversary.add_corrupted_node_messages(round, node.id, ctx.messages_to_send)

            # call the Measurement to give some report
            self._measure.report_round(round)

        # call the Measurement to give the final report
        return self._measure.report_final()
