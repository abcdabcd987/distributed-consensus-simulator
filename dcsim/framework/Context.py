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

    @property
    def received_messages(self) -> Tuple['MessageTuple', ...]:
        return self._received_messages

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        return self._message_tuples_to_send

    def _sign(self, message: bytes, sender_id: NodeId) -> str:
        m = hashlib.sha1()
        m.update(self._secret_keys[sender_id])
        m.update(message)
        return m.hexdigest()

    def sign(self, message: bytes) -> str:
        return self._sign(message, self._node.id)

    def verify(self, signature: str, message: bytes, sender_id: NodeId) -> bool:
        return self._sign(message, sender_id) == signature
