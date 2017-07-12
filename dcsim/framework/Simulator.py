from typing import *
from .ConfigurationBase import ConfigurationBase
from .Coordinator import Coordinator
from .Context import Context
from .MessageTuple import MessageTuple
from .NodeId import NodeId


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        self.coordinator = Coordinator(configuration=config)
        self._config = config

        num_corrupted_nodes = int(config.num_nodes * config.ratio_corrupted)
        num_honest_nodes = config.num_nodes - num_corrupted_nodes
        self.honest_nodes = [config.honest_node_type(config) for _ in range(0, num_honest_nodes)]
        self.corrupted_nodes = [config.corrupted_node_type(config) for _ in range(0, num_corrupted_nodes)]
        self.nodes = self.honest_nodes + self.corrupted_nodes
        for node in self.nodes:
            self.coordinator.add_node(node)
        self.network = config.network_controller_type(config)
        self.adversary = config.adversary_controller_type(self.corrupted_nodes, config)
        self.measure = config.measurement_type(self.corrupted_nodes, self.honest_nodes, self.network, self.adversary, config)

    def run(self):
        round = 0
        honest_messages_to_send = {node.id: [] for node in self.honest_nodes}  # type: Dict[NodeId, List[MessageTuple]]
        corrupted_messages_to_send = {node.id: [] for node in self.corrupted_nodes}  # type: Dict[NodeId, List[MessageTuple]]

        while not self.measure.should_stop(round):
            round += 1

            for node in self.honest_nodes:
                received_messages = []
                messages_to_send = []
                filtered = self.network.round_filter(honest_messages_to_send[node.id], round)
                for message, send_now in zip(honest_messages_to_send[node.id], filtered):
                    if send_now:
                        received_messages.append(message)
                    else:
                        messages_to_send.append(message)

                ctx = Context(round, node, self.coordinator, received_messages)
                node.round_action(ctx)
                messages_to_send += ctx.messages_to_send
                honest_messages_to_send[node.id] = messages_to_send

            self.adversary.round_instruction(honest_messages_to_send, corrupted_messages_to_send, round)
            for node in self.corrupted_nodes:
                ctx = Context(round, node, self.coordinator, corrupted_messages_to_send[node.id])
                node.round_action(ctx)
                corrupted_messages_to_send[node.id] = ctx.messages_to_send

            self.measure.report_round(round)
        self.measure.report_final()
