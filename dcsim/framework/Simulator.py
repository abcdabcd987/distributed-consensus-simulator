from typing import *
from .ConfigurationBase import ConfigurationBase
from .Coordinator import Coordinator
from .Context import Context


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        self.coordinator = Coordinator(configuration=config)

        num_corrupted_nodes = int(config.get_num_nodes() * config.get_ratio_corrupted())
        num_honest_nodes = config.get_num_nodes() - num_corrupted_nodes
        self.honest_nodes = [config.get_honest_node_type()() for _ in range(0, num_honest_nodes)]
        self.corrupted_nodes = [config.get_corrupted_node_type()() for _ in range(0, num_corrupted_nodes)]
        self.nodes = self.honest_nodes + self.corrupted_nodes
        for node in self.nodes:
            self.coordinator.add_node(node)
        self.network = config.get_network_controller_type()()
        self.adversary = config.get_adversary_controller_type()()
        self.measure = config.get_measurement_type()(self.corrupted_nodes, self.honest_nodes, self.network, self.adversary)
        self.trust_length = config.get_trust_length()
        self.max_delay = config.get_max_delay()

    def run(self):
        round_counter = 0
        pending_message_tuples = []
        # received_message_tuples = []
        while not self.measure.should_stop(round_counter):
            # increase round counter
            round_counter += 1
            print('Simulator: current round', round_counter)
            # get adversarial instructions from adversary controller
            adversarial_instructions = self.adversary.round_instruction(self.corrupted_nodes, pending_message_tuples, round_counter, self.trust_length)

            # filter message to deliver
            filtered = self.network.round_filter(pending_message_tuples, self.max_delay, round_counter, self.corrupted_nodes)
            received_message_tuples = [m for m, p in zip(pending_message_tuples, filtered) if p]
            pending_message_tuples = [message_tuple
                                      for message_tuple in pending_message_tuples
                                      if message_tuple not in received_message_tuples
                                      ]
            for node in self.nodes:
                ctx = Context(round_counter, node, self.coordinator, received_message_tuples, adversarial_instructions)
                node.round_action(ctx)
                pending_message_tuples += ctx.get_messages_to_send()
            self.measure.report_every(self.honest_nodes, self.corrupted_nodes, round_counter)
        self.measure.report()
