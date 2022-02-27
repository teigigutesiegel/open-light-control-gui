from OpenLightControlGui.model import State
from OpenLightControlGui import AbstractDirectoryView

from typing import Dict, Optional, TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QColor


class StateDirectoryView(AbstractDirectoryView):
    _states: 'Dict[int, State]'

    state_selected = pyqtSignal(int, State)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__(parent=parent, placeholder=placeholder)
        self._states = {}

        self._title = "State"
        self.setWindowTitle(f"{self._title} Directory")
    
    def addState(self, num: int, state: State, name: Optional[str] = None, color: Optional['QColor'] = None) -> None:
        self._states[num] = state
        if not name:
            name = f"State {num}"
        item = self.ViewTile(num, name, color)
        item.selected.connect(lambda num: self._handle_TileClick(num))
        self.setItem(num, item)
    
    def getState(self, num: int) -> Optional[State]:
        return self._states.get(num)

    def _handle_TileClick(self, num: int) -> None:
        if not self._guard_mode:
            self.state_selected.emit(num, self._states.get(num))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = StateDirectoryView()
    window.show()
    window.tile_selected.connect(lambda num: print(f"Tile {num} selected"))
    window.state_selected.connect(lambda num, group: print(f"{group} at {num} selected"))
    sys.exit(app.exec_())
