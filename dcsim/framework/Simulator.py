from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        self.network_controller = config.get_network_controller_type()()
        self.adversary_controller = config.get_adversary_controller_type()()
        self.honest_nodes = [config.get_honest_node_type()() for _ in range(0, config.get_num_nodes)]
        

    def run(self):
        raise NotImplementedError
