from typing import *

from .MessageTuple import MessageTuple
from .NodeId import NodeId
from .NodeBase import NodeBase


class Context:
    def __init__(self,
                 nodes: Tuple[NodeId, ...],
                 round: int,
                 node: NodeBase,
                 received_messages: Tuple[MessageTuple, ...]) -> None:
        """
        initialize the Context class
        :param nodes: the nodes that will be broadcast to
        :param round: the round that the context is in
        :param node: the node of the sender
        :param received_messages: having the shape of [(sender_id, receiver_id, round, message)] contains all messages that this node received in this round.
        """
        self._nodes = nodes
        self._round = round
        self._node = node
        self._received_messages = received_messages
        self._message_tuples_to_send = []  # type: List[MessageTuple]

    @property
    def round(self):
        return self._round

    def send(self, receiver: NodeId, message: Any) -> None:
        """
        sends a message to a given node
        :param receiver: the ndoe that receives the message
        :param message: the messags that to be sent
        """
        sender = self._node.id  # type: NodeId
        message_tuple = MessageTuple(sender=sender, receiver=receiver, round=self._round, message=message)
        self._message_tuples_to_send.append(message_tuple)

    def broadcast(self, message: Any) -> None:
        """
        broadcasts a message to all nodes
        :param message: the message to be broadcast
        """
        for node_id in self._nodes:
            self.send(node_id, message)

    @property
    def received_messages(self) -> Tuple['MessageTuple', ...]:
        """
        reture the received messages
        :return: a tuple contains all the received messages
        """
        return self._received_messages

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        """
        return the messages to be sent
        :return: A list contains all the messages to be sent
        """
        return self._message_tuples_to_send
