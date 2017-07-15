import hashlib
from typing import *
from dcsim.framework import *
from .common import *
from .CorruptedNode import CorruptedNode
if TYPE_CHECKING:
    from .Configuration import Configuration


class BlockTree():
    def __init__(self, key) -> None:
        self._depth = 0
        self._blockPool = {SuperRoot.hashval: SuperRoot}

    @property
    def depth(self) -> int:
        return self._depth

    def insert(self, cur: Block):
        if cur.hashval in self._blockPool.keys():
            return
        tmp = cur
        seq = []
        while tmp.hashval != SuperRoot.hashval:
            seq.append(tmp)
            #print("AdversaryController - BlockTree.insert: searching %s %s" % (tmp.hashval, tmp.pbhv))
            tmp = self._blockPool.get(tmp.pbhv, None)
            if tmp is None:
                break
        if tmp is None:
            self._blockPool[cur.hashval] = cur
        else:
            self._blockPool[cur.hashval] = cur
            for node in seq:
                if node not in tmp.children:
                    tmp.children.append(node)
                tmp = node
            self._depth = max(self._depth, len(seq))


def valid(block: Block, timestamp: int):
    return check_sol(block.id, block.round) and block.round <= timestamp


class AdversaryController(AdversaryControllerBase):
    def __init__(self, corrupted_nodes: Tuple['CorruptedNode', ...], config: 'Configuration') -> None:
        super().__init__(corrupted_nodes, config)
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()

    def update(self, ctx: Context):
        for message_tuple in ctx._received_messages:
            message = message_tuple.message
            sender = message_tuple.sender
            if message["type"] == 0:
                if verify_tx(ctx, message, sender):
                    self._tx.insert(message["value"])
            elif message["type"] == 1:
                if verify_block(ctx, message, sender):
                    self._root.insert(message["value"])

    def action(self, ctx: Context):
        for badNode in self._corrupted_nodes:
            if check_sol(badNode.id, ctx._round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                block = Block(self._chain[-1].hashval, self._tx.get_all(), cast(Timestamp, ctx._round), badNode.id)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) - 2 > self._root._depth + self._config.confirm_time:
                    cast(CorruptedNode, badNode).add_send(self._chain)
                    self._chain = [SuperRoot]
                    print("Corrupt chain pushed")
        print("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))

    def round_instruction(self, ctx: Context):
        self.update(ctx)
        self.action(ctx)
