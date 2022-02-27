# pyright: reportGeneralTypeIssues=false
from typing import Optional
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QMouseEvent, QPaintEvent
from PyQt5.QtCore import pyqtSignal, Qt

class XY_Pad(QWidget):
    px: int
    py: int
    _height: int
    _width: int
    position_changed = pyqtSignal(float, float)

    def __init__(self, parent: Optional[QWidget] = None):
        super(XY_Pad, self).__init__(parent)
        self.on_wid = False
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(self.p)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)
        self.px = -1
        self.py = -1
        self._height = self.size().height()
        self._width = self.size().width()
        self.setMouseTracking(True)

    def paintEvent(self, a0: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.MouseDraw(qp)
        qp.end()

    def MouseDraw(self, qp: QPainter):
        pen= QPen(Qt.red, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.px,0,self.px,self._height)
        qp.drawLine(0,self.py,self._width,self.py)

    def drawLines(self, qp: QPainter):
        pen = QPen(Qt.lightGray, 2, Qt.SolidLine)
        qp.setPen(pen)
        size=self.size()
        qp.drawLine(0, int(size.height()/2), size.width(), int(size.height()/2))
        qp.drawLine(int(size.width()/2), 0, int(size.width()/2), size.height())

    def mousePressEvent(self, a0: QMouseEvent):
        if a0.button() == Qt.LeftButton:
            self.lastPoint = a0.pos()
            self.on_wid = True

    def mouseMoveEvent(self, a0: QMouseEvent):
        self.px = a0.pos().x()
        self.py = a0.pos().y()
        self._height = self.size().height()
        self._width = self.size().width()
        if (a0.buttons() & Qt.LeftButton) and self.on_wid:
            if ((self.px >= 0) and (self.py >= 0)) and ((self.px <= self._width) and self.py <= self._height):
                self.position_changed.emit(self.px/self._width,self.py/self._height)
        self.update()

    def mouseReleaseEvent(self, a0: QMouseEvent):
        self.px = a0.pos().x()
        self.py = a0.pos().y()
        self._height = self.size().height()
        self._width = self.size().width()
        if a0.button() == Qt.LeftButton and self.on_wid:
            if ((self.px >= 0) and (self.py >= 0)) and ((self.px <= self._width) and self.py <= self._height):
                self.position_changed.emit(self.px/self._width,self.py/self._height)
            self.on_wid = False


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    window = XY_Pad()
    window.position_changed.connect(lambda x, y: print(x, y))
    window.show()
    sys.exit(app.exec_())
