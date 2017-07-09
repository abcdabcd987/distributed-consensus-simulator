from typing import *
if TYPE_CHECKING:
    from .NodeBase import NodeBase
    from .ConfigurationBase import ConfigurationBase


class Coordinator:
    def __init__(self, configuration: Type['ConfigurationBase']) -> None:
        self.config = configuration
        self.m_nodes = []

    def add_node(self, node: NodeBase) -> None:
        self.m_nodes.append(node)

    @property
    def nodes(self) -> List[NodeBase]:
        return self.m_nodes

    @property
    def configuration(self) -> Type['ConfigurationBase']:
        return self.config