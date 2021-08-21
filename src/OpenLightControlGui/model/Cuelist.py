from typing import Iterable, Optional
from numbers import Number
import time

from OpenLightControlGui.model.Cue import Cue
from PyQt5.QtCore import QTimer

class Cuelist():
    _cues: 'list[Cue]'
    _name: str
    _currCue: int = 0
    _standardFade: int = 0

    _fadetimer: QTimer
    _fadestart: int = 0
    _fadetime: int = 0
    _cuetimer: QTimer

    _lastdmxstate: 'dict[int, list[int]]'
    _nextdmxstate: 'dict[int, list[int]]'
    _dmxstate: 'dict[int, list[int]]'

    _faderval: float = 1.0
    _paused: bool = False

    def __init__(self, cues: 'Iterable[Cue]', name: 'Optional[str]' = None) -> None:
        self._cues = []
        self._lastdmxstate = {}
        self._nextdmxstate = {}
        self._dmxstate = {}
        for i, cue in enumerate(cues):
            self.addCue(cue, i)
        if name:
            self.name = name
        self._fadetimer = QTimer(self)
    
    def addCue(self, cue: Cue, num: Optional[Number] = None) -> None:
        if num == None:
            num = len(self._cues)
        self._cues.insert(num, cue)
        self._recalc()
    
    def removeCue(self, num: Number) -> None:
        del self._cues[num]
        self._recalc()
    
    def getCue(self, num: Number) -> Optional[Cue]:
        return self._cues[num] if num < len(self._cues) else None

    def _recalc(self):
        for i, cue in enumerate(self._cues):
            if not cue.name:
                cue.num = i + 1
    
    def _getName(self) -> 'Optional[str]':
        return getattr(self, "_name", None)
    
    def _setName(self, name: str) -> None:
        self._name = name
    
    def _getcurrCue(self) -> int:
        return self._currCue
    
    def _getstandardFade(self) -> int:
        return self._standardFade
    
    def _setstandardFade(self, ms: int) -> None:
        self._standardFade = ms

    name: 'Optional[str]' = property(_getName, _setName)
    currCue: int = property(_getcurrCue)
    standardFade: int = property(_getstandardFade, _setstandardFade)

    def go(self):
        if self._paused:
            self._cuetimer.start()
            self._paused = False
        else:
            try:
                self._cuetimer.timeout.disconnect(self.go)
            except:
                pass
            if self.currCue == len(self._cues) - 1:
                self.goto(0)
            else:
                self.goto(self.currCue + 1)
    
    def goto(self, num):
        fadetime = self.standardFade
        curcue = self._cues[self.currCue]
        nextcue = self._cues[num]
        if nextcue.fade != None:
            fadetime = nextcue.fade
        if nextcue.duration > 0:
            self._cuetimer.timeout.connect(self.go)
            self._cuetimer.start(fadetime +  nextcue.duration)
        if fadetime == 0:
            self._nextdmxstate = {}
            self._dmxstate = nextcue.getDmxState(faderval=self._faderval)
        else:
            self._fadetime = fadetime
            self._lastdmxstate = curcue.getDmxState(faderval=self._faderval)
            self._nextdmxstate = curcue.getDmxState(faderval=self._faderval)
            self._fadetimer.timeout.connect(self._fade)
            self._fadestart = time.time_ns() // 1000000
            self._fadetimer.start(10)
    
    def pause(self, pause: bool = True):
        if pause:
            self._cuetimer.stop()
        else:
            self._cuetimer.start()
        self._paused = pause

    def stop(self):
        self._cuetimer.stop()
        self._fadetimer.stop()
        self._dmxstate = {}

    def _fade(self):
        def fadeval(ti: float, f: int = 0, t: int = 0) -> int:
            return int(f * (1-ti) + t * ti)
        
        ti = (time.time_ns() // 1000000 - self._fadestart) / self._fadetime
        uni_num = list(set([*self._lastdmxstate.keys(), *self._nextdmxstate.keys()]))
        unis = {}
        for uni in uni_num:
            if not unis.get(uni):
                unis[uni] = [0]*512
            l = self._lastdmxstate.get(uni, [0]*512)
            n = self._nextdmxstate.get(uni, [0]*512)
            for i in range(len(l)):
                unis[uni][i] = fadeval(ti, l[i], n[i])
        self._dmxstate = unis

    def getDmxState(self) -> 'dict[int, list[int]]':
        return self._dmxstate

    
    def __str__(self) -> str:
        if self.name:
            return f"Cuelist {self.name}"
        return f"Cuelist of {self._cues}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, format_spec: str) -> str:
        return self.__str__()
