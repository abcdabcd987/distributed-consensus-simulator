import os
from typing import *
from .ConfigurationBase import ConfigurationBase
from .Context import Context
from .MessageTuple import MessageTuple
from .NodeId import NodeId


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        num_corrupted_nodes = int(config.num_nodes * config.ratio_corrupted)
        num_honest_nodes = config.num_nodes - num_corrupted_nodes
        self._honest_nodes = tuple(config.honest_node_type(config) for _ in range(0, num_honest_nodes))
        self._corrupted_nodes = tuple(config.corrupted_node_type(config) for _ in range(0, num_corrupted_nodes))
        self._nodes = self._honest_nodes + self._corrupted_nodes
        self._node_ids = tuple(node.id for node in self._nodes)
        self._secret_keys = {id: Simulator._generate_secret_key() for id in self._node_ids}
        for node in self._nodes:
            node.set_node_list(self._node_ids)

        self._config = config
        self._network = config.network_controller_type(config)
        self._adversary = config.adversary_controller_type(self._corrupted_nodes, config)
        self._measure = config.measurement_type(self._corrupted_nodes, self._honest_nodes, self._network, self._adversary, config)

    @staticmethod
    def _generate_secret_key():
        return os.urandom(16)

    def run(self):
        # pending_messages : messages that hasn't been delivered before this round
        # messages_dict    : pending_messages grouped by receiver
        # delayed_messages : messages that NetworkController decides not to be delivered in this round
        # received_messages: messages that will be received in this round by a certain honest node
        # new_messages     : messages produced in this round

        round = 0
        pending_messages = []  # type: List[MessageTuple]

        while not self._measure.should_stop(round):
            round += 1

            # group messages that hasn't been delivered before this round by receiver
            messages_dict = {node.id: [] for node in self._nodes}  # type: Dict[NodeId, List[MessageTuple]]
            for message in pending_messages:
                messages_dict[message.receiver].append(message)

            # run honest nodes
            delayed_messages = []
            new_messages = []
            for node in self._honest_nodes:
                # call NetworkController to determine whether a message sent to this node
                # should be delivered in this round or not
                received_messages = []
                filtered = self._network.round_filter(messages_dict[node.id], round)
                for message, send_now in zip(messages_dict[node.id], filtered):
                    if send_now:
                        received_messages.append(message)
                    else:
                        delayed_messages.append(message)

                # let the node action and collect new messages
                ctx = Context(self._node_ids, self._secret_keys, round, node, received_messages)
                node.round_action(ctx)
                new_messages += ctx.messages_to_send

            # adversary can gives instructions to corrupted nodes according to pending messages
            # and also honest nodes' messages in this round.
            self._adversary.round_instruction(new_messages, pending_messages, round)

            # run corrupted nodes
            for node in self._corrupted_nodes:
                ctx = Context(self._node_ids, self._secret_keys, round, node, messages_dict[node.id])
                node.round_action(ctx)
                new_messages += ctx.messages_to_send

            # new messages as well as old messages that have been delayed should be considered in the next round
            pending_messages = delayed_messages + new_messages

            # call the Measurement to give some report
            self._measure.report_round(round)

        # call the Measurement to give the final report
        self._measure.report_final()
