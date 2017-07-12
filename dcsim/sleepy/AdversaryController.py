import hashlib
import itertools
from dcsim.framework import *
from .HonestNode import TBlock, D_p, SuperRoot
from typing import *
if TYPE_CHECKING:
    from .Configuration import Configuration
    from .CorruptedNode import CorruptedNode


def check(id:int, timestamp:int):
    sha = hashlib.sha256()
    sha.update(("%d%d"% (id, timestamp)).encode("utf-8"))
    return sha.hexdigest() < D_p


class TransactionPool:
    def __init__(self):
        self._keys = {}

    def contain_key(self, tx: str):
        return tx in self._keys.keys()

    def insert(self, tx: str):
        self._keys[tx] = 1

    def get_all(self):
        return [key for key in self._keys.keys()]

    def erase(self, tx: str):
        del self._keys[tx]

    def clear(self):
        self._keys.clear()


class BlockTree():
    def __init__(self, key):
        self._depth = 0
        self._blockPool = {SuperRoot.hashval:SuperRoot}

    @property
    def depth(self) -> int:
        return self._depth

    def insert(self, cur: TBlock):
        if cur.hashval in self._blockPool.keys():
            return
        tmp = cur
        seq = []
        while tmp.hashval != SuperRoot.hashval:
            seq.append(tmp)
            #print("AdversaryController - BlockTree.insert: searching %s %s" % (tmp.hashval, tmp.pbhv))
            tmp = self._blockPool.get(tmp.pbhv, "404")
            if tmp == "404":
                break
        if tmp == "404":
            self._blockPool[cur.hashval] = cur
        else:
            self._blockPool[cur.hashval] = cur
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            self._depth = max(self._depth, len(seq))


def valid(block: TBlock, timestamp: int):
    return check(block.id, block.round) and block.round <= timestamp


class AdversaryController(AdversaryControllerBase):
    def __init__(self, corrupted_nodes: List['NodeBase'], config: Type['Configuration']):
        super().__init__(corrupted_nodes, config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()

    def round_instruction(self,
                          new_messages: List[MessageTuple],
                          old_messages: List[MessageTuple],
                          current_round: int):
        for message_tuple in old_messages:
            message = message_tuple.message
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], current_round):
                    self._root.insert(message["value"])

        for badNode in self._corrupted_nodes:
            if check(badNode.id, current_round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                block = TBlock(self._chain[-1].hashval, self._tx.get_all(), current_round, badNode.id)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) - 2 > self._root._depth + self._config.confirm_time:
                    badNode.add_send(self._chain)
                    self._chain = [SuperRoot]
                    print("Corrupt chain pushed")
        print("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))
