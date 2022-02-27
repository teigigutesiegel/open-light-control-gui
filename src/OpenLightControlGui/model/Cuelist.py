from typing import Dict, Iterable, Iterator, List, Optional
import time

from OpenLightControlGui.model.Cue import Cue
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class Cuelist(QObject):
    _cues: 'List[Cue]'
    _name: str
    _currCue: int = 0
    _standardFade: int = 0
    _standardDuration: int = 0

    _fadetimer: QTimer
    _fadestart: int = 0
    _fadetime: int = 0
    _cuetimer: QTimer

    currentCueChanged = pyqtSignal(int)

    _lastdmxstate: 'Dict[int, List[int]]'
    _nextdmxstate: 'Dict[int, List[int]]'
    _dmxstate: 'Dict[int, List[int]]'

    _faderval: float = 1.0
    _paused: bool = False

    def __init__(self, cues: 'Iterable[Cue]', name: 'Optional[str]' = None) -> None:
        super().__init__()
        self._cues = []
        self._lastdmxstate = {}
        self._nextdmxstate = {}
        self._dmxstate = {}
        for i, cue in enumerate(cues):
            self.addCue(cue, i)
        if name:
            self.name = name
        self._fadetimer = QTimer()
        self._cuetimer = QTimer()
    
    def addCue(self, cue: Cue, num: Optional[int] = None) -> None:
        if num is None:
            num = len(self._cues)
        self._cues.insert(num, cue)
        self._recalc()
    
    def removeCue(self, num: int) -> None:
        del self._cues[num]
        self._recalc()
    
    def getCue(self, num: int) -> Optional[Cue]:
        return self._cues[num] if num < len(self._cues) else None

    def _recalc(self):
        for i, cue in enumerate(self._cues):
            if not cue.name:
                cue.num = i + 1
    
    @property
    def name(self) -> 'Optional[str]':
        return getattr(self, "_name", None)

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
    
    @property
    def currCue(self) -> int:
        return self._currCue
    
    @property
    def standardFade(self) -> int:
        return self._standardFade
    
    @standardFade.setter
    def standardFade(self, ms: int) -> None:
        self._standardFade = ms

    @property
    def standardDuration(self) -> int:
        return self._standardDuration
    
    @standardDuration.setter
    def standardDuration(self, ms: int) -> None:
        self._standardDuration = ms
    
    @property
    def faderval(self) -> float:
        return self._faderval

    @faderval.setter
    def faderval(self, val: float) -> None:
        self._faderval = val
        self._dmxstate = self._cues[self.currCue].getDmxState(faderval=self._faderval)

    def back(self):
        try:
            self._cuetimer.timeout.disconnect(self.go)
        except:
            pass
        try:
            self._cuetimer.timeout.disconnect(self.back)
        except:
            pass
        if self.currCue == 0:
                self.goto(len(self._cues) - 1, True)
        else:
            self.goto(self.currCue - 1, True)

    def go(self):
        if self._paused:
            self._cuetimer.start()
            self._paused = False
        else:
            try:
                self._cuetimer.timeout.disconnect(self.go)
            except:
                pass
            try:
                self._cuetimer.timeout.disconnect(self.back)
            except:
                pass
            if self.currCue == len(self._cues) - 1:
                self.goto(0)
            else:
                self.goto(self.currCue + 1)
    
    def goto(self, num, back: bool = False):
        fadetime = self.standardFade
        curcue = self._cues[self.currCue]
        nextcue = self._cues[num]
        if nextcue.fade != None:
            fadetime = nextcue.fade
        duration = self.standardDuration
        if nextcue.duration != None:
            duration = nextcue.duration
        if duration > 0:
            if back:
                self._cuetimer.timeout.connect(self.back) # type: ignore
            else:
                self._cuetimer.timeout.connect(self.go) # type: ignore
            self._cuetimer.start(fadetime +  duration)
        if fadetime == 0:
            self._nextdmxstate = {}
            self._dmxstate = nextcue.getDmxState(faderval=self._faderval)
        else:
            self._fadetime = fadetime
            self._lastdmxstate = curcue.getDmxState(faderval=self._faderval)
            self._nextdmxstate = nextcue.getDmxState(faderval=self._faderval)
            self._fadetimer.timeout.connect(self._fade) # type: ignore
            self._fadestart = time.time_ns() // 1000000
            self._fadetimer.start(10)
        self._currCue = num
        self.currentCueChanged.emit(self.currCue)
    
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
        
        x = (time.time_ns() // 1000000 - self._fadestart)
        ti = x / self._fadetime
        if x > self._fadetime:
            ti = 1
            self._fadetimer.stop()
            self._fadetimer.timeout.disconnect(self._fade)
        
        uni_num = list(set([*self._lastdmxstate.keys(), *self._nextdmxstate.keys()]))
        unis = {}
        for uni in uni_num:
            if not unis.get(uni):
                unis[uni] = [0]*512
            l = self._lastdmxstate.get(uni, [0]*512)
            n = self._nextdmxstate.get(uni, [0]*512)
            for i in range(len(l)):
                unis[uni][i] = fadeval(ti, l[i], n[i]) if l[i] or n[i] else 0
        self._dmxstate = unis

    def getDmxState(self) -> 'Dict[int, List[int]]':
        return self._dmxstate

    def isRunning(self) -> bool:
        return self.getDmxState() != {}

    def isPaused(self) -> bool:
        return self._paused

    def __repr__(self) -> str:
        if self.name:
            return f"Cuelist {self.name}"
        return f"Cuelist of {self._cues}"
    
    def __len__(self) -> int:
        return len(self._cues)
    
    def __iter__(self) -> 'Iterator[Cue]':
        return iter(self._cues)
    
    def __getitem__(self, key) -> 'Cue':
        return self._cues[key]
