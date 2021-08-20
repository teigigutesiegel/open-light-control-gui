from OpenLightControlGui.model import Group
from OpenLightControlGui import AbstractDirectoryView

from typing import Optional, TYPE_CHECKING

from PyQt5.QtCore import pyqtSignal

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QColor


class GroupDirectoryView(AbstractDirectoryView):
    _groups: 'dict[int, Group]'

    group_selected = pyqtSignal(int, Group)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__(parent=parent, placeholder=placeholder)
        self._groups = {}

        self._title = "Group"
        self.setWindowTitle(f"{self._title} Directory")
    
    def addGroup(self, num: int, group: Group, color: Optional['QColor'] = None) -> None:
        self._groups[num] = group
        if not group.name:
            group.name = f"Group {num}"
        item = self.ViewTile(num, group.name, color)
        item.selected.connect(lambda num: self._handle_TileClick(num))
        self.setItem(num, item)
    
    def getGroup(self, num: int) -> Optional[Group]:
        return self._groups.get(num)

    def _handle_TileClick(self, num: int) -> None:
        self.group_selected.emit(num, self._groups.get(num))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = GroupDirectoryView()
    window.show()
    window.tile_selected.connect(lambda num: print(f"Tile {num} selected"))
    window.group_selected.connect(lambda num, group: print(f"{group} at {num} selected"))
    sys.exit(app.exec_())
