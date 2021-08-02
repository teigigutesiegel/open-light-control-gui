from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenLightControlGui.components.AbstractDirectoryView import AbstractDirectoryView

import sys
from typing import Optional
from random import randint


class PalletteDirectoryView(AbstractDirectoryView):
    _i: QLabel
    _p: QLabel
    _c: QLabel
    _b: QLabel
    _e: QLabel
    _t: QLabel
    _l: QLabel

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent=parent)

        kindToolbar = QToolBar()
        kindwid = QWidget()
        kindlay = QGridLayout()
        kindlay.setSpacing(0)
        kindlay.setContentsMargins(0, 0, 0, 0)
        self._i = QLabel("I")
        self._p = QLabel("P")
        self._c = QLabel("C")
        self._b = QLabel("B")
        kindlay.addWidget(self._i, 0, 0)
        kindlay.addWidget(self._p, 0, 1)
        kindlay.addWidget(self._c, 0, 2)
        kindlay.addWidget(self._b, 0, 3)
        self._e = QLabel("E")
        self._t = QLabel("T")
        self._l = QLabel("L")
        kindlay.addWidget(self._e, 1, 0)
        kindlay.addWidget(self._t, 1, 1)
        kindlay.addWidget(self._l, 1, 2)
        kindwid.setLayout(kindlay)
        kindToolbar.addWidget(kindwid)
        font = self._i.font()
        font.setPointSize(8)
        for lab in [self._i, self._p, self._c, self._b, self._e, self._t, self._l]:
            lab.setFont(font)
            lab.setStyleSheet(lab.styleSheet() + "color: #fff")
            # lab.setMargin(1)
            lab.setAlignment(Qt.AlignCenter)
            lab.setFixedSize(15, 15)
        self.addToolBar(kindToolbar)

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

    window = PalletteDirectoryView()
    window.show()
    sys.exit(app.exec_())
