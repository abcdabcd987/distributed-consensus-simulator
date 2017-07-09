from typing import *
from dcsim.framework import *


class NetworkController(NetworkControllerBase):
    def round_filter(self, messages_to_send: List[MessageTuple], current_round: int) -> List[bool]:
        pass
