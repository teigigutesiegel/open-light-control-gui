from .AbstractChannel import AbstractChannel

from typing import Union, TYPE_CHECKING, Any
from numbers import Number

if TYPE_CHECKING:
    from .Fixture import Fixture
    from .CoarseChannel import CoarseChannel


class Resolution(int):
    pass


RESOLUTION_8BIT: Resolution = Resolution(1)
RESOLUTION_16BIT: Resolution = Resolution(2)
RESOLUTION_24BIT: Resolution = Resolution(3)
RESOLUTION_32BIT: Resolution = Resolution(4)

class FineChannel(AbstractChannel):
    '''
    Represents a finer channel of a 16+ bit channel.
    Also called LSB (least significant byte) channel.
    '''
    _coarseChannel: 'CoarseChannel'
    _cache: 'dict[str, Any]'

    def __init__(self, key: str, coarseChannel: 'CoarseChannel') -> None:
        super().__init__(key)
        self.coarseChannel = coarseChannel

    def _get_coarseChannel(self) -> 'CoarseChannel':
        return self._coarseChannel

    def set_coarseChannel(self, coarseChannel: 'CoarseChannel') -> None:
        self._coarseChannel = coarseChannel
        self._cache = {}

    def _get_coarserChannel(self) -> 'Union[FineChannel, CoarseChannel]':
        if self.resolution == RESOLUTION_16BIT:
            return self.coarseChannel
        else:
            return self.coarseChannel.fineChannels[self.resolution - 3]

    def _get_name(self) -> str:
        if self.resolution > RESOLUTION_16BIT:
            a = self.resolution - 1
        else:
            a = ""
        return f"{self.coarseChannel.name} fine{a}"

    def _get_fixture(self) -> 'Fixture':
        return self.coarseChannel.fixture

    def _get_resolution(self) -> Resolution:
        return self.coarseChannel.fineChannelAliases.index(self.key) + 2

    def _get_defaultValue(self) -> Number:
        return self.coarseChannel.getDefaultValueWithResolution(self.resolution) % 256

    coarseChannel: 'CoarseChannel' = property(
        _get_coarseChannel, set_coarseChannel)
    coarserChannel: 'Union[FineChannel, CoarseChannel]' = property(
        _get_coarserChannel)
    name: str = property(_get_name)
    fixture: 'Fixture' = property(_get_fixture)
    resolution: Resolution = property(_get_resolution)
    defaultValue: Number = property(_get_defaultValue)
