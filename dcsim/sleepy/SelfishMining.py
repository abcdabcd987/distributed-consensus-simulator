import hashlib
from collections import deque, defaultdict
from typing import *
from dcsim.framework import *
from dcsim.sleepy.ConsistencyAttack import BlockTree, TransactionPool, check, valid
from dcsim.sleepy.utils import SuperRoot, TBlock, Timestamp
import logging

if TYPE_CHECKING:
    from .Configuration import Configuration


class SelfishMining(AdversaryControllerBase):
    def __init__(self, config: 'Configuration') -> None:
        super().__init__(config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()
        self._bad_nodes = deque()
        self._tmp_blocks = deque()
        self._last_chain_len = 0
        self._round_honest_mined = False
        self._pending_messages = defaultdict(list)  # type: DefaultDict[int, List['MessageTuple']]
        self._probabiltiy = config.probability

    def set_trusted_third_party(self, node_id: 'NodeId', trusted_third_party: 'TrustedThirdPartyCaller'):
        super().set_trusted_third_party(node_id, trusted_third_party)
        self._trusted_third_parties[node_id].call('FSign', 'register')

    @property
    def main_chain(self):
        return self._root.main_chain

    def round_action(self, round: int):
        logging.debug("Adversary Information:")

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

        for bad_node_id in self._corrupted_nodes:
            if check(bad_node_id, round, self._probabiltiy):
                logging.debug('AdversaryController.round_instruction: NodeId', bad_node_id, 'chosen as the leader')
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, round), bad_node_id)
                self._tx.clear()

                if self._chain[-1].timestamp < block.timestamp:
                    self._bad_nodes.append(bad_node_id)
                    self._tmp_blocks.append(block)
                    self._chain.append(block)

        logging.debug("Root Depth %d" % self._root.depth)
        logging.debug("Chain Length %d" % (len(self._chain) - 1))
        logging.debug("Honest Mined? %r" % self._round_honest_mined)
        logging.debug("# Bad Nodes in Queue: %d" % len(self._bad_nodes))
        logging.debug("# Pending Blocks in Private Chain: %d" % len(self._tmp_blocks))

        if self._round_honest_mined and len_changed:
            if len(self._chain) - 1 < self._root.depth:
                logging.debug("Reset Private Chain...")
                self._chain = self.main_chain
                self._bad_nodes.clear()
                self._tmp_blocks.clear()
            elif len(self._bad_nodes) > 0:
                logging.debug("Cover Honest's New Block...")
                corrupted_node = self._bad_nodes.popleft()
                block = self._tmp_blocks.popleft()

                pending_messages = self._pending_messages[round + 1]
                ttp = self._trusted_third_parties[corrupted_node]
                for honest_node in self._honest_nodes:
                    sig = ttp.call('FSign', 'sign', message=block.serialize)
                    packed = {"type": 1, "value": block, "signature": sig}
                    t = MessageTuple(sender=corrupted_node, receiver=honest_node, round=round, message=packed)
                    pending_messages.append(t)

        self._round_honest_mined = False

    def _handle_new_messages(self, round: int, new_messages: List['MessageTuple']):
        for message_tuple in new_messages:
            message = message_tuple.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], round, self._probabiltiy):
                    self._round_honest_mined = True
                    self._root.insert(message["value"])

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages[round + self._config.max_delay] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        return self._pending_messages.pop(round, [])
