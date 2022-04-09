from OpenLightControlGui.model.State import State
from OpenLightControlGui.model.Cuelist import Cuelist

from typing import Dict, List, Optional, Union, Iterable

class Scene():
    _states: 'Dict[str, State]'
    _cuelists: 'Dict[str, Cuelist]'
    
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
            if isinstance(cuelists, Cuelist):
                self._cuelists["0"] = cuelists
            else:
                for i, item2 in enumerate(cuelists):
                    self._cuelists[str(i)] = item2
    
    def getState(self, name: str) -> 'Optional[State]':
        return self._states.get(name, None)
    
    def getStates(self) -> 'Dict[str, State]':
        return self._states
    
    def getCuelist(self, name: str) -> 'Optional[Cuelist]':
        return self._cuelists.get(name, None)
    
    def getCuelists(self) -> 'Dict[str, Cuelist]':
        return self._cuelists
    
    def addState(self, state: State, name: Optional[str] = None):
        if not name:
            name = str(len(self._states.keys()))
        self._states[name] = state
    
    def removeState(self, name: str):
        try:
            del self._states[name]
        except KeyError:
            pass
    
    def addCuelist(self, cuelist: Cuelist, name: Optional[str] = None):
        if not name:
            name = f"Cuelist {len(self._cuelists.keys()) + 1}"
        if not cuelist.name:
            cuelist.name = name
        self._cuelists[name] = cuelist
    
    def removeCuelist(self, name: str):
        try:
            del self._cuelists[name]
        except KeyError:
            pass
    
    def __repr__(self) -> str:
        return f"Scene of {self._states} and {self._cuelists}"
    
    def getDmxState(self, faderval: float = 1, fadertype: str = "Intensity") -> 'Dict[int, List[Optional[int]]]':
        def combine_universes(base: 'Dict[int, List[Optional[int]]]', adding: 'Dict[int, List[Optional[int]]]'):
            for num, universe in adding.items():
                if not base.get(num):
                    base[num] = universe
                else:
                    for i, channel in enumerate(universe):
                        if channel is not None:
                            base[num][i] = max(base[num][i], channel) if base[num][i] is not None else channel # type: ignore

        universes: 'Dict[int, List[Optional[int]]]' = {}

        if fadertype != "Intensity":
            print("!WARNING!: fadertype not yet supported")
        
        for state in self._states.values():
            combine_universes(universes, state.getDmxState(faderval))

        for cuelist in self._cuelists.values():
            combine_universes(universes, cuelist.getDmxState())

        for universe in universes.values():
            for i, val in enumerate(universe):
                if val is None:
                    universe[i] = 0

        return universes
