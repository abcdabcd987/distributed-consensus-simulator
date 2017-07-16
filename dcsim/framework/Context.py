import hashlib
from typing import *

from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase
from .AuthenticationServiceBase import AuthenticationServiceBase


class Context:
    def __init__(self,
                 authentication_service: AuthenticationServiceBase,
                 nodes: Tuple[NodeId, ...],
                 round: int,
                 node: NodeBase,
                 received_messages: Tuple[MessageTuple, ...]) -> None:
        self._nodes = nodes
        self._authentication_service = authentication_service
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

    def sign(self, message: bytes) -> str:
        return self._authentication_service.sign(sender=self._node.id, message=message)

    def verify(self, signature: str, message: bytes, sender_id: NodeId) -> bool:
        return self._authentication_service.verify(signature=signature, sender=sender_id, message=message)
