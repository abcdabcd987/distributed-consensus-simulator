import abc
from .NodeBase import NodeBase
from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .MessageTuple import MessageTuple
    from .TrustedThirdPartyCaller import TrustedThirdPartyCaller


class AdversaryControllerBase(metaclass=abc.ABCMeta):
    def __init__(self, config: 'ConfigurationBase') -> None:
        """
        Initalize the Adversary Controller, set the config, get the list of all corrupted nodes

        :param config: Configuration of the protocol
        """
        self._config = config
        self._corrupted_nodes = [NodeBase.generate_node_id() for _ in range(config.num_corrupted_nodes)]
        self._trusted_third_parties = {}  # type: Dict[NodeId, TrustedThirdPartyCaller]

    @property
    def corrupted_node_list(self) -> List['NodeId']:
        return self._corrupted_nodes

    def set_honest_node_list(self, node_ids: Tuple['NodeId', ...]) -> None:
        self._honest_nodes = node_ids

    def set_trusted_third_party(self, node_id: 'NodeId', trusted_third_party: 'TrustedThirdPartyCaller'):
        self._trusted_third_parties[node_id] = trusted_third_party

    @abc.abstractmethod
    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        """
        get all delivered messages in designated round

        :param round: the round that these messages are in
        """
        pass

    @abc.abstractmethod
    def round_action(self, round: int) -> None:
        """
        the action of adversary controller in designated round

        """
        pass

    @abc.abstractmethod
    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        """
        add messages(messages_to_send) sent from node(sender_id) in designated (round) to adversary controller

        :param round: the round that the messages are in
        :param sender_id: the id of the sender
        :param messages_to_send: A list that contains the new messages
        """
        pass
