from OpenLightControlGui.model.Effect import Effect

from typing import Iterable, Literal, Optional, Union
from numbers import Number

class BaseState():
    types: Literal
    vals: 'dict[types, Number]'
    additive: bool = False

    def __init__(self, vals: 'Optional[dict[types, Number]]' = None) -> None:
        if vals:
            self.vals = vals
        else:
            self.vals = {}

    def copy(self) -> 'BaseState':
        return BaseState(self.vals)

    def __add__(self, o: 'Union[BaseState, Iterable[BaseState]]') -> 'BaseState':
        s = self.copy()
        if isinstance(o, BaseState):
            s += o
        elif isinstance(o, Iterable):
            for state in o:
                s += state
        return s

    def __iadd__(self, o: 'Union[BaseState, Iterable[BaseState]]') -> 'BaseState':
        if isinstance(o, BaseState):
            for key, val in o.vals.items():
                if o.additive and self.vals[key]:
                    self.vals[key] += o.vals[key]
                else:
                    self.vals[key] = val
        elif isinstance(o, Iterable):
            for state in o:
                self += state
        return self

    def __str__(self) -> str:
        return f"{__class__.__name__} {', '.join(self.vals.keys())}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()


class IntesityState(BaseState):
    types = Literal["Intesity", "Indigo", "Smoke", "Fan"]

    def copy(self) -> 'IntesityState':
        return IntesityState(self.vals)


class PositionState(BaseState):
    types = Literal["Pan", "Tilt", "PosTime"]

    def copy(self) -> 'PositionState':
        return PositionState(self.vals)


class ColorState(BaseState):
    types = Literal["Hue", "Saturation", "Red", "Green", "Blue", "Slot", "Slot2", "ColorFx"]

    def copy(self) -> 'ColorState':
        return ColorState(self.vals)


class BeamState(BaseState):
    types = Literal["Gobo", "GoboRot", "GoboShake", "Focus", "Prism", "PrismRot", "PrismShake"]

    def copy(self) -> 'BeamState':
        return BeamState(self.vals)


class LampState():
    Intesity: Optional[IntesityState]
    Position: Optional[PositionState]
    Color: Optional[ColorState]
    Beam: Optional[BeamState]
    Effect: Optional[Iterable[Effect]]

    def __init__(self, Intesity: Optional[IntesityState] = None, Position: Optional[PositionState] = None, Color: Optional[ColorState] = None, Beam: Optional[BeamState] = None, Effect_: Optional[Iterable[Effect]] = None) -> None:
        self.Intesity = Intesity
        self.Position = Position
        self.Color = Color
        self.Beam = Beam
        self.Effect = Effect_

    def copy(self) -> 'LampState':
        return LampState(self.Intesity, self.Position, self.Color, self.Beam, self.Effect)

    def __add__(self, o: 'Union[LampState, Iterable[LampState]]') -> 'LampState':
        s = self.copy()
        if isinstance(o, LampState):
            s += o
        elif isinstance(o, Iterable):
            for state in o:
                s += state
        return s

    def __iadd__(self, o: 'Union[LampState, Iterable[LampState]]') -> 'LampState':
        if isinstance(o, LampState):
            for typ in ["Intesity", "Position", "Color", "Beam", "Effect"]:
                if getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(self, typ) + getattr(o, typ))
                elif not getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(o, typ))
        elif isinstance(o, Iterable):
            for state in o:
                self += state
        return self

    def __str__(self) -> str:
        ret_str = ""
        if self.Intesity:
            ret_str += "I"
        else:
            ret_str += "."
        if self.Position:
            ret_str += "P"
        else:
            ret_str += "."
        if self.Color:
            ret_str += "C"
        else:
            ret_str += "."
        if self.Beam:
            ret_str += "B"
        else:
            ret_str += "."
        if self.Effect:
            ret_str += "E"
        return f"LampState {ret_str}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()
