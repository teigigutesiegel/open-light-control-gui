from typing import Optional, Iterable, Union
from numbers import Number

from OpenLightControlGui.model.Address import Address
from OpenLightControlGui.fixture_model.Fixture import Fixture
from OpenLightControlGui.fixture_model.Mode import Mode
from OpenLightControlGui.fixture_model.AbstractChannel import AbstractChannel

class Lamp():
    _address: 'list[Address]'
    _mode: Mode
    _num: Number

    def __init__(self, num: Number, mode: Mode, address: Optional[Union[Address, Iterable[Address]]] = None) -> None:
        self._num = num
        self._mode = mode
        if address:
            if not isinstance(address, Iterable):
                self._address = [address]
            else:
                self._address = [a for a in address]
        else:
            self._address = []
    
    def _get_num(self) -> Number:
        return self._num
    
    def _set_num(self, num = Number):
        self._num = num
    
    def _get_mode(self) -> Mode:
        return self._mode
    
    def _get_fixture(self) -> Fixture:
        return self.mode.fixture
    
    def _get_channels(self) -> 'list[AbstractChannel]':
        return self.mode.channels

    def _get_address(self) -> 'list[Address]':
        return self._address
    
    def _set_address(self, address: Iterable[Address]) -> None:
        self._address = [a for a in address]
    
    def add_address(self, address: Address) -> None:
        self._address.append(address)
    
    def _get_hasAddress(self) -> bool:
        return len(self._address) > 0
    
    number: Number = property(_get_num, _set_num)
    mode: Mode = property(_get_mode)
    fixture: Fixture = property(_get_fixture)
    channels: 'list[AbstractChannel]' = property(_get_channels)
    address: 'list[Address]' = property(_get_address, _set_address)
    hasAddress: bool = property(_get_hasAddress)

    def __eq__(self, o: 'Lamp') -> bool:
        return isinstance(o, Lamp) and self.address == o.address and self.mode == o.mode

    def __str__(self) -> str:
        return f"{self.number}-{self.fixture.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()
