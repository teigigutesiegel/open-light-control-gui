from typing import Optional
from numbers import Number

from .Address import Address
from OpenLightControlGui.fixture_model.Fixture import Fixture
from OpenLightControlGui.fixture_model.Capability import Capability

class Lamp():
    _address: Optional[Address]
    _fixture: Fixture
    _num: Number

    def __init__(self, num: Number, fixture: Fixture, address: Optional[Address] = None) -> None:
        self._num = num
        self._fixture = fixture
        self._address = address
    
    def get_num(self) -> Number:
        return self._num
    
    def get_fixture(self) -> Fixture:
        return self._fixture
    
    def get_capabilities(self) -> 'list[Capability]':
        return self.fixture.capabilities

    def get_address(self) -> Address:
        return self._address
    
    def set_address(self, address: Address) -> None:
        self._address = address
    
    def get_hasAddress(self) -> bool:
        return bool(getattr(self, "address", None))
    
    number: Number = property(get_num)
    fixture: Fixture = property(get_fixture)
    capabilities: 'list[Capability]' = property(get_capabilities)
    address: Address = property(get_address, set_address)
    hasAddress: bool = property(get_hasAddress)

    def __eq__(self, o: 'Lamp') -> bool:
        return isinstance(o, Lamp) and self.address == o.address and self.fixture == o.fixture

    def __str__(self) -> str:
        if self.hasAddress:
            return f"{self.number}-{self.fixture.name} at {self.address}"
        else:
            return f"{self.number}-{self.fixture.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()
