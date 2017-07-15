from typing import *
from dcsim.framework import *
if TYPE_CHECKING:
    from .common import TBlock


class CorruptedNode(NodeBase):
    def __init__(self, config: ConfigurationBase) -> None:
        """
        intitialze the CorruptedNode, including the configuration
        :param config: the configuration of the node
        """
        super().__init__(config)
        self._cache = []  # type: List['TBlock']

    def add_send(self, blocks: List['TBlock']):
        """
        cache the given blocks
        :param blocks: A list contians all the blocks
        """
        self._cache = blocks

    def round_action(self, ctx: Context) -> None:
        """
        the round action of the corrupted node
        :param ctx:
        """
        while len(self._cache) > 0:
            message = self._cache.pop()
            ctx.broadcast({"type": 1, "value": message, "signature": ctx.sign(message.serialize)})
