from OpenLightControlGui.model import Cuelist

from typing import Optional

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor


class CuelistView(QMainWindow):
    _mainTable: QTableWidget
    _mainWid: QWidget
    _num: int
    _cuelist: Cuelist

    tile_selected = pyqtSignal(int)

    def __init__(self, num: int, cuelist: Cuelist, parent: Optional['QWidget'] = None) -> None:
        self._num = num
        self._cuelist = cuelist
        super().__init__(parent=parent)
        self.setWindowTitle(f"#{self._num} Cuelist - {self._cuelist.name}")

        self._mainTable = QTableWidget(0, 4)
        self._mainTable.setHorizontalHeaderLabels(["Num", "Name", "Duration", "Fade"])
        self._mainTable.setStyleSheet("color: #fff")
        self.setCentralWidget(self._mainTable)

        self._populateTable()
        self._mainTable.itemChanged.connect(self._handle_item_change) # type: ignore
        self._cuelist.currentCueChanged.connect(self.my_update)

        self._mainToolbar = QToolBar()
        self._renumbut = QPushButton("Renumber")
        self._renumbut.clicked.connect(self._renumber) # type: ignore
        self._mainToolbar.addWidget(self._renumbut)
        self._renumbut.setFixedHeight(36)
        self.addToolBar(self._mainToolbar)
    
    def _renumber(self):
        self._mainTable.itemChanged.disconnect(self._handle_item_change)
        for i, cue in enumerate(self._cuelist):
            cue.num = i + 1
        self._clear_table()
        self._populateTable()
        self._mainTable.itemChanged.connect(self._handle_item_change)

    def _populateTable(self):
        self._mainTable.setRowCount(len(self._cuelist))
        for x, cue in enumerate(self._cuelist):
            wid = QTableWidgetItem(str(cue.num))
            self._mainTable.setItem(x, 0, wid)
            wid = QTableWidgetItem(str(cue.name))
            self._mainTable.setItem(x, 1, wid)
            wid = QTableWidgetItem(str(cue.duration))
            self._mainTable.setItem(x, 2, wid)
            wid = QTableWidgetItem(str(cue.fade))
            self._mainTable.setItem(x, 3, wid)
            self._resize_table()
        self.my_update()

    def _handle_item_change(self, item: 'QTableWidgetItem'):
        row = self._mainTable.row(item)
        col = self._mainTable.column(item)
        cue = self._cuelist[row]

        if col == 0:
            if str(cue.num) == item.text():
                return
            num = float(item.text())
            self._cuelist.removeCue(row)
            num_ord = 0
            for num_ord, cue_i in enumerate(self._cuelist):
                if cue_i.num is not None and cue_i.num > num:
                    break
            self._cuelist.addCue(cue, num_ord)
            cue.num = num if num != int(num) else int(num)
            self._mainTable.itemChanged.disconnect(self._handle_item_change) # type: ignore
            self._clear_table()
            self._populateTable()
            self._mainTable.itemChanged.connect(self._handle_item_change) # type: ignore
        elif col == 1:
            cue.name = item.text()
        elif col == 2:
            try:
                val = int(item.text())
                cue.duration = val if val > 0 else 0
            except ValueError:
                item.setText(str(cue.duration))
        elif col == 3:
            try:
                val = int(item.text())
                cue.fade = val if val >= 0 else None
            except ValueError:
                item.setText(str(cue.fade))

    # def setFadeStarted(self, from_: int, to: int):
    #     self._mainTable.item(from_, 0).setForeground(QColor(255, 80, 0))
    #     self._mainTable.item(to, 0).setForeground(QColor(255, 160, 0))
    
    def my_update(self):
        for row in range(self._mainTable.rowCount()):
            self._mainTable.item(row, 0).setForeground(QColor(255, 255, 255))
        if self._cuelist.isRunning():
            if self._cuelist.isPaused():
                self._mainTable.item(self._cuelist.currCue, 0).setForeground(QColor(255, 80, 0))
            else:
                self._mainTable.item(self._cuelist.currCue, 0).setForeground(QColor(0, 255, 0))

    def _clear_table(self) -> None:
        for _ in range(self._mainTable.rowCount()):
            self._mainTable.removeRow(0)

    def _resize_table(self) -> None:
        self._mainTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._mainTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
