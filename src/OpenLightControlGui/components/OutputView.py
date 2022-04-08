from OpenLightControlGui.model import Scene, State, Group, Lamp, LampState
from OpenLightControlGui.components.FlowLayout import FlowLayout

from typing import Dict, Optional, List

from PyQt5.QtWidgets import QScrollArea, QWidget, QApplication, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

class Tombstone(QWidget):
    lamp: Lamp
    lampstate: LampState

    def __init__(self, lamp: Lamp, lampstate: LampState) -> None:
        super().__init__()
        self.lamp = lamp
        self.lampstate = lampstate

        self.main_lay = QVBoxLayout()
        self.lamp_num = QLabel()
        self.lamp_intens = QLabel()
        self.lamp_pan = QLabel()
        self.lamp_tilt = QLabel()
        self.main_lay.addWidget(self.lamp_num)
        self.main_lay.addWidget(self.lamp_intens)
        self.main_lay.addWidget(self.lamp_pan)
        self.main_lay.addWidget(self.lamp_tilt)

        self.main_wid = QWidget()
        self.main_wid.setObjectName("tombstone")
        self.main_wid.setLayout(self.main_lay)

        slay = QVBoxLayout()
        slay.addWidget(self.main_wid)
        self.setLayout(slay)

        self.update()
    
    def update(self):
        self.lamp_num.setText(str(self.lamp.number))
        self.lamp_intens.setText(str(self.lampstate.Intensity.Intensity if self.lampstate.Intensity else "-"))
        self.lamp_pan.setText(str(self.lampstate.Position.Pan if self.lampstate.Position else "-"))
        self.lamp_tilt.setText(str(self.lampstate.Position.Tilt if self.lampstate.Position else "-"))
        
        if self.lamp.capabilities["Color"] and self.lampstate.Color:
            rgb = []
            for i, coltype in enumerate(["Red", "Green", "Blue"]):
                if getattr(self.lampstate.Color, coltype).unit == "col":
                    val = int(getattr(self.lampstate.Color, coltype).getBaseUnitEntity().number * 255)
                else:
                    val = int(getattr(self.lampstate.Color, coltype).getBaseUnitEntity().number)
                rgb.append(val)
            self.setStyleSheet("#tombstone { border: 1px solid rgb(" + ','.join([str(x) for x in rgb]) + ") }")
        else:
            self.setStyleSheet("#tombstone { border: 1px solid lightgrey }")

class OutputView(QWidget):
    scene: 'List[Scene]'
    main_lay: FlowLayout
    stone_dict: Dict[int, Tombstone]

    def __init__(self, scene: 'List[Scene]', parent: Optional[QWidget] = None):
        super(OutputView, self).__init__(parent)
        self.scene = scene
        self.stone_dict = {}

        self.setWindowTitle("OutputView")

        self.main_lay = FlowLayout(margin=10)
        wid = QWidget()
        wid.setLayout(self.main_lay)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(wid)
        lay = QVBoxLayout()
        lay.addWidget(scroll)
        self.setLayout(lay)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update) # type: ignore
        self.timer.start(100)
        self.update()

    def update(self):
        self.stone_dict.clear()
        self.main_lay.clear()
        for scene in self.scene:
            for name, state in scene.getStates().items():
                for lamp in state.group.lamps:
                    self.stone_dict[lamp.number] = Tombstone(lamp, state.state)
        for _, lamp in sorted(self.stone_dict.items()):
            self.main_lay.addWidget(lamp)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    scene = Scene()
    scene.addState(State(Group(), LampState()), "Scene")
    window = OutputView(scene)
    window.show()
    sys.exit(app.exec_())
