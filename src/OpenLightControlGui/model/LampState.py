from OpenLightControlGui.model.Effect import Effect
from OpenLightControlGui.fixture_model import Entity

from typing import Iterable, Literal, Optional, Union


class LampState():
    class BaseState():
        types: Literal
        vals: 'dict[types, Union[Entity, str]]'
        additive: bool = False

        def __init__(self, vals: 'Optional[dict[types, Union[Entity, str]]]' = None) -> None:
            if vals:
                self.vals = vals
            else:
                self.vals = {}

        def copy(self) -> 'LampState.BaseState':
            return LampState.BaseState(self.vals)

        def _set_val(self, typ: str, val: Union[Entity, str]) -> None:
            self.vals[typ] = val

        def _get_val(self, typ: str) -> Optional[Union[Entity, str]]:
            return self.vals.get(typ)

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
                    if o.additive and self.vals[key]:
                        self.vals[key] += o.vals[key]
                    else:
                        self.vals[key] = val
            elif isinstance(o, Iterable):
                for state in o:
                    self += state
            return self

        def __str__(self) -> str:
            return f"{self.__class__.__name__} {', '.join(self.vals.keys())}"

        def __repr__(self) -> str:
            return self.__str__()

        def __format__(self, format_spec: str) -> str:
            return self.__str__()

        def __bool__(self) -> bool:
            return bool(self.vals)

    class IntensityState(BaseState):
        types = Literal["Intensity", "Intensity2", "Smoke", "Fan", "Strobe"]

        def copy(self) -> 'LampState.IntensityState':
            return LampState.IntensityState(self.vals)

        def _set_i(self, val: Entity) -> None:
            self._set_val("Intensity", val)

        def _get_i(self) -> 'Optional[Entity]':
            return self._get_val("Intensity")

        def _set_i2(self, val: Entity) -> None:
            self._set_val("Intensity2", val)

        def _get_i2(self) -> 'Optional[Entity]':
            return self._get_val("Intensity2")

        def _set_smoke(self, val: Entity) -> None:
            self._set_val("Smoke", val)

        def _get_smoke(self) -> 'Optional[Entity]':
            return self._get_val("Smoke")

        def _set_fan(self, val: Entity) -> None:
            self._set_val("Fan", val)

        def _get_fan(self) -> 'Optional[Entity]':
            return self._get_val("Fan")
        
        def _set_strobe(self, val: Entity) -> None:
            self._set_val("Strobe", val)
        
        def _get_strobe(self) -> 'Optional[Entity]':
            return self._get_val("Strobe")

        Intensity: 'Optional[Entity]' = property(_get_i, _set_i)
        Intensity2: 'Optional[Entity]' = property(_get_i2, _set_i2)
        Smoke: 'Optional[Entity]' = property(_get_smoke, _set_smoke)
        Fan: 'Optional[Entity]' = property(_get_fan, _set_fan)
        Strobe: 'Optional[Entity]' = property(_get_strobe, _set_strobe)

    class PositionState(BaseState):
        types = Literal["Pan", "Tilt", "PosTime"]

        def copy(self) -> 'LampState.PositionState':
            return LampState.PositionState(self.vals)

        def _set_p(self, val: Entity) -> None:
            self._set_val("Pan", val)

        def _get_p(self) -> 'Optional[Entity]':
            return self._get_val("Pan")

        def _set_t(self, val: Entity) -> None:
            self._set_val("Tilt", val)

        def _get_t(self) -> 'Optional[Entity]':
            return self._get_val("Tilt")

        def _set_pt(self, val: Entity) -> None:
            self._set_val("PosTime", val)

        def _get_pt(self) -> 'Optional[Entity]':
            return self._get_val("PosTime")

        Pan: 'Optional[Entity]' = property(_get_p, _set_p)
        Tilt: 'Optional[Entity]' = property(_get_t, _set_t)
        PosTime: 'Optional[Entity]' = property(_get_pt, _set_pt)

    class ColorState(BaseState):
        types = Literal["Hue", "Saturation", "Red",
                        "Green", "Blue", "Slot", "Slot2", "ColorFx"]

        def copy(self) -> 'LampState.ColorState':
            return LampState.ColorState(self.vals)

        def _set_h(self, val: Entity) -> None:
            self._set_val("Hue", val)

        def _get_h(self) -> 'Optional[Entity]':
            return self._get_val("Hue")

        def _set_s(self, val: Entity) -> None:
            self._set_val("Saturation", val)

        def _get_s(self) -> 'Optional[Entity]':
            return self._get_val("Saturation")

        def _set_r(self, val: Entity) -> None:
            self._set_val("Red", val)

        def _get_r(self) -> 'Optional[Entity]':
            return self._get_val("Red")

        def _set_g(self, val: Entity) -> None:
            self._set_val("Green", val)

        def _get_g(self) -> 'Optional[Entity]':
            return self._get_val("Green")

        def _set_b(self, val: Entity) -> None:
            self._set_val("Blue", val)

        def _get_b(self) -> 'Optional[Entity]':
            return self._get_val("Blue")

        def _set_slot(self, val: Entity) -> None:
            self._set_val("Slot", val)

        def _get_slot(self) -> 'Optional[Entity]':
            return self._get_val("Slot")

        def _set_slot2(self, val: Entity) -> None:
            self._set_val("Slot2", val)

        def _get_slot2(self) -> 'Optional[Entity]':
            return self._get_val("Slot2")

        def _set_fx(self, val: Union[Entity, str]) -> None:
            self._set_val("ColorFx", val)

        def _get_fx(self) -> 'Optional[Union[Entity, str]]':
            return self._get_val("ColorFx")

        Hue: 'Optional[Entity]' = property(_get_h, _set_h)
        Saturation: 'Optional[Entity]' = property(_get_s, _set_s)
        Red: 'Optional[Entity]' = property(_get_r, _set_r)
        Green: 'Optional[Entity]' = property(_get_g, _set_g)
        Blue: 'Optional[Entity]' = property(_get_b, _set_b)
        Slot: 'Optional[Entity]' = property(_get_slot, _set_slot)
        Slot2: 'Optional[Entity]' = property(_get_slot2, _set_slot2)
        ColorFx: 'Optional[Entity]' = property(_get_fx, _set_fx)

    class BeamState(BaseState):
        types = Literal["Gobo", "GoboRot", "GoboShake", "Gobo2", "Gobo2Rot",
                        "Gobo2Shake", "Focus", "Prism", "PrismRot", "PrismShake"]

        def copy(self) -> 'LampState.BeamState':
            return LampState.BeamState(self.vals)

        def _set_g(self, val: Entity) -> None:
            self._set_val("Gobo", val)

        def _get_g(self) -> 'Optional[Entity]':
            return self._get_val("Gobo")

        def _set_gr(self, val: Entity) -> None:
            self._set_val("GoboRot", val)

        def _get_gr(self) -> 'Optional[Entity]':
            return self._get_val("GoboRot")

        def _set_gs(self, val: Entity) -> None:
            self._set_val("GoboShake", val)

        def _get_gs(self) -> 'Optional[Entity]':
            return self._get_val("GoboShake")

        def _set_g2(self, val: Entity) -> None:
            self._set_val("Gobo", val)

        def _get_g2(self) -> 'Optional[Entity]':
            return self._get_val("Gobo")

        def _set_g2r(self, val: Entity) -> None:
            self._set_val("GoboRot", val)

        def _get_g2r(self) -> 'Optional[Entity]':
            return self._get_val("GoboRot")

        def _set_g2s(self, val: Entity) -> None:
            self._set_val("GoboShake", val)

        def _get_g2s(self) -> 'Optional[Entity]':
            return self._get_val("GoboShake")

        def _set_f(self, val: Entity) -> None:
            self._set_val("Focus", val)

        def _get_f(self) -> 'Optional[Entity]':
            return self._get_val("Focus")

        def _set_p(self, val: Entity) -> None:
            self._set_val("Prism", val)

        def _get_p(self) -> 'Optional[Entity]':
            return self._get_val("Prism")

        def _set_pr(self, val: Entity) -> None:
            self._set_val("PrismRot", val)

        def _get_pr(self) -> 'Optional[Entity]':
            return self._get_val("PrismRot")

        def _set_ps(self, val: Entity) -> None:
            self._set_val("PrismShake", val)

        def _get_ps(self) -> 'Optional[Entity]':
            return self._get_val("PrismShake")

        Gobo: 'Optional[Entity]' = property(_get_g, _set_g)
        GoboRot: 'Optional[Entity]' = property(_get_gr, _set_gr)
        GoboShake: 'Optional[Entity]' = property(_get_gs, _set_gs)
        Gobo2: 'Optional[Entity]' = property(_get_g2, _set_g2)
        Gobo2Rot: 'Optional[Entity]' = property(_get_g2r, _set_g2r)
        Gobo2Shake: 'Optional[Entity]' = property(_get_g2s, _set_g2s)
        Focus: 'Optional[Entity]' = property(_get_f, _set_f)
        Prism: 'Optional[Entity]' = property(_get_p, _set_p)
        PrismRot: 'Optional[Entity]' = property(_get_pr, _set_pr)
        PrismShake: 'Optional[Entity]' = property(_get_ps, _set_ps)

    class MaintenanceState(BaseState):
        def copy(self) -> 'LampState.MaintenanceState':
            return LampState.MaintenanceState(self.vals)
        
        def set_val(self, typ: str) -> None:
            self.vals = { typ: True }
        
        def get_val(self) -> str:
            return list(self.vals.keys())[0]

    Intensity: Optional[IntensityState]
    Position: Optional[PositionState]
    Color: Optional[ColorState]
    Beam: Optional[BeamState]
    Effect: Optional[Iterable[Effect]]
    Maintenance: Optional[MaintenanceState]

    def __init__(self, Intensity: Optional[IntensityState] = None, Position: Optional[PositionState] = None, Color: Optional[ColorState] = None, Beam: Optional[BeamState] = None, Effect_: Optional[Iterable[Effect]] = None, Maintenance: Optional[MaintenanceState] = None) -> None:
        self.Intensity = Intensity
        self.Position = Position
        self.Color = Color
        self.Beam = Beam
        self.Effect = []
        if Effect_:
            for i in Effect_:
                self.Effect.append(i)
        self.Maintenance = Maintenance

    def copy(self) -> 'LampState':
        return LampState(self.Intensity, self.Position, self.Color, self.Beam, self.Effect)

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
            for typ in ["Intensity", "Position", "Color", "Beam", "Effect"]:
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
        if self.Effect:
            ret_str += "E"
        if self.Maintenance:
            ret_str += "L"
        return f"LampState {ret_str}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.Intensity) or bool(self.Position) or bool(self.Color) or bool(self.Beam) or bool(self.Effect)
