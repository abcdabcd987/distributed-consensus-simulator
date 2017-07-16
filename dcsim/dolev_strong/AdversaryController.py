import hashlib
import random
from dcsim.framework import *
from typing import *
from .common import *
if TYPE_CHECKING:
    from .Configuration import Configuration
    from .CorruptedNode import CorruptedNode


class AdversaryController(AdversaryControllerBase):
    def give_round0_instruction(self, senders: Tuple['NodeId', ...]) -> None:
        for cur_node in self._corrupted_nodes:
            if cur_node in senders:
                for hon_node_id in self._honest_node_ids:
                    cur_node.add_send(hon_node_id, self._First_msg)

                self._remain_corrupt_nodes.append(cur_node)

                corr_node = random.choice(self._corrupted_nodes)
                while corr_node in self._remain_corrupt_nodes:
                    corr_node = random.choice(self._corrupted_nodes)
                self._remain_corrupt_nodes.append(corr_node)

                cur_node.add_send(corr_node.id, self._Second_msg)

                self._this_sender = cur_node

                self._next_sender = corr_node

    def add_corrupted_node_messages(self, round: int, sender_id: 'NodeId',
                                    messages_to_send: List['MessageTuple']) -> None:
        self._msg[sender_id] = messages_to_send
    ##    print(len(self._msg[sender_id]))
        self._message_pool += messages_to_send

    def give_instruction(self, round: int) -> None:
        if round + 1 >= len(self._corrupted_nodes):
            t = self._corrupted_nodes[round % len(self._corrupted_nodes)]
        else:
            t = random.choice(self._corrupted_nodes)
            while t in self._remain_corrupt_nodes:
                t = random.choice(self._corrupted_nodes)
            self._remain_corrupt_nodes.append(t)


    ##    print(self._this_sender)
    ##    print(self._next_sender)
    ##    print()

        for msg in self._msg[self._this_sender.id]:
            if msg.receiver == self._next_sender.id:
                self._next_sender.add_send(t.id, msg.message)

        if round + 1 >= len(self._corrupted_nodes):
            for msg in self._msg[self._this_sender.id]:
                self._next_sender.add_send(random.choice(self._honest_node_ids), msg.message)

        self._this_sender = self._next_sender
        self._next_sender = t


    '''    if round + 1 < len(self._corrupted_nodes):
            for cur_node in self._corrupted_nodes:
                for msg in self._msg[cur_node.id]:
                    t = msg.receiver
                    if t in self._id_dict:
                        for corr_node in self._corrupted_nodes:
                            if (t != corr_node):
                                self._id_dict[t].add_send(corr_node.id, msg.message)
        
        if round + 1 == len(self._corrupted_nodes):
            rev = random.choice(self._honest_node_ids)
            for corr_node in self._corrupted_nodes:
                msgs = self._msg[corr_node.id]
                for msg in msgs:
                    if msg.receiver in self._id_dict:
                        self._id_dict[msg.receiver].add_send(rev, msg.message)'''


    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._message_pool += messages_to_send

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        m = self._message_pool
        self._message_pool = []
        return m

    def __init__(self, honest_node_ids: Tuple['NodeId', ...], corrupted_nodes: Tuple['CorruptedNode', ...],
                 config: 'ConfigurationBase'):
        super().__init__(honest_node_ids, corrupted_nodes, config)
        self._honest_node_ids = honest_node_ids
        self._corrupted_nodes = corrupted_nodes
        self._First_msg = Message(value = "Lele is a nice guy~", nodeId = None, signature = None)
        self._Second_msg = Message(value = "Lele is a cute guy~", nodeId = None, signature = None)
        self._msg = {node.id : [] for node in corrupted_nodes}  # type: Dict['NodeId', List['MessageTuple']]
        self._message_pool = []
        self._remain_corrupt_nodes = []
        self._next_sender = self._corrupted_nodes[0] # type: NodeBase
        self._this_sender = self._corrupted_nodes[0]
        self._id_dict = {node.id: node for node in corrupted_nodes}
        ##for node in corrupted_nodes:
        ##    self._id_dict[node.id] = node