from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenLightControlGui.components.FlowLayout import FlowLayout

import sys
from typing import Optional
from numbers import Number
import os
basepath = os.path.dirname(__file__)


class AbstractDirectoryView(QMainWindow):
    _title: str = ""
    _mainStack: QStackedLayout
    _mainGrid: FlowLayout
    _gridWid: QWidget
    _mainTable: QTableWidget
    _scrollArea: QScrollArea
    _mainWid: QWidget
    _items: 'dict[int, ViewTile]'
    _guard_mode: bool
    _mainToolbar: QToolBar
    _guardbut: QPushButton
    _tablebut: QPushButton
    _lightbut: QPushButton
    DirectoryTypes = {
        "I": "Intensity",
        "P": "Position",
        "C": "Colour",
        "B": "Beam",
        "E": "Effects",
        "T": "Time",
        "L": "Control"
    }
    _viewTileSize: Number = 75
    _placeholder: int = 1000

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent=parent)
        self._items = {}
        self._guard_mode = False

        self.setWindowTitle(f"{self._title} Directory")

        self._mainGrid = FlowLayout(margin=0, spacing=0)
        self._mainTable = QTableWidget(self._placeholder, 4)
        self._mainTable.setHorizontalHeaderLabels(
            ["Name", "Colour", "Comment", "Kind"])
        self._mainTable.setStyleSheet("color: #fff")

        self._fill_grid()

        self._mainStack = QStackedLayout()
        self._gridWid = QWidget()
        self._gridWid.setLayout(self._mainGrid)
        self._scrollArea = QScrollArea()
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setWidget(self._gridWid)
        self._mainStack.addWidget(self._scrollArea)
        self._mainStack.addWidget(self._mainTable)
        self._mainWid = QWidget()
        self._mainWid.setLayout(self._mainStack)
        self.setCentralWidget(self._mainWid)

        self.setGeometry(0, 0, 500, 300)
        self.setStyleSheet("""
        QWidget {
            background: #282828;
        }
        QPushButton {
            color: #fff;
        }
        QPushButton:pressed,
        QPushButton:hover,
        QPushButton:checked {
            color: #000;
            background-color: rgb(0,0,255);
        }""")

        self._mainToolbar = QToolBar()
        self._guardbut = QPushButton("Guard")
        self._guardbut.clicked.connect(self._toggle_guard)
        self._tablebut = QPushButton()
        self._tablebut.setIconSize(QSize(30, 30))
        self._tablebut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/table.svg")))
        self._tablebut.clicked.connect(self._toggle_table)
        self._lightbut = QPushButton()
        self._lightbut.setIconSize(QSize(30, 30))
        self._lightbut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/lighttable.svg")))
        self._lightbut.clicked.connect(self._toggle_full_color)
        self._mainToolbar.addWidget(self._guardbut)
        self._mainToolbar.addWidget(self._tablebut)
        self._mainToolbar.addWidget(self._lightbut)
        self._guardbut.setFixedHeight(36)
        self.addToolBar(self._mainToolbar)

    def _fill_grid(self):
        for i in range(self._placeholder):
            item = self.ViewTile(i+1)
            self._mainGrid.addWidget(item)
            self._mainTable.setRowHidden(i, True)

    def getItem(self, pos: int) -> Optional[object]:
        return self._items.get(pos)

    def setItem(self, pos: int, item: "ViewTile") -> None:
        self._items[pos] = item
        self._add_table_item(item)
        self._mainGrid.removeWidget(self._mainGrid.itemAt(pos-1).widget())
        self._mainGrid.insertWidget(pos-1, item)
        item.clicked.connect(lambda x, num=item._num: print(f"pressed {num}"))
        # self._mainGrid.replaceWidget(self._mainGrid.itemAt(pos-1).widget(), self.ViewTile(pos+1, item.name, item.getColor()))

    def _add_table_item(self, item: "ViewTile") -> None:
        wid = QTableWidgetItem(str(item._title))
        self._mainTable.setItem(item._num-1, 0, wid)
        if item.getColour():
            colwid = QTableWidgetItem()
            colwid.setBackground(item.getColour())
            colwid.setFlags(Qt.ItemIsEnabled)
            self._mainTable.setItem(item._num-1, 1, colwid)
        wid = QTableWidgetItem(item._getdirIndicator())
        wid.setFlags(Qt.ItemIsEnabled)
        self._mainTable.setItem(item._num-1, 3, wid)
        self._mainTable.setRowHidden(item._num-1, False)
        self._resize_table()

    def _remove_table_item(self, pos: int) -> None:
        self._mainTable.removeCellWidget(pos-1, 0)
        self._mainTable.removeCellWidget(pos-1, 1)
        self._mainTable.removeCellWidget(pos-1, 2)
        self._mainTable.removeCellWidget(pos-1, 3)
        self._mainTable.setRowHidden(pos-1, True)

    def isInGuardMode(self) -> bool:
        return self._guard_mode

    def setGuardMode(self, guard_mode: bool) -> None:
        self._guard_mode = guard_mode

    def removeItem(self, pos: int) -> None:
        self._mainGrid.removeWidget(self._mainGrid.itemAt(pos-1).widget())
        self._remove_table_item(pos)
        del self._items[pos]

    def setItems(self, dic: 'dict[int, object]') -> None:
        for pos, item in dic.items():
            self.setItem(pos, item)

    def _toggle_guard(self) -> None:
        if self._guardbut.isCheckable():
            self._guardbut.setChecked(False)
            self._guardbut.setCheckable(False)
            self._guard_mode = False
        else:
            self._guardbut.setCheckable(True)
            self._guardbut.setChecked(True)
            self._guard_mode = True

    def _toggle_table(self) -> None:
        if self._mainStack.currentIndex() == 0:
            self._mainStack.setCurrentIndex(1)
            self._tablebut.setCheckable(True)
            self._tablebut.setChecked(True)
        else:
            self._mainStack.setCurrentIndex(0)
            self._tablebut.setChecked(False)
            self._tablebut.setCheckable(False)

    def _toggle_full_color(self) -> None:
        if self._lightbut.isCheckable():
            for item in self._items.values():
                item.setFullColor(False)
            self._lightbut.setChecked(False)
            self._lightbut.setCheckable(False)
        else:
            for item in self._items.values():
                item.setFullColor(True)
            self._lightbut.setCheckable(True)
            self._lightbut.setChecked(True)

    def _resize_table(self) -> None:
        self._mainTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self._mainTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

    class ViewTile(QPushButton):
        _title: str = ""
        _num: int
        _active: bool = False
        _color: QColor
        _fullColor: bool = False
        _mainVLay: QVBoxLayout
        _headerLay: QHBoxLayout
        _numLabel: QLabel
        _mainLabel: QLabel
        _mainLay: QVBoxLayout
        _mainWidget: QWidget

        def __init__(self, num: int, title: Optional[str] = None, color: Optional[QColor] = None, fullColor: bool = False) -> None:
            super().__init__()
            self._num = num
            if title:
                self._title = title
                self._active = True
            self._fullColor = fullColor

            self._mainVLay = QVBoxLayout()
            self._headerLay = QHBoxLayout()
            self._numLabel = QLabel(str(self._num))
            self._headerLay.addWidget(self._numLabel)
            self._mainVLay.addLayout(self._headerLay)

            self._mainLabel = QLabel(self._title)
            pol = QSizePolicy()
            pol.setVerticalPolicy(QSizePolicy.Expanding)
            pol.setHorizontalPolicy(QSizePolicy.Expanding)
            self._mainLabel.setSizePolicy(pol)
            self._mainLabel.setAlignment(Qt.AlignTop)
            self._mainLabel.setWordWrap(True)

            font = self._numLabel.font()
            font.setPointSize(7)
            self._numLabel.setFont(font)
            self._mainLabel.setFont(font)

            self._mainVLay.addWidget(self._mainLabel)
            self._mainVLay.setSpacing(0)
            self._mainWidget = QWidget()
            self._mainWidget.setLayout(self._mainVLay)
            self._mainLay = QVBoxLayout()
            self._mainLay.addWidget(self._mainWidget)
            self._mainLay.setContentsMargins(0, 0, 0, 0)
            self._mainLay.setSpacing(0)
            self.setLayout(self._mainLay)

            if color:
                self.setColour(color)
            else:
                self.clearColour()
            self.setFixedSize(AbstractDirectoryView._viewTileSize,
                              AbstractDirectoryView._viewTileSize)

        def setActive(self, active: bool) -> None:
            if active:
                self.setStyleSheet(
                    self.styleSheet() + "QWidget { color: #fff; background-color: #3a3a3a }")
            else:
                self.setStyleSheet(self.styleSheet() +
                                   "QWidget { color: #d3d3d3 }")

        def setFullColor(self, fullColor: bool) -> None:
            self._fullColor = fullColor
            col = self.getColour()
            if col:
                self.clearColour()
                self.setColour(col)

        def setColour(self, color: QColor) -> None:
            self._color = color
            if self._fullColor:
                if self.getColour():
                    self.setStyleSheet(
                        "QWidget { " + "background-color: rgb({0:d}, {1:d}, {2:d})".format(*color.getRgb()) + " }")
                    if self.getColour().getHsvF()[2] >= 0.5:
                        self.setStyleSheet(
                            self.styleSheet() + "QWidget { color:#000}")
                else:
                    self.clearColour()
            else:
                self.setStyleSheet("""
                QWidget {"""+"border: 2px solid rgb({0:d}, {1:d}, {2:d});".format(*color.getRgb()) +
                                   """
                    border-radius: 5px;
                }
                QLabel {
                    border: 0px;
                    border-radius: 0px;
                }
                """)
                self.setActive(self._active)

        def getColour(self) -> Optional[QColor]:
            if self._color:
                return self._color
            else:
                return None

        def clearColour(self) -> None:
            self._color = None
            self.setStyleSheet("""
            QWidget {
                border: 1px solid #000;
                border-radius: 0px;
                background: #282828;
            }
            QLabel {
                 border: 0px;
                 border-radius: 0px;
            }
            """)
            self.setActive(self._active)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AbstractDirectoryView()
    window.show()
    sys.exit(app.exec_())
