from typing import *
from dcsim.framework import *


class AdversaryController(AdversaryControllerBase):
    def round_instruction(self,
                          corrupted_nodes: Type[NodeBase],
                          pending_messages: List[MessageTuple]) -> Dict[NodeId, Any]:
        raise NotImplementedError
