
class Address():
    _universe: int
    _address: int

    def __init__(self, universe: int, address: int) -> None:
        self._universe = universe
        self._address = address
    
    def get_universe(self) -> int:
        return self._universe
    
    def get_address(self) -> int:
        return self._address
    
    universe = property(get_universe)
    address = property(get_address)

    def __eq__(self, o: 'Address') -> bool:
        return isinstance(o, Address) and self.universe == o.universe and self.address == o.address

    def __gt__(self, o: 'Address') -> bool:
        return self.universe > o.universe or (self.universe == o.universe and self.address > o.address)
    
    def __lt__(self, o: 'Address') -> bool:
        return self.universe < o.universe or (self.universe == o.universe and self.address < o.address)

    def __str__(self) -> str:
        return f"{self.universe}:{self.address}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()
