from typing import *
from dcsim.framework import *


class HonestNode(NodeBase):
    @property
    def id(self) -> NodeId:
        raise NotImplementedError

    def round_action(self, ctx: Context) -> None:
        raise NotImplementedError
