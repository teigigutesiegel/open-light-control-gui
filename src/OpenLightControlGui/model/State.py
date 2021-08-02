from typing import Iterable, Optional, Union

from OpenLightControlGui.model.Lamp import Lamp
from OpenLightControlGui.model.Group import Group
from OpenLightControlGui.model.LampState import LampState

class State():
    _groups: 'list[Group]'
    _state: 'Optional[LampState]'

    def __init__(self, groups: 'Optional[Union[Lamp, Iterable[Lamp], Group, Iterable[Group]]]' = None, state: 'Optional[LampState]' = None) -> None:
        self._groups = []
        if groups:
            if isinstance(groups, Iterable):
                for item in groups:
                    self.addItem(item)
            else:
                self.addItem(groups)
        
        self._state = state

    def addLamp(self, lamp: Lamp) -> None:
        self.addGroup(Group(lamp))
    
    def removeLamp(self, lamp: Lamp) -> None:
        for i, group in enumerate(self._groups):
            if group.includes(lamp):
                self._groups.pop(i)
                break

    def addGroup(self, group: Group) -> None:
        self._groups.append(group)
    
    def removeGroup(self, group: Group) -> None:
        self._groups.pop(self._groups.index(group))
    
    def getGroups(self) -> 'list[Group]':
        return self._groups
    
    groups: 'list[Group]' = property(getGroups)
    
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
        return f"State of {self.groups}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()
