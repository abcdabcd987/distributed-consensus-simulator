import hashlib
from typing import *
import os
from dcsim.framework.AuthenticationServiceBase import AuthenticationServiceBase
from dcsim.framework.NodeId import NodeId


class HashBasedAuthenticationService(AuthenticationServiceBase):
    """
    A authentication service based on hash with secret keys
    
    each node has one secret key and the signature is generated by
        signature = SHA256(node's secret key || message)
    where || is concatenation operator of bytes
    """
    def __init__(self):
        self._secret_keys = {}
    
    def generate_keys(self, node_ids: Tuple[NodeId, ...]):
        for node_id in node_ids:
            self._secret_keys[node_id] = os.urandom(16)
    
    def get_key(self, node_id) -> Any:
        return self.get_secret_key(node_id)
    
    def get_secret_key(self, node_id) -> Any:
        return self._secret_keys[node_id]
    
    def get_public_key(self, node_id) -> Any:
        raise NotImplementedError("hash based authentication does not have public key.")
    
    def sign(self, sender: NodeId, message: bytes) -> str:
        m = hashlib.sha1()
        m.update(self._secret_keys[sender])
        m.update(message)
        return m.hexdigest()
    
    def verify(self, signature: str, sender: NodeId, message: bytes) -> bool:
        return self.sign(sender, message) == signature

