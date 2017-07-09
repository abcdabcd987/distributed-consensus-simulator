from typing import *
from dcsim.framework import *
import hashlib
import random

D_p = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

def check(id:int, timestamp:int):
    sha = hashlib.sha256()
    sha.update(("%d%d"% (id, timestamp)).encode("utf-8"))
    if sha.hexdigest() < D_p:
        return True
    else:
        return False


class transaction():

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


class txPool():

    def __init__(self):
        self._keys = {}

    def containKey(self, key):
        return key in self._keys.keys()

    def insert(self, key):
        self._keys[key.id] = key

    def getAll(self):
        res = ""
        for item in self._keys.values():
            res.join("(%d,%s)" % (item.id, item.key))
        return res

    def clear(self):
        self._keys = {}


class bNode():

    def __init__(self, prehsh, txs, time, id, hsh):
        self._prehsh = prehsh
        self._txs = txs
        self._round = time
        self._id = id
        self._hsh = hsh

    @property
    def id(self):
        return self._id

    @property
    def hsh(self) -> str:
        return self._hsh

    @property
    def prehsh(self) -> str:
        return self._prehsh

    @property
    def round(self) -> int:
        return self.round


class blockTree():

    def __init__(self, key):
        self._key = key
        self._children = []
        self._blockPool = {}
        self._depth = 0

    @property
    def depth(self) -> int:
        return self._depth

    @property
    def key(self) -> bNode:
        return self._key

    @property
    def children(self):
        return self._children

    def containChild(self, cur:bNode):
        for child in self._children:
            if child.hsh == cur.hsh:
                return True
        return False

    def insert(self, cur:bNode):
        tmp = cur
        seq = []
        while tmp.prehsh != "":
            seq.append(tmp)
            tmp = self._blockPool.get(tmp.prehsh, default="404")
        if tmp == "404":
            self._blockPool[cur.hsh] = cur
        else:
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            self._depth = max(self._depth, len(seq))


empty_Node = bNode("", "", 0, 0, "ROOT")


def valid(block: bNode, timestamp: int):
    return check(block.id, block.round) and block.round <= timestamp


class AdversaryController(AdversaryControllerBase):
    def __init__(self):
        self._root = blockTree(empty_Node)
        self._chain = [empty_Node]
        self._tx = txPool()

    def round_instruction(self,
                          corrupted_nodes: List[NodeBase],
                          pending_messages: List[MessageTuple],
                          current_round: int) -> Dict['NodeId', Any]:
        for message in pending_messages:
            if message["type"] == 0:
                if not self._tx.containKey(message["value"]):
                    self._tx.insert(message["value"])
            else:
                if valid(message["value"], current_round):
                    self._root.insert(message["value"])

        for badNode in corrupted_nodes:
            if check(badNode.id, current_round):
                srcStr = "".join(self._chain[-1].hsh).join(self._tx.getAll()).join("%d" % current_round).join("%d" % badNode.id)
                hsh = hashlib.sha256(srcStr.encode("utf-8")).hexdigest()
                block = bNode(self._chain[-1].hsh, self._tx.getAll(), current_round, badNode.id, hsh)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) > self._root._depth + T:
                    badNode.addSend(self._chain)
