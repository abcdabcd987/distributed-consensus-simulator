"""
    Sleepy Consensus Algorithms
    * Block class
        * pbhv : the hash value of previous block
        * txs  : recorded transactions (input)
        * t    : timestamp
        * pid  : player's identifier 
        * function GetHash(self)
    * TNode class 
        we use tree to keep tract of main chain and alternative chains,
        TNode class represent node of the tree
        * block
        * hash_val : the hash value of block in this node
            (store it so as to make searching blocks easier)
        * depth : the depth from this node to root
            (namely, the height of this block)
        * and something to organize this structure
    * BlockChain class
        implemented as a tree
    * CheckSolution(block) : Check if H(pid, t) < D_p
    * CheckTx(tx) : placeholder, simply return True now
        Check if transaction is valid
    * TxPool class
        Store transactions that will be added into block
        * AddTx(self, tx) : add a transaction into pool
        * RemoveTx(self, tx) : remove a specific transaction
        * FindTx(self, tx) : check if a specifix transaction is already in it
        * PopOne(self) : placeholder
            pop the transaction with highest priority
        * PopAll(self) : pop out all transaction
    * OrphanBlockPool class
        Store blocks whose parent block is not in the chain currently
        * AddBlock(self)
        * PopChild(self, hash_val) : 
            find the node with specified pbhv, if no match, return none
"""

from typing import *
from dcsim.framework import *

class HonestNode(NodeBase):
    @property
    def id(self) -> NodeId:
        raise NotImplementedError

    def round_action(self, ctx: Context) -> None:
        raise NotImplementedError
