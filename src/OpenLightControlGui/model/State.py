from typing import Iterable, Optional, Union

from OpenLightControlGui.model.Lamp import Lamp
from OpenLightControlGui.model.Group import Group
from OpenLightControlGui.model.LampState import LampState

class State():
    _group: 'Group'
    _state: 'LampState'

    def __init__(self, groups: 'Optional[Union[Lamp, Iterable[Lamp], Group, Iterable[Group]]]' = None, state: 'Optional[Union[LampState, Iterable[LampState]]]' = None) -> None:
        self._group = Group()
        if groups:
            if isinstance(groups, Iterable):
                for item in groups:
                    self.addItem(item)
            else:
                self.addItem(groups)
        
        self._state = LampState()
        if state:
            if isinstance(state, Iterable):
                for item in state:
                    self.addState(item)
            else:
                self.addState(state)

    def addLamp(self, lamp: Lamp) -> None:
        self.addGroup(Group(lamp))
    
    def removeLamp(self, lamp: Lamp) -> None:
        if self._group.includes(lamp):
            self._group -= lamp

    def addGroup(self, group: Group) -> None:
        self._group += group
    
    def removeGroup(self, group: Group) -> None:
        self._group -= group
    
    def getGroup(self) -> 'Group':
        return self._group
    
    def setGroup(self, group: 'Group'):
        self._group = group
    
    group: 'Group' = property(getGroup, setGroup)
    
    def addItem(self, item: Union[Lamp, Group]) -> None:
        if isinstance(item, Lamp):
            self.addLamp(item)
        elif isinstance(item, Group):
            self.addGroup(item)
        else:
            raise TypeError(f"Type {type(item)} does not match {Lamp} or {Group}")
    
    def removeItem(self, item: Union[Lamp, Group]) -> None:
        if isinstance(item, Group):
            self.removeGroup(item)
        else:
            self.removeLamp(item)
    
    def addState(self, state: LampState) -> None:
        if self._state:
            self._state += state
        else:
            self._state = state
    
    def removeState(self, state: LampState) -> None:
        self._state -= state

    def getState(self) -> LampState:
        return self._state
    
    def setState(self, state: LampState) -> None:
        self._state = state
    
    state: LampState = property(getState, setState)

    def __str__(self) -> str:
        return f"State of {self.group}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def getDmxState(self, faderval: float = 1) -> 'dict[int, list[int]]':
        universes = {}
        for lamp in self.group.getLamps():
            for address in lamp.address:
                if not address.universe in universes.keys():
                    universes[address.universe] = [0]*512
            cap = lamp.capabilities
            if self.state:
                if self.state.Intensity:
                    if self.state.Intensity.Intensity:
                        if not cap['Intensity'] == None:
                            for address in lamp.address:
                                if self.state.Intensity.Intensity.unit == "%":
                                    val = self.state.Intensity.Intensity.getBaseUnitEntity().number / 100 * 255
                                else:
                                    val = self.state.Intensity.Intensity.getBaseUnitEntity().number
                                universes[address.universe][address.address + \
                                    cap['Intensity']] = int(val * faderval)
                if self.state.Position:
                    pass
                if self.state.Color:
                    if not cap['Color'] == None:
                        for coltype in ["Red", "Green", "Blue"]:
                            if coltype in cap['Color'].keys():
                                if getattr(self.state.Color, coltype):
                                    for address in lamp.address:
                                        if getattr(self.state.Color, coltype).unit == "col":
                                            val = int(
                                                getattr(self.state.Color, coltype).getBaseUnitEntity().number * 255)
                                        else:
                                            val = int(
                                                getattr(self.state.Color, coltype).getBaseUnitEntity().number)
                                        universes[address.universe][address.address + \
                                            cap['Color'][coltype]] = val
                if self.state.Beam:
                    pass
                if self.state.Maintenance:
                    pass
        
        return universes
