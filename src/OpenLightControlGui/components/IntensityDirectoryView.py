# pyright: reportGeneralTypeIssues=false, reportOptionalMemberAccess=false
from OpenLightControlGui import PalletteDirectoryView
from OpenLightControlGui.model import LampState

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget


class IntensityDirectoryView(PalletteDirectoryView):
    _intens: 'dict[int, LampState]'

    intens_selected = pyqtSignal(int, LampState)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__("Intensity", parent=parent, placeholder=placeholder)

        self._intens = {}

    def addIntensity(self, num: int, state: LampState, name: Optional[str] = None, color: Optional['QColor'] = None) -> None:
        self._intens[num] = state
        if not name:
            name = f"Inten {num}"
        if color == None and state.Color and all(x is not None for x in [state.Color.Red, state.Color.Green, state.Color.Blue]):
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

    def getIntens(self, num: int) -> Optional[LampState]:
        return self._intens.get(num)

    def _handle_TileClick(self, num: int) -> None:
        self.intens_selected.emit(num, self._intens.get(num))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = IntensityDirectoryView()
    window.show()
    sys.exit(app.exec_())
