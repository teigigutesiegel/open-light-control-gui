from OpenLightControlGui.fixture_model.CoarseChannel import CoarseChannel
from OpenLightControlGui.model import State, Cuelist

from typing import Optional, Union, Iterable

from OpenLightControlGui.model.LampState import LampState

class Scene():
    _states: 'list[State]'
    _cuelists: 'list[Cuelist]'
    
    def __init__(self, states: 'Optional[Union[State, Iterable[State]]]' = None, cuelists: 'Optional[Union[Cuelist, Iterable[Cuelist]]]' = None) -> None:
        self._states = []
        if states:
            if isinstance(states, Iterable):
                for item in states:
                    self._states.append(item)
            else:
                self._states.append(states)
        self._cuelists = []
        if cuelists:
            if isinstance(cuelists, Iterable):
                for item in cuelists:
                    self._cuelists.append(item)
            else:
                self._cuelists.append(cuelists)
    
    def __str__(self) -> str:
        return f"Scene of {self._states} and {self._cuelists}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()
    
    def getDmxState(self, faderval: float = 1, fadertype: str = "Intensity") -> 'dict[int, list[int]]':
        universes = {}

        if fadertype != "Intensity":
            print("!WARNING!: fadertype not yet supported")
        
        for state in self._states:
            for lamp in state.group.getLamps():
                for address in lamp.address:
                    if not address.universe in universes.keys():
                        universes[address.universe] = [0]*512
                cap = lamp.capabilities
                if state.state:
                    if state.state.Intensity:
                        if state.state.Intensity.Intensity:
                            if not cap['Intensity'] == None:
                                for address in lamp.address:
                                    universes[address.universe][address.address + cap['Intensity']] = int(state.state.Intensity.Intensity.getBaseUnitEntity().number * faderval)
                    if state.state.Position:
                        pass
                    if state.state.Color:
                        if not cap['Color'] == None:
                            for coltype in ["Red", "Green", "Blue"]:
                                if coltype in cap['Color'].keys():
                                    if getattr(state.state.Color, coltype):
                                        for address in lamp.address:
                                            universes[address.universe][address.address + cap['Color'][coltype]] = getattr(state.state.Color, coltype).getBaseUnitEntity().number
                    if state.state.Beam:
                        pass
                    if state.state.Maintenance:
                        pass
        
        return universes
