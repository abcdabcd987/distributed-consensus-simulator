import hashlib
import pickle
from typing import *
from typing import Optional, List, NewType, cast

from dcsim.framework import *

Tx = NewType('Tx', bytes)
Hashval = NewType('Hashval', bytes)
Timestamp = NewType('Timestamp', int)



class TxPool:
    '''
    store all received txs
    at the end of each round, all txs in the txpool form a new block, and clear it
    '''

    def __init__(self) -> None:
        """
        initialize the transaction pool
        """
        self.txs = []  # type: List[Tx]

    def add_tx(self, tx: Tx):
        """
        add a trasaction to the pool

        :param tx: the inserted transaction
        """
        self.txs.append(tx)

    def remove_tx(self, tx) -> bool:
        """
        remove a given transaction

        :param tx: the transaction to be removed
        :return: whether the removement is success or not
        """
        for item in self.txs:
            if tx == item:
                self.txs.remove(tx)
                return True
        return False

    def find_tx(self, tx) -> Optional[Tx]:
        """
        find a transaction in the pool

        :param tx: the given transaction
        :return: the found transation or none if not found
        """
        for item in self.txs:
            if tx == item:
                return tx
        return None

    def get_all(self):  # get data
        """
        get all the transactions

        :return: all the transactions
        """
        return self.txs

    def clear_all(self):
        """
        delete all the transactions
        """
        del self.txs[:]


class TBlock:
    def __init__(self, pbhv: Hashval, txs: List[Tx], timestamp: Timestamp, pid: NodeId) -> None:
        # comes from TxPool
        """
        Initialize the block of the transactions

        :param pbhv: the hash of the previous block
        :param txs: the transactions contained in this block
        :param timestamp: the timestap of this block
        :param pid: the sender id of this block
        """
        self.txs = txs
        self.pbhv = pbhv
        self.timestamp = timestamp
        self.pid = pid
        self.children = []  # type: List[TBlock]

    @property
    def id(self) -> int:
        """
        return the pid of the block

        :return: the pid of the block
        """
        return self.pid

    @property
    def round(self) -> int:
        """
        return the timestamp of this block

        :return: the timestamp of this block
        """
        return self.timestamp

    @property
    def hashval(self) -> Hashval:
        """
        the hash value of this block

        :return:
        """
        return cast(Hashval, hashlib.sha256(self.serialize).hexdigest())

    @property
    def serialize(self) -> bytes:
        """
        get pickle of the informations in this block

        :return: the pickle of all the informations in this block
        """
        return pickle.dumps((self.pbhv, self.txs, self.timestamp, self.pid))

    def __repr__(self):
        return repr((self.txs, self.hashval, self.pbhv, self.timestamp, self.pid, self.children))

class TNode:
    #Wrap TBlock with its previous block and blockchain's depth
    def __init__(self, depth, block, father):  # father's(block's) hash
        """
        Initialize the TNode

        :param depth: the depth of the this TNode
        :param block: corresponding TBlock
        :param father: previous TNode
        """
        self.depth = depth  # type: int
        self.block = block  # type: TBlock
        # own hash
        self.hash = block.hashval  # type: Hashval
        self.father = father  # type: Optional['TNode']

        self.index = []  # type: List[int]
        self.children = []  # type: List[TNode]
        #num of children
        self.num = 0  # type: int

        #previous block hash value
        if father is None:
            self.block.pbhv = "0"
        else:
            self.block.pbhv = father.hash

    def get_children(self):
        """
        get the children of this TNode

        :return: the chlldren of this TNode
        """
        return self.children

    def get_child_index(self, child_node: 'TNode') -> int:
        """
        return the index of the child_node

        :param child_node:
        :return: the index of child_node
        """
        for i in range(len(self.index)):
            if child_node.hash == self.children[self.index[i]].hash:
                return i
        return -1

    def add_child(self, new_node: 'TNode') -> bool:
        # if full, discard new_node
        # max is 16
        """
        all the children to this node

        :param new_node: the children node to be added
        :return: whether the addition succeed
        """
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
        """
        swap the order of two children

        :param i: one node to be swap
        :param j: another node to be swap
        """
        x = self.index[i]
        self.index[i] = self.index[j]
        self.index[j] = x

    def search(self, p_hash: Hashval) -> Optional['TNode']:
        """
        find a node in its subtree with hashval p_hash

        :param p_hash: the hash of the TNode to be searched
        :return: the TNode found
        """
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
    #actually it's a blocktree
    def __init__(self) -> None:
        # pbhv = "0", txs = [], timestamp = 0, nid = 0
        """
        initialize the blockchain
        """
        self.genesis = TNode(0, SuperRoot, None)    # type: TNode
        #head of mainchain
        self.head = self.genesis    # type: TNode
        #tail of mainchain
        self.tail = self.genesis    # type: TNode

    def find(self, hash_val: Hashval) -> Optional['TNode']:
        """
        find a TNode whose hash equal to hash_val

        :param hash_val: the hash value given
        :return: a TNode with given hash_val
        """
        if self.head.hash == hash_val:
            return self.head
        else:
            return self.head.search(hash_val)

    def add_child(self, t_node: 'TNode', block: 'TBlock'):
        """
        add a child to after the given TNode

        :param t_node: the node who want the this child
        :param block: the child to be added
        :return: the new TNode
        """
        new_node = TNode(t_node.depth + 1, block, t_node)
        t_node.add_child(new_node)
        #change of mainchain
        #TNode of mainchian is index[0] child of its previous TNode
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
        """
        return TBlocks of mainchain

        :return: TBlocks of mainchain
        """
        temp_list = []              # type: List[TBlock]
        temp_node = self.genesis    # type: TNode
        while temp_node != self.tail:
            temp_list.append(temp_node.block)
            i = temp_node.index[0]
            temp_node = temp_node.children[i]
        temp_list.append(self.tail.block)
        return temp_list

    def get_top(self) -> TNode:
        #get last TNode of mainchain
        return self.tail


class OrphanBlockPool:
    '''
    store the blocks that has been received but wait for the receipt of its previous block
    '''

    def __init__(self) -> None:
        """
        initialize the orphan block pool
        """
        self.block = []  # type: List[TBlock]

    def add_block(self, ablock: TBlock):
        """
        add a block to orphan pool

        :param ablock: block to be added
        """
        self.block.append(ablock)

    def pop_children(self, hv: Hashval) -> Optional[List[TBlock]]:
        """
        remove the blocks whose father's hashval is hv from orphan pool

        :param hv: the given hash value
        :return: the removed blocks
        """
        temp_block = []
        for i in self.block:
            if i.pbhv == hv:
                temp_block.append(i)
                self.block.remove(i)
        if not temp_block:
            return None
        return temp_block

    def find(self, hashval: Hashval) -> Optional[List[TBlock]]:
        """
        find the child whose hashvalue equal to the given hashvalue

        :param hashval: the given hash value
        :return: the children whose hashvalue equal to the given hashvalue
        """
        temp_block = []
        for i in self.block:
            if i.hashval == hashval:
                temp_block.append(i)
        if not temp_block:
            return None
        return temp_block


def check_tx(tx: Tx):
    """
    check whether the transaction is none

    :param tx: the given transaction
    :return: whether the transaction is none
    """
    return True if tx is not None else False


def check_solution(tblock: TBlock, probability):
    """
    check whether the tblock is the leader

    :param tblock: the block to be checked
    :return: whether the block satisfies the restriction
    """
    spid = '%s' % tblock.pid
    st = '%s' % tblock.timestamp
    sha256 = hashlib.sha256()
    k = spid + st
    sha256.update(k.encode('utf-8'))
    v = float(int(sha256.hexdigest(), 16))
    d_p = 2.0**256 * probability
    return v < d_p
