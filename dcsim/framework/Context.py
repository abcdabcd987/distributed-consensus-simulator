import hashlib
from typing import *

from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase


class Context:
    def __init__(self,
                 nodes: Tuple[NodeId, ...],
                 secret_keys: Dict[NodeId, bytes],
                 round: int,
                 node: NodeBase,
                 received_messages: Tuple[MessageTuple, ...]) -> None:
        self._nodes = nodes
        self._secret_keys = secret_keys
        self._round = round
        self._node = node
        self._received_messages = received_messages
        self._message_tuples_to_send = []  # type: List[MessageTuple]

    def send(self, receiver: NodeId, message: Any) -> None:
        sender = self._node.id  # type: NodeId
        message_tuple = MessageTuple(sender=sender, receiver=receiver, round=self._round, message=message)
        self._message_tuples_to_send.append(message_tuple)

    def broadcast(self, message: Any) -> None:
        for node_id in self._nodes:
            self.send(node_id, message)

    def get_secret_key(self):
        return self._secret_keys[self._node.id]

    def get_public_key(self, node_id: NodeId):
        return self._secret_keys[node_id]

    @property
    def received_messages(self) -> Tuple['MessageTuple', ...]:
        return self._received_messages

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        return self._message_tuples_to_send
