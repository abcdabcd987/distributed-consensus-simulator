from typing import *
from dcsim.framework import *
import random


class CorruptedNode(NodeBase):
    def __init__(self):
        random.seed()
        self._id = random.randint(1, 1 << 32)
        self._cache = []

    @property
    def id(self) -> NodeId:
        return self._id

    def add_send(self, blocks):
        self._cache = blocks

    def round_action(self, ctx: Context) -> None:
        while len(self._cache) > 0:
            ctx.broadcast({"type": 1, "value": self._cache.pop()})
