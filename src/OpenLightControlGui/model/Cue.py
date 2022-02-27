from typing import Iterable, Union, Optional
from OpenLightControlGui.model.State import State

class Cue():
    _states: 'list[State]'
    _name: 'Optional[str]' = None
    _num: 'Optional[int]' = None
    _duration: int = 0
    _fadein: 'Optional[int]' = None

    def __init__(self, states: 'Union[State, Iterable[State]]', name: 'Optional[str]' = None, num: 'Optional[int]' = None) -> None:
        self._states = []
        if isinstance(states, Iterable):
            for state in states:
                self.addState(state)
        else:
            self.addState(states)
        if name:
            self.name = name
        if num != None:
            self.num = num
    
    def addState(self, state: State) -> None:
        self._states.append(state)
    
    def removeState(self, state: State) -> None:
        if state in self._states:
            self._states.pop(self._states.index(state))
    
    def getStates(self) -> 'list[State]':
        return self._states
    
    states: 'list[State]' = property(getStates)

    def _getName(self) -> 'Optional[str]':
        return self._name
    
    def _setName(self, name: str) -> None:
        self._name = name
    
    name: 'Optional[str]' = property(_getName, _setName)
    
    def _getNum(self) -> 'Optional[num]':
        return self._num
    
    def _setNum(self, num: int) -> None:
        self._num = num

    num: 'Optional[int]' = property(_getNum, _setNum)
    
    def _getDuration(self) -> int:
        return self._duration
    
    def _setDuration(self, ms: int) -> None:
        self._duration = ms

    duration: int = property(_getDuration, _setDuration)
        
    def _getFadeIn(self) -> int:
        return self._fadein
    
    def _setFadeIn(self, ms: int) -> None:
        self._fadein = ms
    
    fade: 'Optional[int]' = property(_getFadeIn, _setFadeIn)
        
    def __repr__(self) -> str:
        if self.name:
            return self.name
        if self.num:
            return f"Cue {self.num}"
        return f"Cue of {self.states}"

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

        for state in self.states:
            combine_universes(universes, state.getDmxState(faderval))

        return universes
