from PyQt5.QtWidgets import QWidget, QPushButton, QToolBar, QMainWindow
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QSize, pyqtSignal

from OpenLightControlGui import ColorCircle, PalletteDirectoryView
from OpenLightControlGui.model import LampState

from typing import Optional
import os
basepath = os.path.dirname(__file__)

class ColorDirectoryView(PalletteDirectoryView):
    _colorToolbar: QToolBar
    _colorbut: QPushButton
    _colors: 'dict[int, LampState]'

    color_selected = pyqtSignal(int, LampState)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__("Color", parent=parent, placeholder=placeholder)
        self._colors = {}

        self._colorToolbar = QToolBar()
        self._colorbut = QPushButton()
        self._colorbut.setIconSize(QSize(30, 30))
        self._colorbut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/color-management.svg")))
        self._colorbut.pressed.connect(self._openColorCircle)
        self._colorToolbar.addWidget(self._colorbut)
        self.insertToolBar(self._mainToolbar, self._colorToolbar)

    def addColor(self, num: int, state: LampState, name: Optional[str] = None, color: Optional['QColor'] = None) -> None:
        self._colors[num] = state
        if not name:
            name = f"Color {num}"
        if color == None and state.Color and all(x != None for x in [state.Color.Red, state.Color.Green, state.Color.Blue]):
            color = QColor.fromRgbF(state.Color.Red.number, state.Color.Green.number, state.Color.Blue.number, 1)
        item = self.ViewTile(num, name, color)
        if state.Intensity:
            item.hasIntensity = True
        if state.Position:
            item.hasPosition = True
        if state.Color:
            item.hasColor = True
        if state.Beam:
            item.hasBeam = True
        if state.Effect:
            item.hasEffects = True
        if state.Maintenance:
            item.hasControl = True
        item.recalc()
        item.selected.connect(lambda num: self._handle_TileClick(num))
        self.setItem(num, item)
    
    def getColor(self, num: int) -> Optional[LampState]:
        return self._colors.get(num)

    def _handle_TileClick(self, num: int) -> None:
        self.color_selected.emit(num, self._colors.get(num))

    def _openColorCircle(self) -> None:
        wid = ColorCircle()
        win = QMainWindow(self)
        win.setCentralWidget(wid)
        win.setWindowTitle("Color Picker")
        win.setGeometry(0, 0, 500, 500)
        win.show()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = ColorDirectoryView()
    window.show()
    sys.exit(app.exec_())
