from typing import *
from dcsim.framework import *
from .common import *


class HonestNode(NodeBase):
    def __init__(self, config: ConfigurationBase) -> None:
        super().__init__(config)
        self._nodeId = self._id
        self._txpool = TransactionPool()
        self._orphanpool = OrphanBlockPool()
        self._block_chain = BlockChain()

    @property
    def main_chain(self):
        return self._block_chain.main_chain

    # remove all the children of block from the orphan pool
    def recursive_remove_block_from_orphan_pool(self, block: Block):
        blocks_to_remove = self._orphanpool.pop_children(block.hashval)
        if blocks_to_remove is None:
            return
        else:
            for b2r in blocks_to_remove:
                self.recursive_remove_block_from_orphan_pool(b2r)

    # add all the orphan that could be connected on to the chain
    def recursive_add_block_from_orphan_pool(self, curnode: BlockNode):
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
        message_tuples = ctx.received_messages
        blocks: List[Block] = []       # store valid blocks

        for message_tuple in message_tuples:
            message = message_tuple.message
            sender = message_tuple.sender
            if message["type"] == 0:   # its a transaction
                if ctx.verify(message["signature"], message["value"], sender) \
                        and check_tx(message["value"]):
                    if not self._txpool.contain_key(message["value"]):
                        my_sig = ctx.sign(message["value"])
                        ctx.broadcast({"type": 0, "valuTNe": message["value"], "signature": my_sig})
                        self._txpool.insert(message["value"])
                    else:
                        continue
                else:
                    continue
            elif message["type"] == 1:   # its a block
                print("HonestNode.round_action: NodeId", self._nodeId, "dealing with", message["value"].hashval)
                if ctx.verify(message["signature"], message["value"].serialize, sender) \
                        and check_solution(message["value"])\
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

            my_sig = ctx.sign(block.serialize)
            ctx.broadcast({"type": 1, "value": block, "signature": my_sig})
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

        pbhv = self._block_chain.get_top().block.hashval
        txs = self._txpool.get_all()
        t = ctx._round
        my_block: Block = Block(pbhv, txs, cast(Timestamp, t), self._nodeId)
        if check_solution(my_block):
            self._block_chain.add_child(self._block_chain.get_top(), my_block)
            my_sig = ctx.sign(my_block.serialize)
            ctx.broadcast({"type": 1, "value": my_block, "signature": my_sig})
            self._txpool.clear()
        return None
