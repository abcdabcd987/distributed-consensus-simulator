from typing import *
from dcsim.framework import *


class Measurement(MeasurementBase):
    def should_stop(self) -> bool:
        raise NotImplementedError

    def __init__(self,
                 corrupted_nodes: List[Type[NodeBase]],
                 honest_nodes: List[Type[NodeBase]],
                 network: Type[NetworkControllerBase],
                 adv: Type[AdversaryControllerBase]) -> None:
        raise NotImplementedError

    def report(self) -> None:
        raise NotImplementedError
