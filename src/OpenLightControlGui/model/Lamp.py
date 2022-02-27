from typing import Any, Dict, List, Literal, Optional, Iterable, Type, Union
from numbers import Number
from OpenLightControlGui.fixture_model.Capability import Capability

from OpenLightControlGui.model.Address import Address
from OpenLightControlGui.fixture_model import Fixture, Mode, AbstractChannel, CoarseChannel

_cap_types = Literal["Intensity", "Position", "Color", "Beam", "Maintenance"]

class Lamp():
    _address: 'List[Address]'
    _mode: Mode
    _number: Number
    _cache: 'Dict[str, Any]'

    def __init__(self, number: Number, mode: Mode, address: Optional[Union[Address, Iterable[Address]]] = None) -> None:
        self._cache = {}
        self._number = number
        self._mode = mode
        if address:
            if not isinstance(address, Iterable):
                self._address = [address]
            else:
                self._address = [a for a in address]
        else:
            self._address = []

    @property
    def number(self) -> Number:
        return self._number

    @number.setter
    def number(self, number = Number):
        self._number = number

    @property
    def mode(self) -> Mode:
        return self._mode

    @property
    def fixture(self) -> Fixture:
        return self.mode.fixture

    @property
    def channels(self) -> 'List[AbstractChannel]':
        return self.mode.channels

    @property
    def address(self) -> 'List[Address]':
        return self._address

    @address.setter
    def address(self, address: 'Union[Address, Iterable[Address]]') -> None:
        if not isinstance(address, Iterable):
            self._address = [address]
        else:
            self._address = [a for a in address]

    def add_address(self, address: 'Union[Address, Iterable[Address]]') -> None:
        if not self.address:
            self._address = []
        if not isinstance(address, Iterable):
            self._address.append(address)
        else:
            self._address.extend(address)
    
    @property
    def hasAddress(self) -> bool:
        return len(self._address) > 0

    @property
    def dmxRange(self) -> int:
        return len(self.mode.channels)

    @property
    def capabilities(self) -> 'Dict[_cap_types, Optional[Union[int, Dict[str, int]]]]':
        if not "capabilities" in self._cache.keys():
            capabilities: 'Dict[_cap_types, Optional[Union[int, Dict[str, int]]]]' = {
                "Intensity": None,
                "Position": None,
                "Color": None,
                "Beam": None,
                "Maintenance": None
            }
            for channelnum, channel in enumerate(self.channels):
                if isinstance(channel, CoarseChannel):
                    if channel.type == "Intensity":
                        if len(channel.capabilities) == 1:
                            cap = channel.capabilities[0]
                            capabilities['Intensity'] = channelnum
                    if "color" in channel.type.lower():
                        if len(channel.capabilities) == 1:
                            cap = channel.capabilities[0]
                            if cap.type == "ColorIntensity":
                                if not capabilities['Color']:
                                    capabilities['Color'] = {}
                                capabilities['Color'][str(cap.color)] = channelnum # type: ignore
            
            self._cache["capabilities"] = capabilities

        return self._cache["capabilities"]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Lamp):
            return NotImplemented
        return self.address == o.address and self.mode == o.mode

    def __len__(self) -> int:
        return self.dmxRange

    def __repr__(self) -> str:
        return f"Lamp({self.number}, {repr(self.mode)}, {repr(self.address)})"

    def __str__(self) -> str:
        return f"{self.number}-{self.fixture.name}"
