import hashlib
import random
from dcsim.framework import *
from .HonestNode import TBlock, D_p
from typing import *
if TYPE_CHECKING:
    from .CorruptedNode import CorruptedNode


def check(id:int, timestamp:int):
    sha = hashlib.sha256()
    sha.update(("%d%d"% (id, timestamp)).encode("utf-8"))
    return sha.hexdigest() < D_p


class Transaction:
    def __init__(self, key="empty transaction"):
        random.seed()
        self._id = random.randint(0, 1 << 32)
        self._key = key

    @property
    def id(self):
        return self._id

    @property
    def key(self):
        return self.key


class TransactionPool:
    def __init__(self):
        self._keys = {}

    def contain_key(self, key):
        return key in self._keys.keys()

    def insert(self, key):
        self._keys[key.id] = key

    def get_all(self):
        res = ""
        for item in self._keys.values():
            res.join("(%d,%s)" % (item.id, item.key))
        return res

    def clear(self):
        self._keys = {}


class BlockTree():
    def __init__(self, key):
        self._key = key
        self._children = []
        self._blockPool = {}
        self._depth = 0

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def key(self) -> TBlock:
        return self._key

    @property
    def children(self):
        return self._children

    def contain_child(self, cur: TBlock):
        for child in self._children:
            if child.hash == cur.hashval:
                return True
        return False

    def insert(self, cur: TBlock):
        tmp = cur
        seq = []
        while tmp.prev_hash != "":
            seq.append(tmp)
            tmp = self._blockPool.get(tmp.prev_hash, "404")
            if tmp == "404":
                break
        if tmp == "404":
            self._blockPool[cur.hashval] = cur
        else:
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            self._depth = max(self._depth, len(seq))


EMPTY_NODE = TBlock("", "", 0, 0)


def valid(block: TBlock, timestamp: int):
    return check(block.id, block.round) and block.round <= timestamp


class AdversaryController(AdversaryControllerBase):
    def __init__(self):
        self._root = BlockTree(EMPTY_NODE)
        self._chain = [EMPTY_NODE]
        self._tx = TransactionPool()

    def round_instruction(self,
                          corrupted_nodes: List['CorruptedNode'],
                          pending_messages: List['MessageTuple'],
                          current_round: int,
                          confirm_time: int) -> Dict['NodeId', Any]:
        print('AdversaryController.round_instruction')
        for message in pending_messages:
            message = message.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], current_round):
                    self._root.insert(message["value"])

        ret = {}
        for badNode in corrupted_nodes:
            if check(badNode.id, current_round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), current_round, badNode.id)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) > self._root._depth + confirm_time:
                    badNode.add_send(self._chain)
                    self._chain = [EMPTY_NODE]
                ret[badNode.id] = None
        return ret