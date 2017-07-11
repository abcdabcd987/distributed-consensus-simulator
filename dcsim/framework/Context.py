from typing import *

from .Coordinator import Coordinator
from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase


class Context:
    def __init__(self,
                 round: int,
                 node: NodeBase,
                 coordinator: 'Coordinator',
                 received_messages: List[MessageTuple],
                 adversary_instruction: Any) -> None:
        self.round = round
        self.node = node
        self.coordinator = coordinator
        self.received_messages = [
            message_tuple
            for message_tuple in received_messages
            if message_tuple.receiver == node.id
        ]
        self.instruction = adversary_instruction
        self.message_tuples_to_send = []

    def send(self, receiver: NodeId, message: Any) -> None:
        sender = self.node.id
        message_tuple = MessageTuple(sender=sender, receiver=receiver, round=self.round, message=message)
        self.message_tuples_to_send.append(message_tuple)

    def broadcast(self, message: Any) -> None:
        for receiver_node in self.coordinator.nodes:
            receiver_id = receiver_node.id
            self.send(receiver_id, message)

    # @property
    def get_received_messages(self) -> List['MessageTuple']:
        return self.received_messages

    # @property
    def get_messages_to_send(self) -> List['MessageTuple']:
        return self.message_tuples_to_send

    # @property
    def get_instruction(self) -> Any:
        return self.instruction

    def sign(self, message: str, sender: NodeId) -> str:
        return self.coordinator.sign(message, sender)

    def verify(self, signature: str, message: str, sender: NodeId) -> bool:
        return self.coordinator.verify(signature, message, sender)
