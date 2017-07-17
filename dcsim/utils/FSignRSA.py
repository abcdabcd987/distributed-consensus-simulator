import os
import random
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from dcsim.framework import *
from typing import *


class FSignRSA(TrustedThirdPartyBase):
    """
    a authentication service based on RSA public key algorithm

    each node has a key pair, private key for sign and public key for verify

    The performance is much worse than hash-based authentication service.
    It is a example to illustrate how to use AuthenticationServiceBase to
      implement a public key algorithm based authentication serivce.
    """

    _public_exponents = [3, 5, 17, 257, 65537]

    def __init__(self, name):
        super().__init__(name)
        self._private_keys = {}

    @property
    def _callable_functions(self) -> List[Callable]:
        return [self.register,
                self.sign,
                self.verify,]

    def round_action(self, round: int) -> None:
        pass

    @staticmethod
    def _generate_secret_key():
        return os.urandom(16)

    def register(self, caller: NodeId) -> None:
        if caller not in self._private_keys:
            self._private_keys[caller] = rsa.generate_private_key(
                public_exponent=random.choice(FSignRSA._public_exponents),
                key_size=2048,
                backend=default_backend()
            )

    def sign(self, caller: NodeId, message: bytes) -> str:
        signature = self._private_keys[caller].sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature)

    def verify(self, caller: NodeId, signature: str, message: bytes, sender_id: NodeId) -> bool:
        public_key = self._private_keys[sender_id].public_key()
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
            return True
        except InvalidSignature:
            return False
