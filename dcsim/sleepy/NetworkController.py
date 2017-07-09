from typing import *
from dcsim.framework import *


class NetworkController(NetworkControllerBase):
    def round_filter(self,
                     messages_to_send: List[MessageTuple],
                     max_delay: int,
                     current_round: int,
                     corrupted_nodes: List[NodeBase]) -> List[MessageTuple]:
        received_message_tuples = []
        for messageTuple in messages_to_send:
            if messageTuple.sender in [cNodes.id for cNodes in corrupted_nodes]:
                received_message_tuples.append(messageTuple)
            elif current_round - messageTuple.round == max_delay:
                received_message_tuples.append(messageTuple)
        return received_message_tuples
