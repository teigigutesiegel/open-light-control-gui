from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .AbstractDirectoryView import AbstractDirectoryView

import sys
from typing import Optional
from random import randint


class PalletteDirectoryView(AbstractDirectoryView):

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent=parent)

        kindToolbar = QToolBar()
        kindwid = QWidget()
        kindlay = QGridLayout()
        kindlay.setSpacing(0)
        kindlay.setContentsMargins(0, 0, 0, 0)
        i = QLabel("I")
        p = QLabel("P")
        c = QLabel("C")
        c.setStyleSheet("background-color: #00f;")
        b = QLabel("B")
        kindlay.addWidget(i, 0, 0)
        kindlay.addWidget(p, 0, 1)
        kindlay.addWidget(c, 0, 2)
        kindlay.addWidget(b, 0, 3)
        e = QLabel("E")
        t = QLabel("T")
        l = QLabel("L")
        kindlay.addWidget(e, 1, 0)
        kindlay.addWidget(t, 1, 1)
        kindlay.addWidget(l, 1, 2)
        kindwid.setLayout(kindlay)
        kindToolbar.addWidget(kindwid)
        font = i.font()
        font.setPointSize(8)
        for lab in [i, p, c, b, e, t, l]:
            lab.setFont(font)
            lab.setStyleSheet(lab.styleSheet() + "color: #fff")
            # lab.setMargin(1)
            lab.setAlignment(Qt.AlignCenter)
            lab.setFixedSize(15, 15)
        self.addToolBar(kindToolbar)

        self._fill_grid_rand()

    def _fill_grid_rand(self, num=20):
        """for testing only"""
        for i in range(num):
            num_ = randint(1, self._placeholder)
            self.setItem(num_, self.ViewTile(
                num_, f"test - {num_}", QColor.fromRgb(randint(0, 255), randint(0, 255), randint(0, 255))))

    class ViewTile(AbstractDirectoryView.ViewTile):
        _dirIndicator: QLabel

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

        def hasIntensity(self) -> bool:
            return False

        def hasPosition(self) -> bool:
            return False

        def hasColour(self) -> bool:
            return True

        def hasBeam(self) -> bool:
            return False

        def hasEffects(self) -> bool:
            return False

        def hasTime(self) -> bool:
            return False

        def hasControl(self) -> bool:
            return False

        def _getdirIndicator(self) -> str:
            ret_str = ""
            if self.hasIntensity():
                ret_str += "I"
            else:
                ret_str += "."
            if self.hasPosition():
                ret_str += "P"
            else:
                ret_str += "."
            if self.hasColour():
                ret_str += "C"
            else:
                ret_str += "."
            if self.hasBeam():
                ret_str += "B"
            else:
                ret_str += "."
            if self.hasEffects():
                ret_str += "E"
            if self.hasTime():
                ret_str += "T"
            if self.hasControl():
                ret_str += "L"
            return ret_str


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AbstractDirectoryView()
    window.show()
    sys.exit(app.exec_())
