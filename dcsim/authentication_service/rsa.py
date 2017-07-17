import hashlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from random import choice
from typing import *
import os
from dcsim.framework.AuthenticationServiceBase import AuthenticationServiceBase
from dcsim.framework.NodeId import NodeId

public_exponents = [3, 5, 17, 257, 65537]


class RsaBasedAuthenticationService(AuthenticationServiceBase):
    """
    a authentication service based on RSA public key algorithm
    
    each node has a key pair, private key for sign and public key for verify
    
    The performance is much worse than hash-based authentication service.
    It is a example to illustrate how to use AuthenticationServiceBase to
      implement a public key algorithm based authentication serivce.
    """
    def __init__(self):
        self._private_keys = {}
    
    def generate_keys(self, node_ids: Tuple[NodeId, ...]):
        for node_id in node_ids:
            self._private_keys[node_id] = rsa.generate_private_key(
                public_exponent=choice(public_exponents),
                key_size=2048,
                backend=default_backend()
            )
    
    def get_key(self, node_id) -> Any:
        return self.get_public_key(node_id)
    
    def get_secret_key(self, node_id) -> Any:
        raise NotImplementedError("RSA-based authentication does not have secret key.")
    
    def get_public_key(self, node_id) -> Any:
        return self._private_keys[node_id].public_key()
    
    def sign(self, sender: NodeId, message: bytes) -> str:
        signature = self._private_keys[sender].sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature)
    
    def verify(self, signature: str, sender: NodeId, message: bytes) -> bool:
        public_key = self._private_keys[sender].public_key()
        try:
            public_key.verify(
                base64.b64decode(signature),
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            return False
        return True


