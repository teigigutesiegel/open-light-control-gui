from .Entity import Entity
from .Resource import Resource

import re
from typing import TYPE_CHECKING, Any, Optional, Union, Callable
from numbers import Number

if TYPE_CHECKING:
    from .Wheel import Wheel


def _Color(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    if name != None and slot.colorTemperature != None:
        return f"{name} ({slot.colorTemperature})"

    if slot.colorTemperature != None:
        return str(slot.colorTemperature)

    return name


def _Gobo(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    if name == None:
        if slot.resource != None:
            return f"Gobo {getattr(slot.resource, 'name', slot.resource)}"

        return None

    if name.startswith("Gobo"):
        return name

    return f"Gobo {name}"


def _Prism(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    if name != None and slot.facets != None:
        return f"{slot.facets}-facet {name}"

    if slot.facets != None:
        return f"{slot.facets}-facet prism"

    return name


def _Iris(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    if slot.openPercent != None:
        return f"Iris {slot.openPercent}"

    return None


def _Frost(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    if slot.frostIntensity != None:
        return f"Frost {slot.frostIntensity}"

    return None


def _Split(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    return f"Split {slot.floorSlot.name} / {slot.ceilSlot.name}"


def _AnimationGoboStart(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    return f"{name} Start" if name != None else None


def _AnimationGoboEnd(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    slotNumber = slot._wheel.slots.index(slot) + 1
    previousSlot = slot._wheel.getSlot(slotNumber - 1)

    return str(previousSlot.name) + " End" if previousSlot.name else None


def _AnimationGobo(slot: 'WheelSlot', name: 'Optional[str]') -> str:
    return slot.floorSlot.name.replace(" Start", "")


namePerType: 'dict[str, Callable[[WheelSlot, Optional[str]], Optional[str]]]' = {
    "Color": _Color,
    "Gobo": _Gobo,
    "Prism": _Prism,
    "Iris": _Iris,
    "Frost": _Frost,
    "Split": _Split,
    "AnimationGoboStart": _AnimationGoboStart,
    "AnimationGoboEnd": _AnimationGoboEnd,
    "AnimationGobo": _AnimationGobo,
    "Default": lambda slot, name: name
}


class WheelSlot():
    '''Information about a single wheel slot (or a split slot).'''
    _jsonObject: 'Optional[dict[str, Any]]'
    _wheel: 'Wheel'
    _floorSlot: 'Optional[WheelSlot]'
    _ceilSlot: 'Optional[WheelSlot]'
    _cache: 'dict[str, Any]'

    def __init__(self, jsonObject: 'Optional[dict[str, Any]]', wheel: 'Wheel', floorSlot: 'Optional[WheelSlot]' = None, ceilSlot: 'Optional[WheelSlot]' = None) -> None:
        self._jsonObject = jsonObject
        self._wheel = wheel
        self._floorSlot = floorSlot
        self._ceilSlot = ceilSlot
        self._cache = {}
    
    def __str__(self) -> str:
        return f"WheelSlot <{self.type}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_isSplitSlot(self) -> bool:
        return self._jsonObject == None

    def _get_type(self) -> str:
        if not "type" in self._cache.keys():
            if not self.isSplitSlot:
                self._cache["type"] = self._jsonObject["type"]
            elif self._floorSlot.type == "AnimationGoboStart":
                self._cache["type"] = "AnimationGobo"
            else:
                self._cache["type"] = "Split"

        return self._cache["type"]

    def _get_nthOfType(self) -> int:
        if not "nthOfType" in self._cache.keys():
            self._cache["nthOfType"] = self._wheel.getSlotsOfType(
                self.type).index(self)

        return self._cache["nthOfType"]

    def _get_resource(self) -> 'Optional[Union[Resource, str]]':
        if not "resource" in self._cache.keys():
            if self.isSplitSlot or not "resource" in self._jsonObject.keys():
                self._cache["resource"] = None
            elif isinstance(self._jsonObject["resource"], str):
                self._cache["resource"] = self._jsonObject["resource"]
            else:
                self._cache["resource"] = Resource(
                    self._jsonObject["resource"])

        return self._cache["resource"]

    def _get_name(self) -> str:
        if not "name" in self._cache.keys():
            nameFunction = namePerType[self.type] if self.type in namePerType.keys(
            ) else namePerType["Default"]
            name = nameFunction(
                self, None if self.isSplitSlot else self._jsonObject.get("name"))

            if name == None:
                typeName = re.sub(
                    "([a-z])([A-Z])", lambda mat: " ".join(mat.groups()), self.type)
                name = typeName if len(self._wheel.getSlotsOfType(
                    self.type)) == 1 else f"{typeName} {self.nthOfType + 1}"

            self._cache["name"] = name

        return self._cache["name"]

    def _get_colors(self) -> 'Optional[list[str]]':
        if not "colors" in self._cache.keys():
            fixedColors = {
                "Open": ["#ffffff"],
                "Closed": ["#000000"]
            }

            self._cache["colors"] = None

            if self.type in fixedColors:
                self._cache["colors"] = fixedColors[self.type]
            elif self.isSplitSlot:
                if self._floorSlot.colors and self._ceilSlot.colors:
                    self._cache["colors"] = self._floorSlot.colors + \
                        self._ceilSlot.colors
            elif "colors" in self._jsonObject.keys():
                self._cache["colors"] = self._jsonObject["colors"]

        return self._cache["colors"]

    def _get_colorTemperature(self) -> 'Optional[Entity]':
        if not "colorTemperature" in self._cache.keys():
            self._cache["colorTemperature"] = Entity.createFromEntityString(
                self._jsonObject["colorTemperature"]) if "colorTemperature" in self._jsonObject.keys() else None

        return self._cache["colorTemperature"]

    def _get_facets(self) -> 'Optional[Number]':
        return self._jsonObject.get("factes", None) or None

    def _get_openPercent(self) -> 'Optional[Entity]':
        if not "openPercent" in self._cache.keys():
            self._cache["openPercent"] = Entity.createFromEntityString(
                self._jsonObject["openPercent"]) if "openPercent" in self._jsonObject.keys() else None

        return self._cache["openPercent"]

    def _get_frostIntensity(self) -> 'Optional[Entity]':
        if not "frostIntensity" in self._cache.keys():
            self._cache["frostIntensity"] = Entity.createFromEntityString(
                self._jsonObject["frostIntensity"]) if "frostIntensity" in self._jsonObject.keys() else None

        return self._cache["frostIntensity"]

    def _get_floorSlot(self) -> 'Optional[WheelSlot]':
        return self._floorSlot or None

    def _get_ceilSlot(self) -> 'Optional[WheelSlot]':
        return self._ceilSlot or None

    isSplitSlot: bool = property(_get_isSplitSlot)
    type: str = property(_get_type)
    nthOfType: int = property(_get_nthOfType)
    resource: 'Optional[Union[Resource, str]]' = property(_get_resource)
    name: str = property(_get_name)
    colors: 'Optional[list[str]]' = property(_get_colors)
    colorTemperature: 'Optional[Entity]' = property(_get_colorTemperature)
    facets: 'Optional[Number]' = property(_get_facets)
    openPercent: 'Optional[Entity]' = property(_get_openPercent)
    frostIntensity: 'Optional[Entity]' = property(_get_frostIntensity)
    floorSlot: 'Optional[WheelSlot]' = property(_get_floorSlot)
    ceilSlot: 'Optional[WheelSlot]' = property(_get_ceilSlot)
