from typing import *
if TYPE_CHECKING:
    from .NodeBase import NodeBase
    from .ConfigurationBase import ConfigurationBase


class Coordinator:
    def __init__(self, configuration: Type['ConfigurationBase']) -> None:
        self.config = configuration
        raise NotImplementedError

    def add_node(self, node: Type['NodeBase']) -> None:
        raise NotImplementedError

    @property
    def nodes(self) -> List[Type['NodeBase']]:
        raise NotImplementedError

    @property
    def configuration(self) -> Type['ConfigurationBase']:
        return self.config
