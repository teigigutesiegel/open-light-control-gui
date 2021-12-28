from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class HiddenSpinBox(QWidget):
    _stack: QStackedLayout
    _blank: QPushButton
    _spin: QSpinBox

    valueChanged = pyqtSignal(int)

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent=parent)

        self._stack = QStackedLayout(self)
        
        self._blank = QPushButton()
        self._blank.setStyleSheet("QPushButton { border-radius: 0px; border: 1px solid black }")
        self._blank.pressed.connect(lambda: self._stack.setCurrentIndex(1))
        self._stack.addWidget(self._blank)
        self._spin = QSpinBox()
        self._spin.valueChanged.connect(lambda num: self.valueChanged.emit(num))
        self._spin.valueChanged.connect(self._check_display)
        self._spin.installEventFilter(self)
        self._stack.addWidget(self._spin)

        self.setLayout(self._stack)
    
    def eventFilter(self, source, event):
        if (event.type() == QEvent.FocusOut and source is self._spin):
            self._check_display()
        return super(HiddenSpinBox, self).eventFilter(source, event)
    
    def _check_display(self) -> None:
        if self._spin.value() == 0:
            self._stack.setCurrentIndex(0)
        else:
            self._stack.setCurrentIndex(1)
    
    def setValue(self, val: int) -> None:
        self._spin.setValue(val)
    
    def value(self) -> int:
        return self._spin.value()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = HiddenSpinBox()
    window.show()
    sys.exit(app.exec_())
