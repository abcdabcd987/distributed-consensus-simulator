from typing import *
if TYPE_CHECKING:
    from .ConfigurationBase import ConfigurationBase


class Simulator:
    def __init__(self, config: Type['ConfigurationBase']) -> None:
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
