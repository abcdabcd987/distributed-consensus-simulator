import abc
from typing import *
if TYPE_CHECKING:
    from .NodeId import NodeId


class TrustedThirdPartyBase(metaclass=abc.ABCMeta):
    def __init__(self, name: str) -> None:
        self._name = name
        self.__func = {f.__name__: f for f in self._callable_functions}

    @property
    def name(self) -> str:
        return self._name

    @abc.abstractmethod
    def round_action(self, round: int) -> None:
        pass

    @property
    @abc.abstractmethod
    def _callable_functions(self) -> List[Callable]:
        pass

    @no_type_check
    def call(self, caller: 'NodeId', function_name: str, args, kwargs):
        func = self.__func[function_name]
        return func(caller, *args, **kwargs)
