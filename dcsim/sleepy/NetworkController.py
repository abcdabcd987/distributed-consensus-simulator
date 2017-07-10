from typing import *
from dcsim.framework import *


class NetworkController(NetworkControllerBase):
    def round_filter(self,
                     messages_to_send: List[MessageTuple],
                     max_delay: int,
                     current_round: int,
                     corrupted_nodes: List[NodeBase]) -> List[bool]:
        print('NetworkController.round_filter')
        corrupted_set = set([c.id for c in corrupted_nodes])
        res = []
        for messageTuple in messages_to_send:
            if messageTuple.sender in corrupted_set:
                res.append(True)
            elif current_round - messageTuple.round == max_delay:
                res.append(True)
            else:
                res.append(False)
        return res
