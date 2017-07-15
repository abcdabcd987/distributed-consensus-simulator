import hashlib
from collections import defaultdict
from typing import *
from dcsim.framework import *
from .common import TBlock, D_p, SuperRoot, Timestamp, Tx
from .CorruptedNode import CorruptedNode
if TYPE_CHECKING:
    from .Configuration import Configuration


def check(id: int, timestamp: int):
    sha = hashlib.sha256()
    sha.update(("%d%d" % (id, timestamp)).encode("utf-8"))
    return sha.hexdigest() < D_p


class TransactionPool:
    def __init__(self) -> None:
        self._keys = set()  # type: Set[Tx]

    def contain_key(self, tx: 'Tx'):
        return tx in self._keys

    def insert(self, tx: 'Tx'):
        self._keys.add(tx)

    def get_all(self):
        return list(self._keys)

    def erase(self, tx: 'Tx'):
        self._keys.remove(tx)

    def clear(self):
        self._keys.clear()


class BlockTree():
    def __init__(self, key) -> None:
        self._depth = 0
        self._blockPool = {SuperRoot.hashval: SuperRoot}
        # Add main_chain for adversary
        self._main_chain = [SuperRoot]

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def main_chain(self):
        return self._main_chain

    def insert(self, cur: TBlock):
        if cur.hashval in self._blockPool.keys():
            return
        tmp = cur
        seq = []
        while tmp.hashval != SuperRoot.hashval:
            seq.append(tmp)
            # print("AdversaryController - BlockTree.insert: searching %s %s" % (tmp.hashval, tmp.pbhv))
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
            # self._depth = max(self._depth, len(seq))
            # reset main_chain
            if len(seq) > self._depth:
                self._main_chain = [SuperRoot]
                seq.reverse()
                for node in seq:
                    self._main_chain.append(node)
                self._depth = len(seq)


def valid(block: TBlock, timestamp: int):
    return check(block.id, block.round) and block.round <= timestamp


class AdversaryController(AdversaryControllerBase):
    def __init__(self, corrupted_nodes: Tuple['CorruptedNode', ...], config: 'Configuration') -> None:
        super().__init__(corrupted_nodes, config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()
        self._pending_messages = defaultdict(list)  # type: DefaultDict[int, List['MessageTuple']]

    def give_instruction(self, round: int) -> None:
        for badNode in self._corrupted_nodes:
            if check(badNode.id, round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, round), badNode.id)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) - 2 > self._root._depth + self._config.confirm_time:
                    cast(CorruptedNode, badNode).add_send(self._chain)
                    self._chain = [SuperRoot]
                    print("Corrupt chain pushed")
        print("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))

    def _handle_new_messages(self, round:int, new_messages: List['MessageTuple']):
        for message_tuple in new_messages:
            message = message_tuple.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], round):
                    self._root.insert(message["value"])

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages[round + self._config.max_delay] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def add_corrupted_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages[round + 1] += messages_to_send
        self._handle_new_messages(round, messages_to_send)

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        return self._pending_messages.pop(round, [])
