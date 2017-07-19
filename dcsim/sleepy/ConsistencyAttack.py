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
    check whether a node is the leader at this round

    :param id: the id of the node
    :param timestamp: the timestamp of this round
    :return: a boolean variable that decides whether this node is the leader at this round
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
        insert a transaction into the transaction pool

        :param tx: the inserted transaction
        """
        self._keys.add(tx)

    def get_all(self):
        """
        get all the transactions in transaction pool

        :return: A list contains all transactions in transaction pool
        """
        return list(self._keys)

    def erase(self, tx: 'Tx'):
        """
        delete a given trasaction from transaction pool
        """
        self._keys.remove(tx)

    def clear(self):
        """
        clear all the transactions in transaction pool
        """
        self._keys.clear()


class BlockTree():
    """
    the blockchain of a node, which is actually a blocktree
    """
    def __init__(self, key) -> None:
        """
        initialze the blocktree with root of it

        :param key: useless
        :param depth: length of main chain
        :param _blockPool: store all blocks of blocktree
        :param _main_chain: longest chain of blocktree
        """

        self._depth = 0
        self._blockPool = {SuperRoot.hashval: SuperRoot}
        self._main_chain = [SuperRoot]

    @property
    def depth(self) -> int:
        """
        return the depth of the blocktree

        :return: the depth of the blocktree
        """
        return self._depth

    @property
    def main_chain(self):
        return self._main_chain

    def insert(self, cur: TBlock):
        """
        insert a given TBlock into the blocktree

        :param cur: the inserted TBlock
        """

        #check whether this TBlock is already in blocktree
        if cur.hashval in self._blockPool.keys():
            return
        tmp = cur
        #seq contains the chain from cur to root
        seq = []
        while tmp.hashval != SuperRoot.hashval:
            seq.append(tmp)
            #print("AdversaryController - BlockTree.insert: searching %s %s" % (tmp.hashval, tmp.pbhv))
            tmp = self._blockPool.get(tmp.pbhv, None)
            if tmp is None:
                break
        #if tmp is None, then the chain contains cur is incomplete and still wating for the receiving of some blocks
        if tmp is None:
            self._blockPool[cur.hashval] = cur
        else:
            self._blockPool[cur.hashval] = cur
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            # self._depth = max(self._depth, len(seq))
            seq.reverse()
            #check whether seq is the longest chain, if so, update the main chain
            if len(seq) > self._depth:
                self._main_chain = [SuperRoot]
                for node in seq:
                    self._main_chain.append(node)
            self._depth = len(seq)


def valid(block: TBlock, timestamp: int, probability):
    """
    decide whether a block is valid

    :param block: the given block
    :param timestamp: the current timestamp
    :return: whether the block is valid
    """
    return check(block.id, block.round, probability) and block.round <= timestamp


class ConsistencyAttack(AdversaryControllerBase):
    """
    attack intends to break the consistency of blockchain
    """
    def __init__(self, config: 'Configuration') -> None:
        """
        Initalize the Adversary Controller, set the config

        :param config: Configuration of the protocol
        :param _chain: private chain
        :param _pending_messagees: the pending messages at each round
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
        """
        action of Adversary Controller in this round
        """
        for bad_node_id in self._corrupted_nodes:
            #find the leader of this round
            if check(bad_node_id, round, self._probabiltiy):
                logging.debug('AdversaryController.round_action: NodeId', bad_node_id, 'chosen as the leader')
                #mine new block
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, round), bad_node_id)
                self._tx.clear()
                #check the validity of timestamp
                if self._chain[-1].timestamp < block.timestamp:
                    self._chain.append(block)
                if len(self._chain) - 2 > self._root.depth:
                #condition satisfied, attack!
                    logging.debug("Attacking honest length %d, corrupt chain length %d" %
                                  (self._root.depth, len(self._chain) - 1))
                    chain_to_broadcast = self._chain
                    self._chain = [SuperRoot]
                    pending_messages = self._pending_messages[round + 1]
                    for corrupted_node in self._corrupted_nodes:
                        ttp = self._trusted_third_parties[corrupted_node]
                        for honest_node in self._honest_nodes:
                            for block in chain_to_broadcast:
                                sig = ttp.call('FSign', 'sign', message=block.serialize)
                                packed = {"type": 1, "value": block, "signature": sig}
                                t = MessageTuple(sender=corrupted_node, receiver=honest_node,
                                                 round=round, message=packed)
                                pending_messages.append(t)
                    logging.debug("Corrupt chain pushed")
        logging.debug("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))

    def _handle_new_messages(self, round: int, new_messages: List['MessageTuple']):
        """
        handle the new messages, insert message into transaction pool or blocktree

        :param round: the current round
        :param new_messages: the new messages
        """
        for message_tuple in new_messages:
            message = message_tuple.message
            if message["type"] == 0:
            #the message is a tx
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
            #the message is a block
                if valid(message["value"], round, self._probabiltiy):
                    self._root.insert(message["value"])

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        """
        add new messages from the honest nodes, delay all of them by delta rounds

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
