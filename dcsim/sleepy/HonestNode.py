"""
    Sleepy Consensus Algorithms
    * Block class
        * pbhv : Hashval (string)
            the hash value of previous block (generated by hashlib)
        * txs  : Tx list (string list) 
            recorded transactions (input)
        * timestamp  : Timestamp (int)
            timestamp, indicating its t-th round
        * pid  : NodeId (int)
            node's identifier
        * get_data(self) -> List[Tx]
            get txs stored in the block
        @ property
        * hashval(self) -> Hashval (string)
            hashval is encrypted with SHA256 whose parameters are txs, timestamp and pid.
    * TNode class
        we use tree to keep tract of main chain and alternative chains,
        TNode class represent node of the tree
        * block : Block
        * hash : Hashval (string)
            the hash value of block in this node
            (store it so as to make searching blocks easier)
        * depth : int
            the depth from this node to root
            (namely, the height of this block)
        * father : Optional('TNode')
            the father node of this TNode
            only genesis' father can be None
        * index : List[int]
            array pointer to the children[]
            index[i] is the index of children, for example, you can say children[index[i]]
        * children : List[TNode]
            this TNode's children list
        * num : int
            index[i] = num
        * get_children(self) -> List[TNode]
            returns this TNode's children list
        * get_child_index(self, child_node: 'TNode') -> int
            return i, children[index[i]] == child_node
        * add_child(self, new_node: 'TNode') -> bool
            add a new_node to children
        * transfer_chain(self, i: int, j: int)
            transfer to child chains
        * search(self, p_hash: str) -> Optional['TNode']
            search for a child whose hash equals to p_hash
    * BlockChain class
        * __init__(self) -> None
            Remember to add genesis block as the root of the tree
            Gensis block consist of:
                pbhv = "0", txs = [], timestamp = 0, nid = 0
                self.genesis = TNode(0, TBlock("0", [], 0, 0), None)    # type: TNode
        * find(self, hash_val) -> TNode
            find the node that contain a block with specified hash value
        * add_child(self, t_node, block) -> TNode
            Create a new node with block inside and make it the t_node's child,
            and then return this node.
            This method will automatically check the depth of newly inserted node
            and update the main chain if needed
        * get_top(self) -> TNode
            Get the top block in main chain
        @ property
        * main_chain(self) -> List[block]
            extract the main chain and form a list where every block just follows its father in the list
    * check_solution(block : Block class) -> bool
        Check if H(pid, t) < D_p
    * check_tx(tx : Tx) -> bool
        placeholder, simply return True now
        Check if transaction is valid
    * TxPool class
        Store transactions that will be added into block
        * find_tx(self, tx) -> bool : placeholder
            check if a specific transaction is already in it
        * add_tx(self, tx) -> bool
            add a transaction into pool if
        * remove_tx(self, tx) : placeholder
            remove a specific transaction
        * pop_one(self) : placeholder
            pop the transaction with highest priority
        * pop_all(self) :
            pop out all transaction
    * OrphanBlockPool class
        Store blocks whose parent block is not in the chain currently
        * add_block(self)
        * find(self, Hashval) -> bool
        * pop_child(self, hv) -> block :
            find the node with specified pbhv, if no match, return none
    * sign_message(message, priv_key) -> signedMessage : placeholder
        use priv_key to sign message
"""

import hashlib
import string
# import rsa
import random
from typing import *
from dcsim.framework import *

D_p = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"  # 这个值暂时定为这么多，后面会改

Tx = str
Hashval = str
Timestamp = int
NodeId = int


# tx pool 存收到但没有放进去的交易信息
class TxPool:

    def __init__(self):
        self.txs = []

    def add_tx(self, txs) -> Tx:
        self.txs.append(txs)
        return txs

    def remove_tx(self, txs) -> bool:
        for item in self.txs:
            if txs == item:
                self.txs.remove(txs)
                return True
        return False

    def find_tx(self, txs) -> Optional['Tx']:
        for item in self.txs:
            if txs == item:
                return txs
        return None

    def get_all(self):  # get data
        return self.txs

    def clear_all(self):
        del self.txs[:]


class TBlock:

    def __init__(self, pbhv, txs, timestamp, pid):
        # comes from TxPool
        self.txs = txs  # type: List[Tx]
        # father's hash
        self.pbhv = pbhv  # type: Hashval
        self.timestamp = timestamp  # type: Timestamp
        self.pid = pid  # type: NodeId

    def get_data(self) -> List[Tx]:
        return self.txs

    @property
    def hashval(self) -> Hashval:  # get its own hash
        hashstr = "".join(self.txs) + str(self.timestamp) + str(self.pid)
        return hashlib.sha256(hashstr.encode("utf-8")).hexdigest()


class TNode:

    def __init__(self, depth, block, father):  # father's(block's) hash
        self.depth = depth  # type: int
        self.block = block  # type: TBlock
        # own hash
        self.hash = block.hashval  # type: str
        self.father = father  # type: Optional['TNode']

        self.index = []  # type: List[int]
        self.children = []  # type: List[TNode]
        self.num = 0  # type: int

        if father == None:
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

    def search(self, p_hash: str) -> Optional['TNode']:
        res = None  # type: Union[TNode, None]
        for child in self.children:
            if child.hash == p_hash:
                return child
            else:
                res = child.search(p_hash)
                if res is not None:
                    break
        return res


class BlockChain:

    def __init__(self) -> None:
        # pbhv = "0", txs = [], timestamp = 0, nid = 0
        self.genesis = TNode(0, TBlock("0", [], 0, 0), None)    # type: TNode
        self.head = self.genesis    # type: TNode
        self.tail = self.genesis    # type: TNode

    def find(self, hash_val: str) -> Optional['TNode']:
        if self.head.hash == hash_val:
            return self.head
        else:
            return self.head.search(hash_val)

    def add_child(self, t_node: 'TNode', block: 'TBlock'):
        new_node = TNode(t_node.depth+1, block, t_node)
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


# TODO: add function find(Hashval) -> bool
class OrphanBlockPool:

    def __init__(self):
        self.block = []

    def add_block(self, ablock):
        self.block.append(ablock)

    def pop_child(self, hv) -> Optional[List['TBlock']]:
        temp_block = []
        for i in self.block:
            if i.pbhv == hv:
                temp_block.append(i)
                self.block.remove(i)
        if temp_block == []:
            return None
        return temp_block

    def find(self, hashval) -> Optional[List['TBlock']]:
        temp_block = []
        for i in self.block:
            if i.hashval == hashval:
                temp_block.append(i)
        if temp_block == []:
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

Message = Any
SignedMessage = Message


def sign_message(message: Message, priv_key) -> SignedMessage:
    return message if priv_key is not None else message


class HonestNode(NodeBase):

    def __init__(self, coorindator):
        # coordinator provides the "permissioned" services
        self._coorindator = coorindator
        # codes to generate rsa key pair, not used yet
        # (self.pub_key, self.priv_key) = rsa.newkeys(512)

        random.seed()
        self._nodeId = random.randint(1, 2**32)
        self._txpool = TxPool()
        self._orphanpool = OrphanBlockPool()
        self._block_chain = BlockChain()

    @property
    def id(self) -> NodeId:
        return self._nodeId

    @property
    def main_chain(self):
        return self._block_chain.main_chain

    def round_action(self, ctx: Context) -> None:
        # check received blocks
        messages: List[Any] = ctx.received_messages
        txs: List[Tx] = []              # store valid txs
        blocks: List[TBlock] = []       # store valid blocks

        # TODO: assume txs could come from the network (not just from input)
        # TODO: deal with them and broadcast txs that haven't been received
        # TODO: this would also require txs that are already in block chain to be removed from txpool
        for message in messages:
            if message["type"] == 0:   # its a transaction
                if check_tx(message["value"]):
                    txs.append(message["value"])
            elif message["type"] == 1:   # its a block
                if not check_solution(message["value"]):
                    continue
                elif message["value"].timestamp >= ctx.round:
                    continue
                else:
                    blocks.append(message["value"])

        for block in blocks:
            # check if this block has been received
            if self._block_chain.find(block.hashval) is not None:
                continue
            elif self._orphanpool.find(block.hashval):
                continue

            ctx.broadcast({"type": 1, "value": block})
            cur_node = self._block_chain.find(block.pbhv)
            child_block = block
            if cur_node is None:
                self._orphanpool.add_block(block)
            else:
                while cur_node is not None:
                    # timestamp is invalid (bigger than father's)
                    if cur_node.block.timestamp >= child_block.timestamp:
                        continue
                    else:   # timestamp check pass
                        cur_node = self._block_chain.add_child(cur_node, child_block)
                        child_block = self._orphanpool.pop_child(child_block.hashval)

        pbhv = self._block_chain.get_top().block.hashval
        txs = self._txpool.get_all()
        t = ctx.round
        my_block: TBlock = TBlock(pbhv, txs, t, self._nodeId)
        if check_solution(my_block):
            self._block_chain.add_child(self._block_chain.get_top(), my_block)
            ctx.broadcast({"type": 1, "value": my_block})
            self._txpool.clear_all()
        return None