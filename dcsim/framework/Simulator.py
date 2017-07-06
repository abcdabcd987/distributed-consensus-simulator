from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        num_corrupted_nodes = int(config.get_num_nodes() * config.get_ratio_corrupted())
        num_honest_nodes = config.get_num_nodes() - num_corrupted_nodes
        self.honest_nodes = [config.get_honest_node_type()() for _ in range(0, num_honest_nodes)]
        self.corrupted_nodes = [config.get_corrupted_node_type()() for _ in range(0, num_corrupted_nodes)]
        self.nodes = self.honest_nodes + self.corrupted_nodes

        self.network = config.get_network_controller_type()()
        self.adversary = config.get_adversary_controller_type()()
        self.measure = config.get_measurement_type()()

    def run(self):
        round = 0
        pending_messages = []
        received_messages = []
        while not self.measure.should_stop():
            round += 1
            adversary_instructions = self.adversary.round_instruction(self.corrupted_nodes, pending_messages)
            for node in self.nodes:
                ctx = Context(round, node, received_messages, adversary_instructions)
                node.round_action(ctx)
                pending_messages += ctx.messages_to_send
            received_messages = self.network.round_filter(pending_messages)
            
            pending_messages -= received_messages
        self.measure.report()
