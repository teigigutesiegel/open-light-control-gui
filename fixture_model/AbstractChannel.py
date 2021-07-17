from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Fixture import Fixture


class AbstractChannel():
    '''Base class for channels.'''
    _key: str
    _pixelKey: str

    def __init__(self, key: str) -> None:
        self._key = key
        self._pixelKey = None

    def __str__(self) -> str:
        return f"Channel <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_fixture(self) -> 'Fixture':
        raise TypeError(
            f"Class {self.__class__.__name__} must implement property fixture")

    def _get_key(self) -> str:
        return self._key

    def _get_name(self) -> str:
        return self._key

    def _get_uniqueName(self) -> str:
        return self.fixture.uniqueChannelNames[self.key]

    def _get_pixelKey(self) -> str:
        return self._pixelKey

    def set_pixelKey(self, key: str) -> None:
        self._pixelKey = key

    key: str = property(_get_key)
    name: str = property(_get_name)
    fixture: 'Fixture' = property(_get_fixture)
    uniqueName: str = property(_get_uniqueName)
    pixelKey: str = property(_get_pixelKey, set_pixelKey)
