from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenLightControlGui.components.Colorpicker import ColorCircle
from OpenLightControlGui.components.AspectLayout import AspectLayout
from OpenLightControlGui.components.PalletteDirectoryView import PalletteDirectoryView

import sys
from typing import Optional
import os
basepath = os.path.dirname(__file__)

class ColorDirectoryView(PalletteDirectoryView):
    _colorToolbar: QToolBar
    _colorbut: QPushButton

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        self._title = "Colour"
        super().__init__(parent=parent)

        self._c.setStyleSheet("background-color: #00f; color: #fff")

        self._colorToolbar = QToolBar()
        self._colorbut = QPushButton()
        self._colorbut.setIconSize(QSize(30, 30))
        self._colorbut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/color-management.svg")))
        self._colorbut.clicked.connect(self._openColorCircle)
        self._colorToolbar.addWidget(self._colorbut)
        self.insertToolBar(self._mainToolbar, self._colorToolbar)

    def _openColorCircle(self) -> None:
        lay = AspectLayout(1)
        col = ColorCircle()
        lay.addWidget(col)
        wid = QWidget()
        wid.setLayout(lay)
        win = QMainWindow(self)
        win.setCentralWidget(wid)
        win.setWindowTitle("Colour Picker")
        win.setGeometry(0, 0, 500, 500)
        win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ColorDirectoryView()
    window.show()
    sys.exit(app.exec_())
