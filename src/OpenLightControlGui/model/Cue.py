from typing import Iterable, Union
from OpenLightControlGui.model.State import State

class Cue():
    _states: 'list[State]'

    def __init__(self, states: 'Union[State, Iterable[State]]') -> None:
        self._states = []
        if isinstance(states, Iterable):
            for state in states:
                self.addState(state)
        else:
            self.addState(states)
    
    def addState(self, state: State) -> None:
        self._states.append(state)
    
    def removeState(self, state: State) -> None:
        if state in self._states:
            self._states.pop(self._states.index(state))
    
    def getStates(self) -> 'list[State]':
        return self._states
    
    states: 'list[State]' = property(getStates)
