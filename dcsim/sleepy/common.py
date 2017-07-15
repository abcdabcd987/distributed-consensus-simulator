import hashlib
import pickle
from typing import *
from dcsim.framework import *

D_p = "0fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

Tx = NewType('Tx', bytes)
Hashval = NewType('Hashval', bytes)
Timestamp = NewType('Timestamp', int)

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

class TBlock:
    def __init__(self, pbhv: Hashval, txs: List[Tx], timestamp: Timestamp, pid: NodeId) -> None:
        # comes from TxPool
        self.txs = txs
        # father's hash
        self.pbhv = pbhv
        self.timestamp = timestamp
        self.pid = pid
        self.children = []  # type: List[TBlock]

    @property
    def id(self) -> int:
        return self.pid

    @property
    def round(self) -> int:
        return self.timestamp

    @property
    def hashval(self) -> Hashval:
        return cast(Hashval, hashlib.sha256(self.serialize).hexdigest())

    @property
    def serialize(self) -> bytes:
        return pickle.dumps((self.pbhv, self.txs, self.timestamp, self.pid))


class TNode:
    def __init__(self, depth, block, father):  # father's(block's) hash
        self.depth = depth  # type: int
        self.block = block  # type: TBlock
        # own hash
        self.hash = block.hashval  # type: Hashval
        self.father = father  # type: Optional['TNode']

        self.index = []  # type: List[int]
        self.children = []  # type: List[TNode]
        self.num = 0  # type: int

        if father is None:
            self.block.pbhv = "0"
        else:
            self.block.pbhv = father.hash

    def get_children(self):
        return self.children

    def get_child_index(self, child_node: 'TNode') -> int:
        for i in range(len(self.index)):
            if child_node.hash == self.children[self.index[i]].hash:
                return i
        return -1

    def add_child(self, new_node: 'TNode') -> bool:
        # if full, max is 16
        if len(self.children) == 16:
            return False
        else:
            self.children.append(new_node)
            self.index.append(self.num)
            self.num += 1
            new_node.depth = self.depth + 1
            new_node.father = self
            return True

    def transfer_chain(self, i: int, j: int):
        x = self.index[i]
        self.index[i] = self.index[j]
        self.index[j] = x

    def search(self, p_hash: Hashval) -> Optional['TNode']:
        res = None      # type: Union[TNode, None]
        for child in self.children:
            if child.hash == p_hash:
                return child
            else:
                res = child.search(p_hash)
                if res is not None:
                    break
        return res


SuperRoot = TBlock(cast(Hashval, b"0"), [], cast(Timestamp, 0), cast(NodeId, 0))


class BlockChain:

    def __init__(self) -> None:
        # pbhv = "0", txs = [], timestamp = 0, nid = 0
        self.genesis = TNode(0, SuperRoot, None)    # type: TNode
        self.head = self.genesis    # type: TNode
        self.tail = self.genesis    # type: TNode

    def find(self, hash_val: Hashval) -> Optional['TNode']:
        if self.head.hash == hash_val:
            return self.head
        else:
            return self.head.search(hash_val)

    def add_child(self, t_node: 'TNode', block: 'TBlock'):
        new_node = TNode(t_node.depth + 1, block, t_node)
        t_node.add_child(new_node)
        if new_node.depth > self.tail.depth:
            temp_node = new_node
            while temp_node is not self.head:
                index = temp_node.father.get_child_index(temp_node)
                if index is not 0 and index is not -1:
                    temp_node.father.transfer_chain(0, index)
                temp_node = temp_node.father
            self.tail = new_node
        return new_node

    @property
    def main_chain(self) -> List['TBlock']:
        temp_list = []              # type: List[TBlock]
        temp_node = self.genesis    # type: TNode
        while temp_node != self.tail:
            temp_list.append(temp_node.block)
            i = temp_node.index[0]
            temp_node = temp_node.children[i]
        temp_list.append(self.tail.block)
        return temp_list

    def get_top(self) -> TNode:
        return self.tail


class OrphanBlockPool:

    def __init__(self) -> None:
        self.block = []  # type: List[TBlock]

    def add_block(self, ablock: TBlock):
        self.block.append(ablock)

    def pop_children(self, hv: Hashval) -> Optional[List[TBlock]]:
        temp_block = []
        for i in self.block:
            if i.pbhv == hv:
                temp_block.append(i)
                self.block.remove(i)
        if not temp_block:
            return None
        return temp_block

    def find(self, hashval: Hashval) -> Optional[List[TBlock]]:
        temp_block = []
        for i in self.block:
            if i.hashval == hashval:
                temp_block.append(i)
        if not temp_block:
            return None
        return temp_block


def check_tx(tx: Tx):
    return True if tx is not None else False


def check_solution(tblock: TBlock):
    spid = '%s' % tblock.pid
    st = '%s' % tblock.timestamp
    sha256 = hashlib.sha256()
    k = spid + st
    sha256.update(k.encode('utf-8'))
    v = sha256.hexdigest()
    if v < D_p:
        return True
    else:
        return False