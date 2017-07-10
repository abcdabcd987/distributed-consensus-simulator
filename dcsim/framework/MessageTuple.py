from typing import *
if TYPE_CHECKING:
    from .NodeId import NodeId


class MessageTuple(NamedTuple):
    sender: NodeId
    receiver: NodeId
    round: int
    message: Any
