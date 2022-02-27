
from OpenLightControlGui.model import Cuelist, State
from OpenLightControlGui import AbstractDirectoryView

from typing import Any, Optional, TYPE_CHECKING, Union

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QColor


class CommandDirectoryView(AbstractDirectoryView):
    _options = ["Go", "Pause", "Back", "Flash", "Stop", "Toggle", "Start", "End"]
    _commands: 'dict[int, dict[str, Any]]'
    _dropdowns: 'dict[int, tuple[QComboBox, QComboBox]]'

    command_selected = pyqtSignal(int, dict)
    command_right_click = pyqtSignal(int, dict)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__(parent=parent, placeholder=placeholder)
        self._commands = {}
        self._dropdowns = {}

        self._title = "Command"
        self.setWindowTitle(f"{self._title} Directory")

        self._mainTable.setColumnCount(5)
        self._mainTable.setHorizontalHeaderItem(3, QTableWidgetItem("Action"))
        self._mainTable.setHorizontalHeaderItem(4, QTableWidgetItem("Action2"))
    
    def _add_table_item(self, item: "AbstractDirectoryView.ViewTile") -> None:
        dropdown = QComboBox()
        dropdown.addItems(self._options)
        dropdown.setCurrentIndex(self._options.index(
            self._commands[item._num]["action"]))
        dropdown.currentIndexChanged.connect(lambda actnum, num=item._num: self.doaction(actnum, num))
        dropdown2 = QComboBox()
        dropdown2.addItems(self._options)
        dropdown2.setCurrentIndex(self._options.index(
            self._commands[item._num]["action2"]))
        dropdown2.currentIndexChanged.connect(
            lambda actnum, num=item._num: self.doaction2(actnum, num))
        self._mainTable.setCellWidget(item._num-1, 3, dropdown)
        self._mainTable.setCellWidget(item._num-1, 4, dropdown2)
        self._dropdowns[item._num] = (dropdown, dropdown2)
        return super()._add_table_item(item)
    
    def addCommand(self, num: int, action: 'Union[State, Cuelist]', actionnum: int, name: str, color: Optional['QColor'] = None) -> None:
        if isinstance(action, Cuelist):
            self._commands[num] = {
                "action": "Go",
                "action2": "Pause",
                "type": "cuelist",
                "object": action,
                "objectnum": actionnum
            }
        else:
            self._commands[num] = {
                "action": "Toggle",
                "action2": "Flash",
                "type": "state",
                "object": action,
                "objectnum": actionnum
            }
        item = self.ViewTile(num, name, color)
        item.selected.connect(lambda num: self._handle_TileClick(num))
        item.right_click.connect(lambda num: self._handle_RightClick(num))
        self.setItem(num, item)
    
    def getCommand(self, num: int) -> Optional[dict]:
        return self._commands.get(num)

    def doaction(self, actnum: int, num: int):
        self._commands[num]["action"] = self._options[actnum]
    
    def doaction2(self, actnum: int, num: int):
        self._commands[num]["action2"] = self._options[actnum]

    def _handle_TileClick(self, num: int) -> None:
        if not self._guard_mode:
            self.command_selected.emit(num, self._commands.get(num))
    
    def _handle_RightClick(self, num: int):
        if not self._guard_mode:
            self.command_right_click.emit(num, self._commands.get(num))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = CommandDirectoryView()
    window.show()
    window.tile_selected.connect(lambda num: print(f"Tile {num} selected"))
    window.command_selected.connect(lambda num, cuelist: print(f"{cuelist} at {num} selected"))
    sys.exit(app.exec_())
