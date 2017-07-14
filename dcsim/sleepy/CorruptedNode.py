from typing import *
from dcsim.framework import *


class CorruptedNode(NodeBase):
    def __init__(self, config: Type['ConfigurationBase']):
        super().__init__(config)
        self._cache = []

    def add_send(self, blocks):
        self._cache = blocks

    def round_action(self, ctx: Context) -> None:
        while len(self._cache) > 0:
            message = self._cache.pop()
            ctx.broadcast({"type": 1, "value": message, "signature": ctx.sign(message.str)})
