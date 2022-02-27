from OpenLightControlGui.model.Effect import Effect
from OpenLightControlGui.fixture_model import Entity

from typing import Dict, Iterable, Literal, Optional, Union, get_type_hints


class LampState():
    class BaseState():
        vals: 'Dict[str, Union[Entity, str, bool]]'
        additive: bool = False

        def __init__(self, vals: 'Optional[Dict[str, Union[Entity, str, bool]]]' = None, *, additive: bool = False) -> None:
            self.vals = {}
            if vals:
                for k, v in vals.items():
                    if isinstance(v, Entity):
                        self.vals[k] = v.copy()
                    else:
                        self.vals[k] = v
            if additive:
                self.additive = additive

        def copy(self) -> 'LampState.BaseState':
            new: 'Dict[str, Union[Entity, str, bool]]' = {}
            for k, v in self.vals.items():
                if isinstance(v, Entity):
                    new[k] = v.copy()
                else:
                    new[k] = v
            return LampState.BaseState(new)

        def __getitem__(self, typ: str) -> Optional[Union[Entity, str, bool]]:
            return self.vals.get(typ)

        def __setitem__(self, typ: str, val: Union[Entity, str]) -> None:
            self.vals[typ] = val
        
        def __eq__(self, o: object) -> bool:
            if not isinstance(o, LampState.BaseState):
                return NotImplemented
            return self.vals == o.vals

        def __add__(self, o: 'Union[LampState.BaseState, Iterable[LampState.BaseState]]') -> 'LampState.BaseState':
            s = self.copy()
            if isinstance(o, LampState.BaseState):
                s += o
            elif isinstance(o, Iterable):
                for state in o:
                    s += state
            return s

        def __iadd__(self, o: 'Union[LampState.BaseState, Iterable[LampState.BaseState]]') -> 'LampState.BaseState':
            if isinstance(o, LampState.BaseState):
                for key, val in o.vals.items():
                    if o.additive and self.vals.get(key) is not None and isinstance(self.vals[key], Entity) and isinstance(o.vals[key], Entity):
                        self.vals[key] += o.vals[key] # type: ignore
                    else:
                        self.vals[key] = val
            elif isinstance(o, Iterable):
                for state in o:
                    self += state
            return self

        def __str__(self) -> str:
            return f"{self.__class__.__name__} {', '.join(self.vals.keys())}"

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({repr(self.vals)}, additive={self.additive})"

        def __bool__(self) -> bool:
            return bool(self.vals)

    class IntensityState(BaseState):
        types = Literal["Intensity", "Intensity2", "Smoke", "Fan", "Strobe"]

        def copy(self) -> 'LampState.IntensityState':
            return LampState.IntensityState(self.vals.copy())

        @property
        def Intensity(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Intensity")

        @Intensity.setter
        def Intensity(self, val: Entity) -> None:
            setattr(self, "Intensity", val)

        @property
        def Intensity2(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Intensity2")

        @Intensity2.setter
        def Intensity2(self, val: Entity) -> None:
            setattr(self, "Intensity2", val)

        @property
        def Smoke(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Smoke")

        @Smoke.setter
        def Smoke(self, val: Entity) -> None:
            setattr(self, "Smoke", val)

        @property
        def Fan(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Fan")

        @Fan.setter
        def Fan(self, val: Entity) -> None:
            setattr(self, "Fan", val)

        @property
        def Strobe(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Strobe")

        @Strobe.setter
        def Strobe(self, val: Entity) -> None:
            setattr(self, "Strobe", val)

    class PositionState(BaseState):
        types = Literal["Pan", "Tilt", "PosTime"]

        def copy(self) -> 'LampState.PositionState':
            return LampState.PositionState(self.vals.copy())

        @property
        def Pan(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Pan")

        @Pan.setter
        def Pan(self, val: Entity) -> None:
            setattr(self, "Pan", val)

        @property
        def Tilt(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Tilt")

        @Tilt.setter
        def Tilt(self, val: Entity) -> None:
            setattr(self, "Tilt", val)

        @property
        def PosTime(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "PosTime")

        @PosTime.setter
        def PosTime(self, val: Entity) -> None:
            setattr(self, "PosTime", val)

    class ColorState(BaseState):
        types = Literal["Hue", "Saturation", "Red",
                        "Green", "Blue", "Slot", "Slot2", "ColorFx"]

        def copy(self) -> 'LampState.ColorState':
            return LampState.ColorState(self.vals.copy())

        @property
        def Hue(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Hue")

        @Hue.setter
        def Hue(self, val: Entity) -> None:
            setattr(self, "Hue", val)

        @property
        def Saturation(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Saturation")

        @Saturation.setter
        def Saturation(self, val: Entity) -> None:
            setattr(self, "Saturation", val)

        @property
        def Red(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Red")

        @Red.setter
        def Red(self, val: Entity) -> None:
            setattr(self, "Red", val)

        @property
        def Green(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Green")

        @Green.setter
        def Green(self, val: Entity) -> None:
            setattr(self, "Green", val)

        @property
        def Blue(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Blue")

        @Blue.setter
        def Blue(self, val: Entity) -> None:
            setattr(self, "Blue", val)

        @property
        def Slot(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Slot")

        @Slot.setter
        def Slot(self, val: Entity) -> None:
            setattr(self, "Slot", val)

        @property
        def Slot2(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Slot2")

        @Slot2.setter
        def Slot2(self, val: Entity) -> None:
            setattr(self, "Slot2", val)

        @property
        def ColorFx(self) -> 'Optional[Union[Entity, str]]':
            return getattr(self, "ColorFx")

        @ColorFx.setter
        def ColorFx(self, val: Union[Entity, str]) -> None:
            setattr(self, "ColorFx", val)

    class BeamState(BaseState):
        types = Literal["Gobo", "GoboRot", "GoboShake", "Gobo2", "Gobo2Rot",
                        "Gobo2Shake", "Focus", "Prism", "PrismRot", "PrismShake"]

        def copy(self) -> 'LampState.BeamState':
            return LampState.BeamState(self.vals.copy())

        @property
        def Gobo(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Gobo")

        @Gobo.setter
        def Gobo(self, val: Entity) -> None:
            setattr(self, "Gobo", val)

        @property
        def GoboRot(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "GoboRot")

        @GoboRot.setter
        def GoboRot(self, val: Entity) -> None:
            setattr(self, "GoboRot", val)

        @property
        def GoboShake(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "GoboShake")

        @GoboShake.setter
        def GoboShake(self, val: Entity) -> None:
            setattr(self, "GoboShake", val)

        @property
        def Gobo2(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Gobo2")

        @Gobo2.setter
        def Gobo2(self, val: Entity) -> None:
            setattr(self, "Gobo2", val)

        @property
        def Gobo2Rot(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Gobo2Ro2")

        @Gobo2Rot.setter
        def Gobo2Rot(self, val: Entity) -> None:
            setattr(self, "Gobo2Rot", val)

        @property
        def Gobo2Shake(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Gobo2Shake")

        @Gobo2Shake.setter
        def Gobo2Shake(self, val: Entity) -> None:
            setattr(self, "Gobo2Shake", val)

        @property
        def Focus(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Focus")

        @Focus.setter
        def Focus(self, val: Entity) -> None:
            setattr(self, "Focus", val)

        @property
        def Prism(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "Prism")

        @Prism.setter
        def Prism(self, val: Entity) -> None:
            setattr(self, "Prism", val)

        @property
        def PrismRot(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "PrismRot")

        @PrismRot.setter
        def PrismRot(self, val: Entity) -> None:
            setattr(self, "PrismRot", val)

        @property
        def PrismShake(self) -> 'Optional[Union[str, Entity]]':
            return getattr(self, "PrismShake")

        @PrismShake.setter
        def PrismShake(self, val: Entity) -> None:
            setattr(self, "PrismShake", val)

    class MaintenanceState(BaseState):
        def copy(self) -> 'LampState.MaintenanceState':
            return LampState.MaintenanceState(self.vals.copy())
        
        def set_val(self, typ: str, val: bool = True) -> None:
            self.vals[typ] = val
        
        def get_val(self) -> str:
            return list(self.vals.keys())[0]

    Intensity: Optional[IntensityState]
    Position: Optional[PositionState]
    Color: Optional[ColorState]
    Beam: Optional[BeamState]
    Effect_: 'Optional[Iterable[Effect]]'
    Maintenance: Optional[MaintenanceState]

    def __init__(self, Intensity: Optional[IntensityState] = None, Position: Optional[PositionState] = None, Color: Optional[ColorState] = None, Beam: Optional[BeamState] = None, Effect_: 'Optional[Iterable[Effect]]' = None, Maintenance: Optional[MaintenanceState] = None) -> None:
        self.Intensity = Intensity
        self.Position = Position
        self.Color = Color
        self.Beam = Beam
        self.Effect_ = []
        if Effect_:
            for i in Effect_:
                self.Effect_.append(i)
        self.Maintenance = Maintenance

    def copy(self) -> 'LampState':
        return LampState(self.Intensity, self.Position, self.Color, self.Beam, self.Effect_)

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
            for typ in ["Intensity", "Position", "Color", "Beam", "Effect_"]:
                if getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(self, typ) + getattr(o, typ))
                elif not getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(o, typ))
        elif isinstance(o, Iterable):
            for state in o:
                self += state
        return self

    def __sub__(self, o: 'Union[LampState, Iterable[LampState]]') -> 'LampState':
        s = self.copy()
        if isinstance(o, LampState):
            s -= o
        elif isinstance(o, Iterable):
            for state in o:
                s -= state
        return s

    def __isub__(self, o: 'Union[LampState, Iterable[LampState]]') -> 'LampState':
        if isinstance(o, LampState):
            for typ in ["Intensity", "Position", "Color", "Beam", "Effect_"]:
                if getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(self, typ) - getattr(o, typ))
                elif not getattr(self, typ) and getattr(o, typ):
                    setattr(self, typ, getattr(o, typ))
        elif isinstance(o, Iterable):
            for state in o:
                self -= state
        return self

    def __repr__(self) -> str:
        ret_str = ""
        if self.Intensity:
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
        if self.Effect_:
            ret_str += "E"
        if self.Maintenance:
            ret_str += "L"
        return f"LampState {ret_str}"

    def __bool__(self) -> bool:
        return bool(self.Intensity) or bool(self.Position) or bool(self.Color) or bool(self.Beam) or bool(self.Effect_)
