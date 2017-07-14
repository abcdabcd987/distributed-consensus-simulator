import hashlib
from typing import *

from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase


class Context:
    def __init__(self,
                 nodes: Iterable[NodeId],
                 secret_keys: Dict[NodeId, bytes],
                 round: int,
                 node: Type['NodeBase'],
                 received_messages: List[MessageTuple]) -> None:
        self._nodes = nodes
        self._secret_keys = secret_keys
        self._round = round
        self._node = node
        self._received_messages = received_messages
        self._message_tuples_to_send = []

    def send(self, receiver: NodeId, message: Any) -> None:
        sender = self._node.id
        message_tuple = MessageTuple(sender=sender, receiver=receiver, round=self._round, message=message)
        self._message_tuples_to_send.append(message_tuple)

    def broadcast(self, message: Any) -> None:
        for node_id in self._nodes:
            self.send(node_id, message)

    @property
    def received_messages(self) -> List['MessageTuple']:
        return self._received_messages

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        return self._message_tuples_to_send

    def _sign(self, message: str, sender_id: NodeId) -> str:
        m = hashlib.sha1()
        m.update(self._secret_keys[sender_id])
        m.update(message.encode('utf-8'))
        return m.hexdigest()

    def sign(self, message: str) -> str:
        return self._sign(message, self._node.id)

    def verify(self, signature: str, message: str, sender_id: NodeId) -> bool:
        return self._sign(message, sender_id) == signature
