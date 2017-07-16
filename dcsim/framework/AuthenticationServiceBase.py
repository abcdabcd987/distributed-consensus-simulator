import abc
from typing import *
if TYPE_CHECKING:
    from .NodeId import NodeId


class AuthenticationServiceBase(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def generate_keys(self, node_ids: Tuple[NodeId, ...]):
        pass
    
    @abc.abstractmethod
    def get_key(self, node_id) -> Any:
        pass

    @abc.abstractmethod
    def get_secret_key(self, node_id) -> Any:
        pass

    @abc.abstractmethod
    def get_public_key(self, node_id) -> Any:
        pass

    @abc.abstractmethod
    def sign(self, sender: NodeId, message: bytes) -> str:
        pass

    @abc.abstractmethod
    def verify(self, signature: str, sender: NodeId, message: bytes) -> bool:
        pass
