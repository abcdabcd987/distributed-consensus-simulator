from typing import *
if TYPE_CHECKING:
    from .NodeId import NodeId
    from .TrustedThirdPartyBase import TrustedThirdPartyBase


class TrustedThirdPartyCaller:
    def __init__(self, trusted_third_parties: List['TrustedThirdPartyBase'], node_id: 'NodeId'):
        self._trusted_third_parties = {t.name: t for t in trusted_third_parties}
        self._node = node_id

    def call(self, party_name: str, function_name: str, *args, **kwargs) -> Any:
        ttp = self._trusted_third_parties[party_name]
        return ttp.call(self._node, function_name, args, kwargs)

