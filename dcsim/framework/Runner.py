from collections import defaultdict
from typing import *
from .ConfigurationBase import ConfigurationBase
from .Context import Context
from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .TrustedThirdPartyCaller import TrustedThirdPartyCaller


class Runner:
    def __init__(self, config: ConfigurationBase) -> None:
        self._config = config
        self._ttps = []

    def add_trusted_third_party(self, ttp):
        self._ttps.append(ttp)

    def init(self):
        # create honest nodes
        self._honest_nodes = []
        for _ in range(self._config.num_honest_nodes):
            node = self._config.honest_node_type(self._config)
            ttp = TrustedThirdPartyCaller(self._ttps, node.id)
            node.set_trusted_third_party(ttp)
            self._honest_nodes.append(node)

        # create adversary
        self._adversary = self._config.adversary_controller_type(self._config)
        honest_node_ids = tuple(node.id for node in self._honest_nodes)
        self._node_ids = list(honest_node_ids) + self._adversary.corrupted_node_list
        self._adversary.set_honest_node_list(honest_node_ids)
        for corrupted_node_id in self._adversary.corrupted_node_list:
            ttp = TrustedThirdPartyCaller(self._ttps, corrupted_node_id)
            self._adversary.set_trusted_third_party(corrupted_node_id, ttp)

        # create measurement
        self._measure = self._config.measurement_type(self._honest_nodes, self._adversary, self._ttps, self._config)

    def run(self):
        round = 0
        while not self._measure.should_stop(round):
            round += 1

            # let the adversary to decide which messages will be delivered at this round
            pending_messages = self._adversary.get_delivered_messages(round)

            # group messages that hasn't been delivered before this round by receiver
            receiver_messages = defaultdict(list)  # type: DefaultDict[NodeId, List[MessageTuple]]
            for message in pending_messages:
                receiver_messages[message.receiver].append(message)

            # run honest nodes
            for node in self._honest_nodes:
                # let the node action and collect new messages
                ctx = Context(self._node_ids, round, node, receiver_messages[node.id])
                node.round_action(ctx)
                self._adversary.add_honest_node_messages(round, node.id, ctx.messages_to_send)

            # run the adversary
            self._adversary.round_action(round)

            # call the Measurement to give some report
            # self._measure.report_round(round)
            self._measure.report_selfish(round, self._adversary)

        # call the Measurement to give the final report
        return self._measure.report_final()
