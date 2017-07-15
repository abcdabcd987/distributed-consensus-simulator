import hashlib
import random
from dcsim.framework import *
from .HonestNode import *
from typing import *
if TYPE_CHECKING:
    from .CorruptedNode import CorruptedNode


def check(id:int, timestamp:int):
    sha = hashlib.sha256()
    sha.update(("%d%d"% (id, timestamp)).encode("utf-8"))
    return sha.hexdigest() < D_p

def valid(block: Block, timestamp: int):
    return check(block.id, block.round) and block.round <= timestamp

class AdversaryController(AdversaryControllerBase):
    def __init__(self):
        self._root = BlockTree(SuperRoot)
        self._chain = [SuperRoot]
        self._tx = TransactionPool()

    def round_instruction(self,
                          corrupted_nodes: List['CorruptedNode'],
                          pending_messages: List['MessageTuple'],
                          current_round: int,
                          confirm_time: int) -> Dict['NodeId', Any]:
        #print('AdversaryController.round_instruction')
        #print('Pending messages:')
        #print(pending_messages)
        #print("SuperRoot hash: %s" % SuperRoot.hashval)
        for message in pending_messages:
            message = message.message
            #print(message["type"], message["value"])
            if message["type"] == 0:
                if not self._tx.contain_key(message["value"]):
                    self._tx.insert(message["value"])
            else:
                #print("Dealing with ", message["value"].id, message["value"].round, message["value"].hashval, message["value"].pbhv)
                if valid(message["value"], current_round):
                    self._root.insert(message["value"])

        ret = {}
        for badNode in corrupted_nodes:
            if check(badNode.id, current_round):
                print('AdversaryController.round_instruction: NodeId', badNode.id, 'chosen as the leader')
                block = Block(self._chain[-1].hashval, self._tx.get_all(), current_round, badNode.id)
                self._tx.clear()
                self._chain.append(block)
                if len(self._chain) - 2 > self._root._depth + confirm_time:
                    badNode.add_send(self._chain)
                    self._chain = [SuperRoot]
                    print("Corrupt chain pushed")
                ret[badNode.id] = None
        print("Current honest length %d, corrupt chain length %d" % (self._root.depth, len(self._chain) - 1))
        return ret