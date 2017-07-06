from typing import *
if TYPE_CHECKING:
    from .Coordinator import Coordinator
    from .MessageTuple import MessageTuple
    from .NodeId import NodeId


class Context:
    def __init__(self,
                 round: int,
                 coordinator: 'Coordinator',
                 received_messages: List[Any],
                 adversary_instruction: Any) -> None:
        raise NotImplementedError

    def send(self, receiver: 'NodeId', message: Any) -> None:
        raise NotImplementedError

    def broadcast(self, message: Any) -> None:
        raise NotImplementedError

    @property
    def received_messages(self) -> List[Any]:
        raise NotImplementedError

    @property
    def messages_to_send(self) -> List['MessageTuple']:
        raise NotImplementedError

    @property
    def instruction(self) -> Any:
        raise NotImplementedError
