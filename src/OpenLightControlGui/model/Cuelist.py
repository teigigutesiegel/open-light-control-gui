from typing import Iterable, Optional
from numbers import Number

from OpenLightControlGui.model.Cue import Cue

class Cuelist():
    _cues: 'dict[Number, Cue]'

    def __init__(self, cues: 'Iterable[Cue]') -> None:
        self._cues = []
        for i, cue in enumerate(cues):
            self.addCue(i, cue)
    
    def addCue(self, num: Number, cue: Cue) -> None:
        self._cues[num] = cue
    
    def removeCue(self, num: Number) -> None:
        del self._cues[num]
    
    def getCue(self, num: Number) -> Optional[Cue]:
        return self._cues.get(num)
