from typing import *
from dcsim.framework import *


class NetworkController(NetworkControllerBase):
    def round_filter(self, messages_to_send: List[MessageTuple]) -> List[bool]:
        raise NotImplementedError
