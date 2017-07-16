import hashlib
from typing import *
import os
import base64
from dcsim.framework.AuthenticationServiceBase import AuthenticationServiceBase

if TYPE_CHECKING:
    from dcsim.framework.NodeId import NodeId


class NoAuthenticationService(AuthenticationServiceBase):
    def __init__(self):
        pass
    
    def generate_keys(self, node_ids: Tuple[NodeId, ...]):
        pass
        
    def get_key(self, node_id) -> Any:
        return None
    
    def get_secret_key(self, node_id) -> Any:
        return None
    
    def get_public_key(self, node_id) -> Any:
        return None
    
    def sign(self, sender: NodeId, message: bytes) -> str:
        return base64.b64encode(os.urandom(32))
    
    def verify(self, signature: str, sender: NodeId, message: bytes) -> bool:
        return True

