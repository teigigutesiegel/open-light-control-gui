from typing import Dict, Iterable, List, Union, Optional
from OpenLightControlGui.model.State import State

class Cue():
    _states: 'List[State]'
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

    @property
    def states(self) -> 'List[State]':
        return self._states

    def getStates(self) -> 'List[State]':
        return self.states

    @property
    def name(self) -> 'Optional[str]':
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def num(self) -> 'Optional[int]':
        return self._num

    @num.setter
    def num(self, num: int) -> None:
        self._num = num

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, ms: int) -> None:
        self._duration = ms

    @property
    def fade(self) -> Optional[int]:
        return self._fadein

    @fade.setter
    def fade(self, ms: int) -> None:
        self._fadein = ms

    def __repr__(self) -> str:
        if self.name:
            return self.name
        if self.num:
            return f"Cue {self.num}"
        return f"Cue of {self.states}"

    def getDmxState(self, faderval: float = 1, fadertype: str = "Intensity") -> 'Dict[int, List[int]]':
        def combine_universes(base: 'Dict[int, List[int]]', adding: 'Dict[int, List[int]]'):
            for num, universe in adding.items():
                if not base.get(num):
                    base[num] = universe
                else:
                    for i, channel in enumerate(universe):
                        base[num][i] = max(base[num][i], channel)

        universes: 'Dict[int, List[int]]' = {}

        if fadertype != "Intensity":
            print("!WARNING!: fadertype not yet supported")

        for state in self.states:
            combine_universes(universes, state.getDmxState(faderval))

        return universes
