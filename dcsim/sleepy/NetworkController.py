from typing import *
from dcsim.framework import *


class NetworkController(NetworkControllerBase):
    def __init__(self, config: Type['ConfigurationBase']):
        super().__init__(config)

    def round_filter(self,
                     messages_to_send: List[MessageTuple],
                     round: int) -> List[bool]:
        return [round - t.round == self._config.max_delay for t in messages_to_send]
