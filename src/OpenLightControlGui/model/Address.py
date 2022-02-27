
class Address():
    _universe: int
    _address: int

    def __init__(self, universe: int, address: int) -> None:
        self._universe = universe
        self._address = address

    @property
    def universe(self) -> int:
        return self._universe

    @universe.setter
    def universe(self, universe: int) -> None:
        self._universe = universe

    @property
    def address(self) -> int:
        return self._address

    @address.setter
    def address(self, address: int) -> None:
        self._address = address
    
    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Address):
            return NotImplemented
        return self.universe < o.universe or (self.universe == o.universe and self.address < o.address)
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Address):
            return NotImplemented
        return self.universe == o.universe and self.address == o.address

    def __str__(self) -> str:
        return f"{self.universe}:{self.address}"
    
    def __repr__(self) -> str:
        return f"Address(universe={self.universe}, address={self.address})"
