from typing import *
from dcsim.framework import *
from .common import *

class CorruptedNode(NodeBase):
    def set_round0_senders(self, sender_id: Tuple['NodeId', ...]) -> None:
        pass

    def round_action(self, ctx: 'Context') -> None:
        for msg in self._broadcast_msg:
 ##           print(self._round)
 ##           print(self.msg)
            ctx.broadcast(Message(value = msg, nodeId = self.id, signature = ctx.sign(msg.serialize)))
        for rev, msg in self._send_msg:
            print(self._round)
            print(msg, " ", self.id, " ", rev)
            ctx.send(rev, Message(value = msg, nodeId = self.id, signature = ctx.sign(msg.serialize)))

        self._broadcast_msg = []
        self._send_msg = []
        self._round += 1
    def round0_sender_action(self, ctx: 'Context') -> None:
        self._round = 0
        self.round_action(ctx)
        self._round = 1

    def __init__(self, config: ConfigurationBase) -> None:
        super().__init__(config)
        self._round = 1
        self._broadcast_msg = []
        self._send_msg = []
    def add_broadcast(self, msg):
        self._broadcast_msg.append(msg)

    def add_send(self,receiver, msg):
        self._send_msg.append((receiver, msg))

