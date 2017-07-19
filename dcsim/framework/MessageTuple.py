from typing import *
from typing import TYPE_CHECKING, NamedTuple, Any

if TYPE_CHECKING:
    from .NodeId import NodeId


class MessageTuple(NamedTuple):
    """
    send message from sender to receiver in designated round

    """
    sender: 'NodeId'
    receiver: 'NodeId'
    round: int
    message: Any
