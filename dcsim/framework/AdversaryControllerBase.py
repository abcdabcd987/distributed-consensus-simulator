import abc
from typing import *
if TYPE_CHECKING:
    from .RunnerBase import RunnerBase
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .MessageTuple import MessageTuple


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, corrupted_nodes: Tuple['NodeBase', ...], config: 'RunnerBase') -> None:
        """
        Initalize the Adversary Controller, set the config and the number of the corrupted nodes,
        :param corrupted_nodes: A tuple contains the corrupted nodes
        :param config: Configuration of the protocol
        """
        self._corrupted_nodes = corrupted_nodes
        self._config = config

    @abc.abstractmethod
    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        """
        Get the delivered messages from all the nodes, returns a list contains all the messagetuples
        :param round: the round that these messages are in
        """
        pass

    @abc.abstractmethod
    def give_instruction(self, round: int) -> None:
        """
        adversary controller gives the instructions to the nodes
        :param round: the round that these instructions are in
        """
        pass

    @abc.abstractmethod
    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        """
        add new messages from the honest nodes
        :param round: the round that the messages are in
        :param sender_id: the id of the sender
        :param messages_to_send: A list that contains the new messages
        """
        pass

    @abc.abstractmethod
    def add_corrupted_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        """
        add new messages from the corrupted nodes
        :param round: the round that the messages are in
        :param sender_id: the id of the sender
        :param messages_to_send: A list that contains the new messages
        """
        pass
