# pyright: reportGeneralTypeIssues=false
from OpenLightControlGui.model import *

s = State()
cuelist = Cuelist([])
c1 = Cue(s, "C1")
c2 = Cue(s, "C2")
c3 = Cue(s, "C3")
cuelist.addCue(c1)
cuelist.addCue(c3)
cuelist.addCue(c2, 1)

print(cuelist)
