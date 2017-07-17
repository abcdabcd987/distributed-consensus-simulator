import abc
from typing import *

from .NodeId import NodeId


class AuthenticationServiceBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_keys(self, node_ids: Tuple[NodeId, ...]):
        """
        generate keys for node ids
        :param node_ids: tuple of node id
        """
        pass
    
    @abc.abstractmethod
    def get_key(self, node_id) -> Any:
        """
        get a key of one node
        :param node_id: the id of given node
        :return: public key for Public Key Algorithm, otherwise the secret key
        """
        pass
    
    @abc.abstractmethod
    def get_secret_key(self, node_id) -> Any:
        """
        get the secret key of one node
        :param node_id: node id
        :return: secret key of the node, if this authentication service
            is based on **public key algorithm**, it should raise 'NotImplementedError'
        """
        pass
    
    @abc.abstractmethod
    def get_public_key(self, node_id) -> Any:
        """
        get the public key of one node
        :param node_id: node id
        :return: public key of the node, if this authentication service
            is based on **secret key algorithm**, it should raise 'NotImplementedError'
        """
        pass
    
    @abc.abstractmethod
    def sign(self, sender: NodeId, message: bytes) -> str:
        """
        generate a signature for a pair of <sender, message>
        :param sender: node id of sender
        :param message: message to sign
        :return: signature in string
        """
        pass
    
    @abc.abstractmethod
    def verify(self, signature: str, sender: NodeId, message: bytes) -> bool:
        """
        verify if a given signature matches the given pair <sender, message>
        :param signature: signature in string which should be in correct format
        :param sender: node id of sender
        :param message: message from sender
        :return: True if matched, or False
        """
        pass
