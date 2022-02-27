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
    
    def removeState(self, name: str):
        del self._states[name]
    
    def addCuelist(self, cuelist: Cuelist, name: Optional[str] = None):
        if not name:
            name = f"Cuelist {len(self._cuelists.keys()) + 1}"
        if not cuelist.name:
            cuelist.name = name
        self._cuelists[name] = cuelist
    
    def removeCuelist(self, name: str):
        del self._cuelists[name]
    
    def __repr__(self) -> str:
        return f"Scene of {self._states} and {self._cuelists}"
    
    def getDmxState(self, faderval: float = 1, fadertype: str = "Intensity") -> 'dict[int, list[int]]':
        def combine_universes(base: 'dict[int, list[int]]', adding: 'dict[int, list[int]]'):
            for num, universe in adding.items():
                if not base.get(num):
                    base[num] = universe
                else:
                    for i, channel in enumerate(universe):
                        base[num][i] = max(base[num][i], channel)

        universes: 'dict[int, list[int]]' = {}

        if fadertype != "Intensity":
            print("!WARNING!: fadertype not yet supported")
        
        for state in self._states.values():
            combine_universes(universes, state.getDmxState(faderval))

        for cuelist in self._cuelists.values():
            combine_universes(universes, cuelist.getDmxState())
        
        return universes
