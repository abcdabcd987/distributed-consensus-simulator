import os
import hashlib
from dcsim.framework import *
from typing import *


class FSign(TrustedThirdPartyBase):
    def __init__(self, name):
        super().__init__(name)
        self._secret_keys = {}

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
        if caller not in self._secret_keys:
            self._secret_keys[caller] = FSign._generate_secret_key()

    def _sign(self, message: bytes, sender_id: NodeId) -> str:
        """
        returns the footprint (signature) of message signed by a given sender node.
        :param message: the messages to be signed
        :param sender_id: the id of the sender node
        :return: the footprint (signature) of message signed by a given sender node.
        """
        m = hashlib.sha1()
        m.update(self._secret_keys[sender_id])
        m.update(message)
        return m.hexdigest()

    def sign(self, caller: NodeId, message: bytes) -> str:
        return self._sign(message, caller)

    def verify(self, caller: NodeId, signature: str, message: bytes, sender_id: NodeId) -> bool:
        return self._sign(message, sender_id) == signature
