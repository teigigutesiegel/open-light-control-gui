from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QToolBar, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from OpenLightControlGui import AbstractDirectoryView

from typing import Optional

class PalletteDirectoryView(AbstractDirectoryView):
    _I: QLabel
    _P: QLabel
    _C: QLabel
    _B: QLabel
    _E: QLabel
    _T: QLabel
    _L: QLabel

    DirectoryTypes = {
        "I": "Intensity",
        "P": "Position",
        "C": "Color",
        "B": "Beam",
        "E": "Effects",
        "T": "Time",
        "L": "Control"
    }

    def __init__(self, title: Optional[str] = None, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__(parent=parent, placeholder=placeholder)

        self._title = title
        self.setWindowTitle(f"{self._title} Directory")

        self._mainTable.setColumnCount(4)
        self._mainTable.setHorizontalHeaderItem(3, QTableWidgetItem("Kind"))

        kindToolbar = QToolBar()
        kindwid = QWidget()
        kindlay = QGridLayout()
        kindlay.setSpacing(0)
        kindlay.setContentsMargins(0, 0, 0, 0)
        for i, key in enumerate(self.DirectoryTypes.keys()):
            lab = QLabel(key)
            font = lab.font()
            font.setPointSize(8)
            lab.setFont(font)
            if self.DirectoryTypes.get(key, "") == title:
                lab.setStyleSheet("background-color: #00f; color: #fff")
            else:
                lab.setStyleSheet(lab.styleSheet() + "color: #fff")
            lab.setAlignment(Qt.AlignCenter)
            lab.setFixedSize(15, 15)
            setattr(self, f"_{key}", lab)
            kindlay.addWidget(lab, i//4, i%4)
        
        kindwid.setLayout(kindlay)
        kindToolbar.addWidget(kindwid)
        self.addToolBar(kindToolbar)
    
    def _add_table_item(self, item: "ViewTile") -> None:
        wid = QTableWidgetItem(item._getdirIndicator())
        wid.setFlags(Qt.ItemIsEnabled)
        self._mainTable.setItem(item._num-1, 3, wid)
        return super()._add_table_item(item)

    class ViewTile(AbstractDirectoryView.ViewTile):
        _dirIndicator: QLabel
        hasIntensity = False
        hasPosition = False
        hasColor = False
        hasBeam = False
        hasEffects = False
        hasTime = False
        hasControl = False

        def __init__(self, num: int, title: Optional[str] = None, color: Optional[QColor] = None, fullColor: bool = False) -> None:
            super().__init__(num, title, color, fullColor)
            self._num = num
            if title:
                self._title = title
                self._active = True
            self._fullColor = fullColor

            if title:
                self._dirIndicator = QLabel(self._getdirIndicator())
                self._dirIndicator.setAlignment(Qt.AlignRight)
                self._headerLay.addWidget(self._dirIndicator)
                font = self._dirIndicator.font()
                font.setPointSize(7)
                self._dirIndicator.setFont(font)

        def _getdirIndicator(self) -> str:
            ret_str = ""
            if self.hasIntensity:
                ret_str += "I"
            else:
                ret_str += "."
            if self.hasPosition:
                ret_str += "P"
            else:
                ret_str += "."
            if self.hasColor:
                ret_str += "C"
            else:
                ret_str += "."
            if self.hasBeam:
                ret_str += "B"
            else:
                ret_str += "."
            if self.hasEffects:
                ret_str += "E"
            if self.hasTime:
                ret_str += "T"
            if self.hasControl:
                ret_str += "L"
            return ret_str

        def recalc(self):
            self._dirIndicator.setText(self._getdirIndicator())

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = PalletteDirectoryView()
    if False:
        from random import randint
        for i in range(20):
            num_ = randint(1, window._placeholder)
            window.setItem(num_, window.ViewTile(
                num_, f"test - {num_}", QColor.fromRgb(randint(0, 255), randint(0, 255), randint(0, 255))))
    window.show()
    sys.exit(app.exec_())
