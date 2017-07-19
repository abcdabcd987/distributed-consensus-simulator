from dcsim.framework.AdversaryControllerBase import AdversaryControllerBase
from dcsim.framework.MessageTuple import MessageTuple
from collections import defaultdict
from typing import *
from typing import TYPE_CHECKING, List, cast, Tuple


class DummyAttack(AdversaryControllerBase):
    def __init__(self, config: 'Configuration') -> None:
        super(DummyAttack, self).__init__(config)
        self._pending_messages = []

    def round_action(self, round: int) -> None:
        for corrupted_node in self._corrupted_nodes:
            for honest_node in self._honest_nodes:
                t = MessageTuple(sender=corrupted_node,
                                 receiver=honest_node,
                                 round=round,
                                 message=1)
                self._pending_messages.append(t)

    def add_honest_node_messages(self, round: int, sender_id: 'NodeId', messages_to_send: List['MessageTuple']) -> None:
        self._pending_messages += messages_to_send

    def get_delivered_messages(self, round: int) -> List['MessageTuple']:
        m = self._pending_messages
        self._pending_messages = []
        return m