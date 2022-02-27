from PyQt5.QtWidgets import QInputDialog, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, QScrollArea, QStackedLayout, QToolBar, QPushButton, QHeaderView, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QApplication
from PyQt5.QtGui import QIcon, QColor, QMouseEvent
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QTimer

from OpenLightControlGui import FlowLayout

from typing import Dict, Optional
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
    _items: 'Dict[int, ViewTile]'
    _guard_mode: bool
    _mainToolbar: QToolBar
    _guardbut: QPushButton
    _tablebut: QPushButton
    _lightbut: QPushButton
    _viewTileSize: int = 75
    _placeholder: int

    tile_selected = pyqtSignal(int)

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        self._placeholder = placeholder
        super().__init__(parent=parent)
        self._items = {}
        self._guard_mode = False

        self._mainGrid = FlowLayout(margin=0, spacing=0)
        self._mainTable = QTableWidget(self._placeholder, 3)
        self._mainTable.setHorizontalHeaderLabels(["Name", "Color", "Comment"])
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
        self._guardbut.clicked.connect(self._toggle_guard) # type: ignore
        self._tablebut = QPushButton()
        self._tablebut.setIconSize(QSize(30, 30))
        self._tablebut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/table.svg")))
        self._tablebut.clicked.connect(self._toggle_table) # type: ignore
        self._lightbut = QPushButton()
        self._lightbut.setIconSize(QSize(30, 30))
        self._lightbut.setIcon(
            QIcon(os.path.join(basepath, "../../assets/icons/lighttable.svg")))
        self._lightbut.clicked.connect(self._toggle_full_color) # type: ignore
        self._mainToolbar.addWidget(self._guardbut)
        self._mainToolbar.addWidget(self._tablebut)
        self._mainToolbar.addWidget(self._lightbut)
        self._guardbut.setFixedHeight(36)
        self.addToolBar(self._mainToolbar)

    def _fill_grid(self):
        for i in range(self._placeholder):
            item = self.ViewTile(i+1)
            item.selected.connect(self._handle_click)
            item.right_click.connect(self._handle_right_click)
            self._mainGrid.addWidget(item)
            self._mainTable.setRowHidden(i, True)
    
    def _handle_click(self, num: int):
        if self._guard_mode:
            self.tile_selected.emit(num)
    
    def _handle_right_click(self, num: int):
        item = self.getItem(num)
        if item is not None:
            if self._guard_mode and item._active:
                text, ok = QInputDialog.getText(self, 'change name', 'New Name:', text=item.title)
                if ok:
                    item.title = text

    def getItem(self, pos: int) -> 'Optional[ViewTile]':
        return self._items.get(pos)
    
    def getItems(self) -> 'Dict[int, ViewTile]':
        return self._items

    def setItem(self, pos: int, item: "ViewTile") -> None:
        self._items[pos] = item
        self._add_table_item(item)
        old_wid: QWidget = self._mainGrid.itemAt(pos-1).widget() # typing: ignore
        self._mainGrid.removeWidget(old_wid)
        old_wid.deleteLater()
        self._mainGrid.insertWidget(pos-1, item)
        item.selected.connect(self._handle_click)
        item.right_click.connect(self._handle_right_click)

    def _add_table_item(self, item: "ViewTile") -> None:
        wid = QTableWidgetItem(str(item.title))
        self._mainTable.setItem(item._num-1, 0, wid)
        col = item.getColor()
        if col is not None:
            colwid = QTableWidgetItem()
            colwid.setBackground(col)
            colwid.setFlags(Qt.ItemIsEnabled) # type: ignore
            self._mainTable.setItem(item._num-1, 1, colwid)
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

    def setItems(self, dic: 'Dict[int, ViewTile]') -> None:
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
        _color: Optional[QColor] = None
        _fullColor: bool = False
        _mainVLay: QVBoxLayout
        _headerLay: QHBoxLayout
        _numLabel: QLabel
        _mainLabel: QLabel
        _mainLay: QVBoxLayout
        _mainWidget: QWidget
        _last_click: str = ""

        selected = pyqtSignal(int)
        double_click = pyqtSignal(int)
        right_click = pyqtSignal(int)

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

            self._mainLabel = QLabel(self.title)
            pol = QSizePolicy()
            pol.setVerticalPolicy(QSizePolicy.Expanding)
            pol.setHorizontalPolicy(QSizePolicy.Expanding)
            self._mainLabel.setSizePolicy(pol)
            self._mainLabel.setAlignment(Qt.AlignTop) # type: ignore
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
                self.setColor(color)
            else:
                self.clearColor()
            self.setFixedSize(AbstractDirectoryView._viewTileSize,
                              AbstractDirectoryView._viewTileSize)
            # self.released.connect(lambda: self.selected.emit(self._num))

        def setActive(self, active: bool) -> None:
            if active:
                self.setStyleSheet(
                    self.styleSheet() + "QWidget { color: #fff; background-color: #3a3a3a }")
            else:
                self.setStyleSheet(self.styleSheet() +
                                   "QWidget { color: #d3d3d3 }")

        def setFullColor(self, fullColor: bool) -> None:
            self._fullColor = fullColor
            col = self.getColor()
            if col:
                self.clearColor()
                self.setColor(col)

        def setColor(self, color: QColor) -> None:
            self._color = color
            if self._fullColor:
                col = self.getColor()
                if col is not None:
                    self.setStyleSheet(
                        "QWidget { " + "background-color: rgb({0:d}, {1:d}, {2:d})".format(*color.getRgb()) + " }")
                    if col.getHsvF()[2] >= 0.5:
                        self.setStyleSheet(
                            self.styleSheet() + "QWidget { color:#000}")
                else:
                    self.clearColor()
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

        def getColor(self) -> Optional[QColor]:
            if self._color:
                return self._color
            else:
                return None

        def clearColor(self) -> None:
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

        @property
        def title(self) -> str:
            return self._title
        
        @title.setter
        def title(self, name: str) -> None:
            self._title = name
            self._mainLabel.setText(name)

        def getTitle(self) -> str:
            return self.title

        def setTitle(self, name: str) -> None:
            self.title = name

        def mousePressEvent(self, e: QMouseEvent) -> None:
            if e.button() == Qt.MouseButton.RightButton:
                self._last_click = ""
                self.right_click.emit(self._num)
            elif e.button() == Qt.MouseButton.LeftButton:
                if self._last_click == "":
                    self._last_click = "Left"
            else:
                return super().mousePressEvent(e)
        
        def mouseReleaseEvent(self, e: QMouseEvent) -> None:
            if self._last_click == "Double":
                self._last_click = ""
                self.double_click.emit(self._num)
            else:
                QTimer.singleShot(QApplication.doubleClickInterval(), self._single_click)
            return super().mouseReleaseEvent(e)

        def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
            self._last_click = "Double"
            return super().mouseDoubleClickEvent(e)

        def _single_click(self):
            if self._last_click == "Left":
                self._last_click = ""
                self.selected.emit(self._num)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = AbstractDirectoryView()
    window.show()
    sys.exit(app.exec_())
