from dataclasses import dataclass

@dataclass(frozen=True, order=True, slots=True)
class Address():
    universe: int
    address: int

    def __str__(self) -> str:
        return f"{self.universe}:{self.address}"
