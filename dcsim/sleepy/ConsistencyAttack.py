import hashlib
from collections import defaultdict
from typing import *
from typing import TYPE_CHECKING, List, cast, Tuple

import logging

from dcsim.framework import *
from .utils import TBlock, SuperRoot, Timestamp, Tx
if TYPE_CHECKING:
    from .Configuration import Configuration


def check(id: int, timestamp: int, probability):
    """
    check whether a node is awake
    :param id: the id of the node
    :param timestamp: the timestap of this round
    :return: a boolean variable that decides whether a ode is awake
    """
    sha = hashlib.sha256()
    sha.update(("%d%d" % (id, timestamp)).encode("utf-8"))
    d_p = 2.0 ** 256 * probability
    return int(sha.hexdigest(), 16) < d_p


class TransactionPool:
    def __init__(self) -> None:
        """
        Initialze the transactionpool
        """
        self._keys = set()  # type: Set[Tx]

    def contain_key(self, tx: 'Tx'):
        """
        return whether a given transaction is in the pool
        :param tx: the given transaction
        :return: whether a given transaction is in the pool
        """
        return tx in self._keys

    def insert(self, tx: 'Tx'):
        """
        insert the transaction to the transactionpool
        :param tx: the inserted transaction
        """
        self._keys.add(tx)

    def get_all(self):
        """
        get all the transaction to a list
        :return: A list contains all the transactions
        """
        return list(self._keys)

    def erase(self, tx: 'Tx'):
        """
        delete a given trasaction
        :param tx:
        """
        self._keys.remove(tx)

    def clear(self):
        """
        clear all the transactions in the pool
        """
        self._keys.clear()


class BlockTree():
    def __init__(self, key) -> None:
        """
        initialze the blocktree, determins the root of the tree
        :param key: useless
        """
        self._depth = 0
        self._blockPool = {SuperRoot.hashval: SuperRoot}

    @property
    def depth(self) -> int:
        """
        return the depth of the blocktree
        :return: the depth of the blocktree
        """
        return self._depth

    def insert(self, cur: TBlock):
        """
        insert a given block to the blocktree
        :param cur: the inserted block
        :return: none
        """
        if cur.hashval in self._blockPool.keys():
            return
        tmp = cur
        seq = []
        while tmp.hashval != SuperRoot.hashval:
            seq.append(tmp)
            #print("AdversaryController - BlockTree.insert: searching %s %s" % (tmp.hashval, tmp.pbhv))
            tmp = self._blockPool.get(tmp.pbhv, None)
            if tmp is None:
                break
        if tmp is None:
            self._blockPool[cur.hashval] = cur
        else:
            self._blockPool[cur.hashval] = cur
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            self._depth = max(self._depth, len(seq))


def valid(block: TBlock, timestamp: int, probability):
    """
        decide whether a block is valid
    :param block: the given block
    :param timestamp: the current timestamp
    :return: whether the block is valid
    """
    return check(block.id, block.round, probability) and block.round <= timestamp


class ConsistencyAttack(AdversaryControllerBase):
    def __init__(self, config: 'Configuration') -> None:
        """
        Initalize the Adversary Controller, set the config and the number of the corrupted nodes,
        :param corrupted_nodes: A tuple contains the corrupted nodes
        :param config: Configuration of the protocol
        """
        super().__init__(config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()
        self._pending_messages = defaultdict(list)  # type: DefaultDict[int, List['MessageTuple']]
        self._probabiltiy = config.probability

    def set_trusted_third_party(self, node_id: 'NodeId', trusted_third_party: 'TrustedThirdPartyCaller'):
        super().set_trusted_third_party(node_id, trusted_third_party)
        self._trusted_third_parties[node_id].call('FSign', 'register')

    def round_action(self, round: int) -> None:
        for bad_node_id in self._corrupted_nodes:
            if check(bad_node_id, round, self._probabiltiy):
                logging.debug('AdversaryController.round_action: NodeId', bad_node_id, 'chosen as the leader')
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, round), bad_node_id)
                self._tx.clear()
                if self._chain[-1].timestamp < block.timestamp:
                    self._chain.append(block)
                if len(self._chain) - 2 > self._root.depth:
                    logging.debug("Attacking honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))
                    chain_to_broadcast = self._chain
                    self._chain = [SuperRoot]

                    pending_messages = self._pending_messages[round + 1]
                    for corrupted_node in self._corrupted_nodes:
                        ttp = self._trusted_third_parties[corrupted_node]
                        for honest_node in self._honest_nodes:
                            for block in chain_to_broadcast:
                                sig = ttp.call('FSign', 'sign', message=block.serialize)
                                packed = {"type": 1, "value": block, "signature": sig}
                                t = MessageTuple(sender=corrupted_node, receiver=honest_node, round=round, message=packed)
                                pending_messages.append(t)
                    logging.debug("Corrupt chain pushed")
        logging.debug("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))

    def _handle_new_messages(self, round:int, new_messages: List['MessageTuple']):
        """
        handle the new messages, insert message to the block tree or transaction
        :param round: the current round
        :param new_messages: the new messages
        """
        for message_tuple in new_messages:
            message = message_tuple.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], round, self._probabiltiy):
                    self._root.insert(message["value"])

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        """
        add new messages from the honest nodes
        :param round: the round that the messages are in
        :param sender_id: the id of the sender
        :param messages_to_send: A list that contains the new messages
        """
        self._pending_messages[round + self._config.max_delay] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        """
        Get the delivered messages from all the nodes, returns a list contains all the messagetuples
        :param round: the round that these messages are in
        :return: a list contains all the messagetuples
        """
        return self._pending_messages.pop(round, [])
