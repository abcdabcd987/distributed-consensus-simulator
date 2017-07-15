import hashlib
from collections import deque, defaultdict
from typing import *
from dcsim.framework import *
from .common import TBlock, D_p, SuperRoot, Timestamp, Tx
from .CorruptedNode import CorruptedNode
from .AdversaryController import TransactionPool, valid, check, BlockTree
if TYPE_CHECKING:
    from .Configuration import Configuration


class SelfishMining(AdversaryControllerBase):
    def __init__(self, corrupted_nodes: Tuple['CorruptedNode', ...], config: 'Configuration') -> None:
        super().__init__(corrupted_nodes, config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()
        self._bad_nodes = deque()
        self._tmp_blocks = deque()
        self._last_chain_len = 0
        self._round_honest_mined = False
        self._pending_messages = defaultdict(list)  # type: DefaultDict[int, List['MessageTuple']]

    @property
    def main_chain(self):
        return self._root.main_chain

    def give_instruction(self, current_round: int):
        print("Adversary Information:")

        len_changed = False

        # for message_tuple in new_message:
        #     message = message_tuple.message
        #     if message["type"] == 1 and valid(message["value"], current_round):
        #         round_honest_mined = True
        #         self._root.insert(message["value"])

        if self._root.depth > self._last_chain_len:
            self._last_chain_len = self._root.depth
            len_changed = True

        # for message_tuple in old_message:
        #     message = message_tuple.message
        #     if message["type"] == 0:
        #         if not self._tx.contain_key(message["value"]):
        #             self._tx.insert(message["value"])
        #     else:
        #         if valid(message["value"], current_round):
        #             self._root.insert(message["value"])

        for badNode in self._corrupted_nodes:
            if check(badNode.id, current_round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                self._bad_nodes.append(badNode)
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, current_round), badNode.id)
                self._tmp_blocks.append(block)
                self._tx.clear()
                self._chain.append(block)

        print("Root Depth %d" % self._root.depth)
        print("Chain Length %d" % (len(self._chain) - 1))
        print("Honest Mined? %r" % self._round_honest_mined)
        print("# Bad Nodes in Queue: %d" % len(self._bad_nodes))
        print("# Pending Blocks in Private Chain: %d" % len(self._tmp_blocks))

        if self._round_honest_mined and len_changed:
            if len(self._chain) - 1 < self._root.depth:
                print("Reset Private Chain...")
                self._chain = self.main_chain
                self._bad_nodes.clear()
                self._tmp_blocks.clear()
            elif len(self._bad_nodes) > 0:
                print("Cover Honest's New Block...")
                tmp = self._bad_nodes.popleft()
                cast(CorruptedNode, tmp).add_send([self._tmp_blocks.popleft()])

        self._round_honest_mined = False

    def _handle_new_messages(self, round: int, new_messages: List['MessageTuple']):
        for message_tuple in new_messages:
            message = message_tuple.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], round):
                    self._round_honest_mined = True
                    self._root.insert(message["value"])

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages[round + self._config.max_delay] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def add_corrupted_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages[round + 1] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        return self._pending_messages.pop(round, [])
