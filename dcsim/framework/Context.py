from typing import *

from .Coordinator import Coordinator
from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase


class Context:
    def __init__(self,
                 round: int,
                 node: Type['NodeBase'],
                 coordinator: 'Coordinator',
                 received_messages: List[MessageTuple]) -> None:
        self._round = round
        self._node = node
        self._coordinator = coordinator
        self._received_messages = received_messages
        self._message_tuples_to_send = []

    def send(self, receiver: NodeId, message: Any) -> None:
        sender = self._node.id
        message_tuple = MessageTuple(sender=sender, receiver=receiver, round=self._round, message=message)
        self._message_tuples_to_send.append(message_tuple)

    def broadcast(self, message: Any) -> None:
        for receiver_node in self._coordinator.nodes:
            self.send(receiver_node.id, message)

    @property
    def received_messages(self) -> List['MessageTuple']:
        return self._received_messages

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        return self._message_tuples_to_send

    def sign(self, message: str, sender: NodeId) -> str:
        return self._coordinator.sign(message, sender)

    def verify(self, signature: str, message: str, sender: NodeId) -> bool:
        return self._coordinator.verify(signature, message, sender)
