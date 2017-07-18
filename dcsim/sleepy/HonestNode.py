from typing import *
from dcsim.framework import *
from .utils import *
import logging
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

    def set_trusted_third_party(self, trusted_third_party: 'TrustedThirdPartyCaller'):
        super(HonestNode, self).set_trusted_third_party(trusted_third_party)
        self._trusted_third_party.call('FSign', 'register')

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
        recursively remove the subtree(the root has already been removed) of the given block from the orphan pool

        :param block: the root of the subtree needed to be removed
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
        recursively add the subtree(root has already been added and removed) of curnode to blockchain, and remove them from orphan pool

        :param curnode: the root of the subtree needed to be added from the orphan pool
        :return: void
        """
        blocks_to_add = self._orphanpool.pop_children(curnode.block.hashval)
        if blocks_to_add is None:
            return
        else:
            for b2a in blocks_to_add:
                # timestamp of root check failed
                # the whole subtree is invalid and can't be added to blockchain
                if curnode.block.timestamp >= b2a.timestamp:
                    self.recursive_remove_block_from_orphan_pool(b2a)
                else:
                    new_node = self._block_chain.add_child(curnode, b2a)
                    self.recursive_add_block_from_orphan_pool(new_node)

    def round_action(self, ctx: Context) -> None:
        """
        the round action of the honest node

        :param ctx: use the ctx to do inputs and outputs for a node
        :return: none
        """

        # check received blocks
        message_tuples = ctx.received_messages
        blocks: List[TBlock] = []       # store received blocks

        for message_tuple in message_tuples:
            message = message_tuple.message
            sender = message_tuple.sender
            if message["type"] == 0:   # its a transaction
                verified = self._trusted_third_party.call('FSign', 'verify',
                                                          signature=message['signature'],
                                                          message=message['value'],
                                                          sender_id=sender)
                if verified and check_tx(message["value"]):
                    #received a tx not in the txpool, forward the tx with its onw sig and store tx in txpool
                    if not self._txpool.find_tx(message["value"]):
                        my_sig = self._trusted_third_party.call('FSign', 'sign', message=message["value"])
                        ctx.broadcast({"type": 0, "value": message["value"], "signature": my_sig})
                        self._txpool.add_tx(message["value"])
                    else:
                        continue
                else:
                    continue
            elif message["type"] == 1:   # its a block
                logging.debug("HonestNode.round_action: NodeId", self._nodeId, "dealing with", message["value"])
                verified = self._trusted_third_party.call('FSign', 'verify',
                                                          signature=message['signature'],
                                                          message=message['value'].serialize,
                                                          sender_id=sender)
                if verified \
                        and check_solution(message["value"], self._probability)\
                        and message["value"].timestamp <= ctx.round:
                    logging.debug("HonestNode.round_action: NodeId", self._nodeId, "accepted message", message["value"].hashval)

                    blocks.append(message["value"])
                else:
                    continue

        # print("Main chain for node %d" % self._nodeId)
        # print(self.main_chain)
        # print("- - - - - - ")

        for block in blocks:
            # check if this block has been received
            if self._block_chain.find(block.hashval) is not None:
                continue
            elif self._orphanpool.find(block.hashval):
                continue

            #cur_node : father of block
            cur_node = self._block_chain.find(block.pbhv)
            if cur_node is None:
                self._orphanpool.add_block(block)
            # timestamp check failed, no need to forward
            elif cur_node.block.timestamp >= block.timestamp:
                self.recursive_remove_block_from_orphan_pool(block)
                continue
            else:
                #block added to the tail of mainchain
                if cur_node == self._block_chain.get_top():
                    for tx in block.txs:
                        self._txpool.remove_tx(tx)
                new_node = self._block_chain.add_child(cur_node, block)
                self.recursive_add_block_from_orphan_pool(new_node)
            #forward valid block
            my_sig = self._trusted_third_party.call('FSign', 'sign', message=block.serialize)
            ctx.broadcast({"type": 1, "value": block, "signature": my_sig})

        #mine new block
        pbhv = self._block_chain.get_top().block.hashval
        txs = self._txpool.get_all()
        t = ctx._round
        my_block: TBlock = TBlock(pbhv, txs, cast(Timestamp, t), self._nodeId)
        if check_solution(my_block, self._probability):
            logging.debug("HonestNode.round_action: NodeId", self._nodeId, "chosen as the leader")
            self._block_chain.add_child(self._block_chain.get_top(), my_block)
            my_sig = self._trusted_third_party.call('FSign', 'sign', message=my_block.serialize)
            ctx.broadcast({"type": 1, "value": my_block, "signature": my_sig})
            self._txpool.clear_all()
        return None
