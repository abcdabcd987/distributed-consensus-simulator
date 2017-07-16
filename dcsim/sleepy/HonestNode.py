from ctypes import cast
from typing import *
from dcsim.framework import *
from .utils import *
if TYPE_CHECKING:
    from dcsim.sleepy.Configuration import Configuration


class HonestNode(NodeBase):
    def __init__(self, config: 'Configuration') -> None:
        """
        Initilize the hoestnode
        :param config: the configuration of the node
        """
        super().__init__(config)
        self._nodeId = self._id
        self._txpool = TxPool()
        self._orphanpool = OrphanBlockPool()
        self._block_chain = BlockChain()
        self._probability = config.probability

    @property
    def main_chain(self):
        """
        return the blockchain's mainchain
        :return: the blockchain's mainchain
        """
        return self._block_chain.main_chain

    # remove all the children of block from the orphan pool
    def recursive_remove_block_from_orphan_pool(self, block: TBlock):
        """
        remove the given block from the orphan pool
        :param block: the block to be removed
        :return: void
        """
        blocks_to_remove = self._orphanpool.pop_children(block.hashval)
        if blocks_to_remove is None:
            return
        else:
            for b2r in blocks_to_remove:
                self.recursive_remove_block_from_orphan_pool(b2r)

    # add all the orphan that could be connected on to the chain
    def recursive_add_block_from_orphan_pool(self, curnode: TNode):
        """
        all the given block to the orphan pool
        :param curnode: the node to be added
        :return: void
        """
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

    def round_action(self, ctx: Context) -> None:
        # check received blocks
        """
        the round action of the honest node
        :param ctx: use the ctx to do inputs and outputs in a node
        :return: none
        """
        message_tuples = ctx.received_messages
        blocks: List[TBlock] = []       # store valid blocks

        for message_tuple in message_tuples:
            message = message_tuple.message
            sender = message_tuple.sender
            if message["type"] == 0:   # its a transaction
                if ctx.verify(message["signature"], message["value"], sender) \
                        and check_tx(message["value"]):
                    if not self._txpool.find_tx(message["value"]):
                        my_sig = ctx.sign(message["value"])
                        ctx.broadcast({"type": 0, "value": message["value"], "signature": my_sig})
                        self._txpool.add_tx(message["value"])
                    else:
                        continue
                else:
                    continue
            elif message["type"] == 1:   # its a block
                print("HonestNode.round_action: NodeId", self._nodeId, "dealing with", message["value"].hashval, "from ", message["value"].pid)
                if ctx.verify(message["signature"], message["value"].serialize, sender) \
                        and check_solution(message["value"], self._probability)\
                        and message["value"].timestamp <= ctx._round:
                    print("HonestNode.round_action: NodeId", self._nodeId, "accepted message", message["value"].hashval)
                    blocks.append(message["value"])
                else:
                    continue

        for block in blocks:
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
                continue
            else:
                if cur_node == self._block_chain.get_top():
                    for tx in block.txs:
                        self._txpool.remove_tx(tx)
                new_node = self._block_chain.add_child(cur_node, block)
                self.recursive_add_block_from_orphan_pool(new_node)
            my_sig = ctx.sign(block.serialize)
            ctx.broadcast({"type": 1, "value": block, "signature": my_sig})


        pbhv = self._block_chain.get_top().block.hashval
        txs = self._txpool.get_all()
        t = ctx._round
        my_block: TBlock = TBlock(pbhv, txs, cast(Timestamp, t), self._nodeId)
        if check_solution(my_block, self._probability):
            self._block_chain.add_child(self._block_chain.get_top(), my_block)
            my_sig = ctx.sign(my_block.serialize)
            ctx.broadcast({"type": 1, "value": my_block, "signature": my_sig})
            self._txpool.clear_all()
        return None
