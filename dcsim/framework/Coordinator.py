from typing import *
import hashlib
import os
import struct
if TYPE_CHECKING:
    from .NodeBase import NodeBase
    from .NodeId import NodeId
    from .ConfigurationBase import ConfigurationBase


class Coordinator:
    def __init__(self, configuration: Type['ConfigurationBase']) -> None:
        self.config = configuration
        self.m_nodes = []
        self.keys_of_nodes = {}

    def add_node(self, node: NodeBase) -> None:
        self.m_nodes.append(node)
        random_key = os.urandom(4)
        self.keys_of_nodes[node.id] = random_key

    def sign(self, message: str, sender: NodeId) -> str:
        """
        sign by SHA1 hash with a id number.
        :param message: string to sign
        :param sender: NodeId of the sender
        :return: signature of <message, sender> in str
        """
        m = hashlib.sha1()
        m.update(message.encode())
        m.update('#'.encode())
        m.update(self.keys_of_nodes[sender])
        return m.hexdigest()
        
    def verify(self, signature: str, message: str, sender: NodeId) -> bool:
        """
        verify a given signature is true
        :param signature: signature which should be produced by self.sign above.
        :param message: string to verify
        :param sender: NodeId of the sender
        :return: True for a correct signature and False otherwise
        """
        real_signature = self.sign(message=message, sender=sender)
        return signature == real_signature

    @property
    def nodes(self) -> List[NodeBase]:
        return self.m_nodes

    @property
    def configuration(self) -> Type['ConfigurationBase']:
        return self.config
