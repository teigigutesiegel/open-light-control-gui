from typing import Dict, Iterable, List, Optional, Union
from OpenLightControlGui.fixture_model.Entity import Entity

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
                for item2 in state:
                    self.addState(item2)
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

    @property
    def group(self) -> 'Group':
        return self._group

    @group.setter
    def group(self, group: 'Group'):
        self._group = group

    def getGroup(self) -> 'Group':
        return self.group

    def setGroup(self, group: 'Group'):
        self._group = group

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

    @property
    def state(self) -> LampState:
        return self._state

    @state.setter
    def state(self, state: LampState) -> None:
        self._state = state

    def getState(self) -> LampState:
        return self.state
    
    def setState(self, state: LampState) -> None:
        self.state = state

    def __repr__(self) -> str:
        return f"State of {self.group}"

    def getDmxState(self, faderval: float = 1) -> 'Dict[int, List[int]]':
        universes: 'Dict[int, List[int]]' = {}
        for lamp in self.group.getLamps():
            for address in lamp.address:
                if not address.universe in universes.keys():
                    universes[address.universe] = [0]*512
            cap = lamp.capabilities
            if self.state:
                if self.state.Intensity:
                    if self.state.Intensity.Intensity:
                        if isinstance(self.state.Intensity.Intensity, Entity):
                            if isinstance(cap['Intensity'], int):
                                for address in lamp.address:
                                    if self.state.Intensity.Intensity.unit == "%":
                                        val = self.state.Intensity.Intensity.getBaseUnitEntity().number / 100 * 255
                                    else:
                                        val = self.state.Intensity.Intensity.getBaseUnitEntity().number
                                    universes[address.universe][address.address + cap['Intensity']] = int(val * faderval) # type: ignore
                            elif isinstance(cap['Intensity'], dict):
                                val = self.state.Intensity.Intensity.getBaseUnitEntity().number
                                ls = sorted(cap['Intensity'].items(), reverse=True) # type: ignore
                                for address in lamp.address:
                                    if self.state.Intensity.Intensity.unit == "%":
                                        val = val / 100
                                        val = int(val * faderval * (2**(8*ls[0][0])-1)).to_bytes(ls[0][0], "big") # type: ignore
                                        for res, num in cap['Intensity'].items():
                                            universes[address.universe][address.address + num] = val[res-1] # type: ignore
                                    else:
                                        val = int(val * faderval * (2**(8*ls[0][0])-1)).to_bytes(ls[0][0], "big") # type: ignore
                                        for res, num in cap['Intensity'].items():
                                            universes[address.universe][address.address + num] = val[res-1] # type: ignore

                if self.state.Position:
                    pass
                if self.state.Color:
                    if isinstance(cap['Color'], dict):
                        for coltype in ["Red", "Green", "Blue"]:
                            if coltype in cap['Color'].keys() and isinstance(getattr(self.state.Color, coltype), Entity):
                                if isinstance(cap['Color'][coltype], int):
                                    for address in lamp.address:
                                        if getattr(self.state.Color, coltype).unit == "col":
                                            val = int(getattr(self.state.Color, coltype).getBaseUnitEntity().number * 255)
                                        else:
                                            val = int(getattr(self.state.Color, coltype).getBaseUnitEntity().number)
                                        universes[address.universe][address.address + cap['Color'][coltype]] = val  # type: ignore
                                elif isinstance(cap['Color'][coltype], dict):
                                    val = getattr(self.state.Color, coltype).getBaseUnitEntity().number
                                    ls = sorted(cap['Color'][coltype].items(), reverse=True) # type: ignore
                                    for address in lamp.address:
                                        if getattr(self.state.Color, coltype).unit == "col":
                                            val = int(val * (2**(8*ls[0][0])-1)).to_bytes(ls[0][0], "big") # type: ignore
                                            for res, num in cap['Color'][coltype].items(): # type: ignore
                                                universes[address.universe][address.address + num] = val[res-1] # type: ignore
                                        else:
                                            val = int(val).to_bytes(ls[0][0], "big") # type: ignore
                                            for res, num in cap['Color'][coltype].items(): # type: ignore
                                                universes[address.universe][address.address + num] = val[res-1] # type: ignore

                if self.state.Beam:
                    pass
                if self.state.Maintenance:
                    pass
        
        return universes
