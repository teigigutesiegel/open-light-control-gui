from .WheelSlot import WheelSlot

from typing import Literal, Any
from numbers import Number
from functools import cmp_to_key
from math import floor, ceil


class Wheel():
    '''Information about a fixture's wheel.'''
    _name: str
    _jsonObject: 'dict[str, Any]'
    _cache: 'dict[str, Any]'

    def __init__(self, wheelName: str, jsonObject: 'dict[str, Any]') -> None:
        self._name = wheelName
        self._jsonObject = jsonObject
        self._cache = {
            "splitSlots": {},
            "slotsOfType": {}
        }
    
    def __str__(self) -> str:
        return f"Wheel <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_name(self) -> str:
        return self._name

    def _get_direction(self) -> 'Literal["CW", "CCW"]':
        return self._jsonObject.get("direction", "CW") or "CW"

    def _get_type(self) -> str:
        slotTypes = [slot.type for slot in self.slots]

        def sorter(a: str, b: str) -> int:
            occurrencesOfA = slotTypes.count(a)
            occurrencesOfB = slotTypes.count(b)
            return occurrencesOfA - occurrencesOfB

        slotTypes.sort(key=cmp_to_key(sorter))

        type = slotTypes.pop()

        if type.startswith("AnimationGobo"):
            return "AnimationGobo"

        return type

    def _get_slots(self) -> 'list[WheelSlot]':
        if not "slots" in self._cache.keys():
            self._cache["slots"] = [
                WheelSlot(slotJson, self) for slotJson in self._jsonObject["slots"]]

        return self._cache["slots"]

    def getSlot(self, slotNumber: Number) -> WheelSlot:
        if slotNumber % 1 == 0:
            return self.slots[self.getAbsoluteSlotIndex(slotNumber)]

        floorIndex = self.getAbsoluteSlotIndex(floor(slotNumber))
        ceilIndex = self.getAbsoluteSlotIndex(ceil(slotNumber))
        splitKey = f"Split {floorIndex}/{ceilIndex}"

        if not splitKey in self._cache["splitSlots"].keys():
            floorSlot = self.slots[floorIndex]
            ceilSlot = self.slots[ceilIndex]

            self._cache["splitSlots"][splitKey] = WheelSlot(
                None, self, floorSlot, ceilSlot)

        return self._cache["splitSlots"][splitKey]

    def getAbsoluteSlotIndex(self, slotNumber: int) -> int:
        '''returns int The zero-based slot index, bounded by the number of slots.'''
        return int(((slotNumber - 1) % len(self.slots)) + (len(self.slots) if slotNumber < 1 else 0))

    def getSlotsOfType(self, type_: str) -> 'list[WheelSlot]':
        '''returns list[<WheelSlot>] All slots with the given type.'''
        if not type_ in self._cache["slotsOfType"]:
            self._cache["slotsOfType"][type_] = list(
                filter(lambda slot: slot.type == type_, self.slots))

        return self._cache["slotsOfType"][type_]

    name: str = property(_get_name)
    direction: 'Literal["CW", "CCW"]' = property(_get_direction)
    type: str = property(_get_type)
    slots: 'list[WheelSlot]' = property(_get_slots)
