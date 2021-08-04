from PyQt5.QtWidgets import QWidget, QPushButton, QToolBar, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from OpenLightControlGui import ColorCircle
from OpenLightControlGui import AspectLayout
from OpenLightControlGui import PalletteDirectoryView

from typing import Optional
import os
basepath = os.path.dirname(__file__)

class ColorDirectoryView(PalletteDirectoryView):
    _colorToolbar: QToolBar
    _colorbut: QPushButton

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__("Color", parent=parent)

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
