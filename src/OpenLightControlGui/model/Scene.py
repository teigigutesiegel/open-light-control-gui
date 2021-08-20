from OpenLightControlGui.fixture_model.CoarseChannel import CoarseChannel
from OpenLightControlGui.model import State, Cuelist

from typing import Optional, Union, Iterable

from OpenLightControlGui.model.LampState import LampState

class Scene():
    _states: 'dict[str, State]'
    _cuelists: 'dict[str, Cuelist]'
    
    def __init__(self, states: 'Optional[Union[State, Iterable[State]]]' = None, cuelists: 'Optional[Union[Cuelist, Iterable[Cuelist]]]' = None) -> None:
        self._states = {}
        if states:
            if isinstance(states, Iterable):
                for i, item in enumerate(states):
                    self._states[str(i)] = item
            else:
                self._states["0"] = states
        self._cuelists = {}
        if cuelists:
            if isinstance(cuelists, Iterable):
                for i, item in enumerate(cuelists):
                    self._cuelists[str(i)] = item
            else:
                self._cuelists["0"] = cuelists
    
    def getState(self, name: str) -> 'Optional[State]':
        return self._states.get(name, None)
    
    def getStates(self) -> 'dict[str, State]':
        return self._states
    
    def getCuelist(self, name: str) -> 'Optional[Cuelist]':
        return self._cuelists.get(name, None)
    
    def getCuelists(self) -> 'dict[str, Cuelist]':
        return self._cuelists
    
    def addState(self, state: State, name: Optional[str] = None):
        if not name:
            name = len(self._states.keys())
        self._states[name] = state
    
    def addCuelist(self, cuelist: Cuelist, name: Optional[str] = None):
        if not name:
            name = len(self._cuelists.keys())
        self._cuelists[name] = cuelist
    
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
        
        for state in self._states.values():
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
                                    if state.state.Intensity.Intensity.unit == "%":
                                        val = state.state.Intensity.Intensity.getBaseUnitEntity().number / 100 * 255
                                    else:
                                        val = state.state.Intensity.Intensity.getBaseUnitEntity().number
                                    universes[address.universe][address.address + cap['Intensity']] = int(val * faderval)
                    if state.state.Position:
                        pass
                    if state.state.Color:
                        if not cap['Color'] == None:
                            for coltype in ["Red", "Green", "Blue"]:
                                if coltype in cap['Color'].keys():
                                    if getattr(state.state.Color, coltype):
                                        for address in lamp.address:
                                            if getattr(state.state.Color, coltype).unit == "col":
                                                val = int(getattr(state.state.Color, coltype).getBaseUnitEntity().number * 255)
                                            else:
                                                val = int(getattr(state.state.Color, coltype).getBaseUnitEntity().number)
                                            universes[address.universe][address.address + cap['Color'][coltype]] = val
                    if state.state.Beam:
                        pass
                    if state.state.Maintenance:
                        pass
        
        return universes
