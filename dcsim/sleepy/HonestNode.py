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
        @ property
        * hashval(self) -> Hashval (string)
            hashval is encrypted with SHA256 whose parameters are txs, timestamp and pid.
        @property
        * str(self) -> str
            change block to str
            make sure to use it only when you are calling ctx.sign

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

    * TransactionPool class
        Store transactions that will be added into block
        * contain_key(self, tx) -> bool : placeholder
            check if a specific transaction is already in it
        * insert(self, tx)
            add a transaction into pool
        * erase(self, tx) : placeholder
            remove a specific transaction
        * clear(self) :
            pop out all transaction

    * OrphanBlockPool class
        Store blocks whose parent block is not in the chain currently
        * add_block(self)
        * find(self, Hashval) -> bool
        * pop_children(self, hv) -> List['TBlock'] :
            find nodes with specified pbhv, if no match, return None

    * check_solution(block : Block class) -> bool
        Check if H(pid, t) < D_p
    * check_tx(tx : Tx) -> bool
        placeholder, simply return True now
        Check if transaction is valid
    * sign_message(message, priv_key) -> signedMessage : placeholder
        use priv_key to sign message
"""

import hashlib
# import rsa
import random
from typing import *
from dcsim.framework import *

D_p = "0fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"  # 这个值暂时定为这么多，后面会改

Tx = str
Hashval = str
Timestamp = int
NodeId = int

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


class TBlock:

    def __init__(self, pbhv: Hashval, txs: List[Type['Tx']], timestamp: int, pid: int) -> object:
        # comes from TransactionPool
        self.txs = txs  # type: List[Tx]
        # father's hash
        self.pbhv = pbhv  # type: Hashval
        self.timestamp = timestamp  # type: Timestamp
        self.pid = pid  # type: NodeId
        self.children = []

    @property
    def id(self) -> int:
        return self.pid
    
    @property
    def round(self) -> int:
        return self.timestamp

    @property
    def hashval(self) -> Hashval:  # get its own hash
        hashstr = self.str
        return hashlib.sha256(hashstr.encode("utf-8")).hexdigest()

    @property
    def str(self) -> str:   # get its string
        return self.pbhv + "".join(self.txs) + str(self.timestamp) + str(self.pid)

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


SuperRoot = TBlock("0", [], 0, 0)


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


class OrphanBlockPool:

    def __init__(self):
        self.block = []

    def add_block(self, ablock):
        self.block.append(ablock)

    def pop_children(self, hv) -> Optional[List['TBlock']]:
        temp_block = []
        for i in self.block:
            if i.pbhv == hv:
                temp_block.append(i)
                self.block.remove(i)
        if not temp_block:
            return None
        return temp_block

    def find(self, hashval: Hashval) -> Optional[List['TBlock']]:
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

Message = Any


class HonestNode(NodeBase):

    def __init__(self):
        random.seed()
        self._nodeId = random.randint(1, 2**32)
        self._txpool = TransactionPool()
        self._orphanpool = OrphanBlockPool()
        self._block_chain = BlockChain()

    @property
    def id(self) -> NodeId:
        return self._nodeId

    @property
    def main_chain(self):
        return self._block_chain.main_chain

    # remove all the children of block from the orphan pool
    def recursive_remove_block_from_orphan_pool(self, block: TBlock):
        blocks_to_remove = self._orphanpool.pop_children(block.hashval)
        if blocks_to_remove is None:
            return
        else:
            for b2r in blocks_to_remove:
                self.recursive_remove_block_from_orphan_pool(b2r)

    # add all the orphan that could be connected on to the chain
    def recursive_add_block_from_orphan_pool(self, curnode: TNode):
        blocks_to_add = self._orphanpool.pop_children(curnode.block.hashval)
        if blocks_to_add is None:
            return
        else:
            for b2a in blocks_to_add:
                # timestamp check failed
                if curnode.block.timestamp >= b2a.timestamp:
                    self.recursive_remove_block_from_orphan_pool(b2a)
                else:
                    new_node = self._block_chain.add_child(curnode, b2a)
                    self.recursive_add_block_from_orphan_pool(new_node)

    def update(self, ctx):
        # check received blocks
        message_tuples: List[MessageTuple] = ctx.received_messages
        self.blocks: List[TBlock] = []       # store valid blocks
        self.message_tuples: List[MessageTuple] = []

        for message_tuple in message_tuples:
            message = message_tuple.message
            sender = message_tuple.sender
            if message["type"] == 0:   # its a transaction
                if ctx.verify(message["signature"], message["value"], sender) \
                        and check_tx(message["value"]):
                    if not self._txpool.contain_key(message["value"]):
                        self.message_tuples.append(message_tuple)
                        self._txpool.insert(message["value"])
                    else:
                        continue
                else:
                    continue
            elif message["type"] == 1:   # its a block
                print("HonestNode.round_action: NodeId %d dealing with " % self._nodeId + message["value"].hashval)
                if ctx.verify(message["signature"], message["value"].str, sender) \
                        and check_solution(message["value"])\
                        and message["value"].timestamp <= ctx.round:
                    print("HonestNode.round_action: NodeId %d accepted message " % self._nodeId + message["value"].hashval)
                    self.blocks.append(message["value"])
                else:
                    continue

        for block in self.blocks:
            # check if this block has been received
            if self._block_chain.find(block.hashval) is not None:
                continue
            elif self._orphanpool.find(block.hashval):
                continue

            cur_node = self._block_chain.find(block.pbhv)
            if cur_node is None:
                self._orphanpool.add_block(block)
            # timestamp check failed
            elif cur_node.block.timestamp >= block.timestamp:
                self.recursive_remove_block_from_orphan_pool(block)
            else:
                if cur_node == self._block_chain.get_top():
                    for tx in block.txs:
                        self._txpool.erase(tx)
                new_node = self._block_chain.add_child(cur_node, block)
                self.recursive_add_block_from_orphan_pool(new_node)
    
    def action(self, ctx):
        for message in self.message_tuples:
            my_sig = ctx.sign(message["value"], self.id)
            ctx.broadcast({"type": 0, "value": message["value"], "signature": my_sig})
        for block in self.blocks:
            my_sig = ctx.sign(block.str, self.id)
            ctx.broadcast({"type": 1, "value": block, "signature": my_sig})
        pbhv = self._block_chain.get_top().block.hashval
        txs = self._txpool.get_all()
        t = ctx.round
        my_block: TBlock = TBlock(pbhv, txs, t, self._nodeId)
        if check_solution(my_block):
            self._block_chain.add_child(self._block_chain.get_top(), my_block)
            my_sig = ctx.sign(my_block.str, self.id)
            ctx.broadcast({"type": 1, "value": my_block, "signature": my_sig})
            self._txpool.clear()

    def round_action(self, ctx: Context) -> None:
        self.update(ctx)
        self.action(ctx)
        return None
