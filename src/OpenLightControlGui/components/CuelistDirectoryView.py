from OpenLightControlGui.model import Cuelist
from OpenLightControlGui import AbstractDirectoryView

from typing import Optional, TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSpinBox, QTableWidgetItem

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QColor


class CuelistDirectoryView(AbstractDirectoryView):
    _cuelists: 'dict[int, Cuelist]'
    _dropdowns: 'dict[int, tuple[QSpinBox, QSpinBox]]'

    cuelist_selected = pyqtSignal(int, Cuelist)
    cuelist_right_click = pyqtSignal(int, Cuelist)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__(parent=parent, placeholder=placeholder)
        self._cuelists = {}
        self._dropdowns = {}

        self._title = "Cuelist"
        self.setWindowTitle(f"{self._title} Directory")

        self._mainTable.setColumnCount(5)
        self._mainTable.setHorizontalHeaderItem(3, QTableWidgetItem("FadeTime"))
        self._mainTable.setHorizontalHeaderItem(4, QTableWidgetItem("Duration"))
    
    def _add_table_item(self, item: "AbstractDirectoryView.ViewTile") -> None:
        dropdown = QSpinBox()
        dropdown.setMinimum(-1)
        dropdown.setMaximum(10000)
        dropdown.setValue(self.getCuelist(item._num).standardFade)
        dropdown.valueChanged.connect(
            lambda val, num=item._num: self.dofade(val, num))
        dropdown2 = QSpinBox()
        dropdown2.setMinimum(-1)
        dropdown2.setMaximum(10000)
        dropdown2.setValue(self.getCuelist(item._num).standardDuration)
        dropdown2.valueChanged.connect(
            lambda val, num=item._num: self.doduration(val, num))
        self._mainTable.setCellWidget(item._num-1, 3, dropdown)
        self._mainTable.setCellWidget(item._num-1, 4, dropdown2)
        self._dropdowns[item._num] = (dropdown, dropdown2)
        return super()._add_table_item(item)
    
    def dofade(self, val, num):
        if val < 0:
            val = None
        c = self.getCuelist(num)
        c.standardFade = val or 0
        for cue in c._cues:
            cue.fade = val
    
    def doduration(self, val, num):
        if val < 0:
            val = None
        c = self.getCuelist(num)
        c.standardDuration = val or 0
        for cue in c._cues:
            cue.duration = val
    
    def addCuelist(self, num: int, cuelist: Cuelist, name: Optional[str] = None, color: Optional['QColor'] = None) -> None:
        self._cuelists[num] = cuelist
        if not name:
            if cuelist.name:
                name = cuelist.name
            else:
                name = f"Cuelist {num}"
                cuelist.name = name
        item = self.ViewTile(num, name, color)
        item.selected.connect(lambda num: self._handle_TileClick(num))
        item.right_click.connect(lambda num: self._handle_RightClick(num))
        self.setItem(num, item)
    
    def getCuelist(self, num: int) -> Optional[Cuelist]:
        return self._cuelists.get(num)

    def _handle_TileClick(self, num: int) -> None:
        if not self._guard_mode:
            self.cuelist_selected.emit(num, self._cuelists.get(num))
    
    def _handle_RightClick(self, num: int):
        if not self._guard_mode:
            self.cuelist_right_click.emit(num, self._cuelists.get(num))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = CuelistDirectoryView()
    window.show()
    window.tile_selected.connect(lambda num: print(f"Tile {num} selected"))
    window.cuelist_selected.connect(lambda num, cuelist: print(f"{cuelist} at {num} selected"))
    sys.exit(app.exec_())
