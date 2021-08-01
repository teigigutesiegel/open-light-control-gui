from typing import Optional
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRect
from PyQt5.QtGui import QColor, QResizeEvent, QPaintEvent, QPainter, QConicalGradient, QRadialGradient, QMouseEvent

import numpy as np
import sys

from .AspectLayout import AspectLayout


class ColorCircle(QWidget):
    px: float
    py: float
    h: float
    s: float
    v: float
    currentColorChanged = pyqtSignal(QColor)

    def __init__(self, parent: Optional[QWidget] = None, startupcolor: 'list[int]' = [255, 255, 255], margin: int = 10) -> None:
        super().__init__(parent=parent)
        self.radius = 0
        self.selected_color = QColor(
            startupcolor[0], startupcolor[1], startupcolor[2], 1)
        self.px = 0.5
        self.py = 0.5
        self.h = self.selected_color.hueF()
        self.s = self.selected_color.saturationF()
        self.v = self.selected_color.valueF()
        self.margin = margin

        qsp = QSizePolicy(QSizePolicy.Preferred,
                          QSizePolicy.Preferred)
        qsp.setHeightForWidth(True)
        self.setSizePolicy(qsp)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.radius = min([self.width()/2, self.height()/2])

    def paintEvent(self, a0: QPaintEvent) -> None:
        center = QPointF(self.width()/2, self.height()/2)
        p = QPainter(self)
        p.setViewport(self.margin, self.margin, self.width() -
                      2*self.margin, self.height()-2*self.margin)
        hsv_grad = QConicalGradient(center, 90)
        for deg in range(360):
            col = QColor.fromHsvF(deg / 360, 1, self.v)
            hsv_grad.setColorAt(deg / 360, col)

        val_grad = QRadialGradient(center, self.radius)
        val_grad.setColorAt(0.0, QColor.fromHsvF(0.0, 0.0, self.v, 1.0))
        val_grad.setColorAt(1.0, Qt.transparent)

        p.setPen(Qt.transparent)
        p.setBrush(hsv_grad)
        p.drawEllipse(self.rect())
        p.setBrush(val_grad)
        p.drawEllipse(self.rect())

        p.setViewport(QRect(0, 0, self.width(), self.height()))
        p.setPen(Qt.black)
        p.setBrush(self.selected_color)
        x = self.width()*self.px
        y = self.height()*self.py
        p.drawEllipse(self.line_circle_inter(
            x, y, self.width()/2, self.height()/2, self.radius), 10, 10)

    def recalc(self) -> None:
        self.selected_color.setHsvF(self.h, self.s, self.v)
        self.currentColorChanged.emit(self.selected_color)
        self.repaint()

    def line_circle_inter(self, x: float, y: float, m_x: float, m_y: float, r: float) -> QPointF:
        m = np.array([m_x, m_y])
        p = np.array([x, y])
        d = p - m
        dist = np.linalg.norm(d)
        vec = d/dist
        c = m+vec*r-vec*self.margin
        return QPointF(c[0], c[1]) if dist >= r else QPointF(x, y)

    def map_color(self, x: int, y: int) -> 'tuple[float, float, float]':
        h = (np.arctan2(x-self.radius, y-self.radius)+np.pi)/(2.*np.pi)
        s = np.sqrt(np.power(x-self.radius, 2) +
                    np.power(y-self.radius, 2))/self.radius
        v = self.v
        if s > 1.0:
            s = 1.0
        return h, s, v

    def processMouseEvent(self, ev: QMouseEvent) -> None:
        x = ev.x()
        y = ev.y()
        if (ev.button() == Qt.RightButton):
            x = self.width() / 2
            y = self.height() / 2
        self.h, self.s, self.v = self.map_color(x, y)
        self.px = x / self.width()
        self.py = y / self.height()
        self.recalc()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.processMouseEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.processMouseEvent(a0)

    def setHue(self, hue: float) -> None:
        if 0 <= hue <= 1:
            self.h = float(hue)
            self.recalc()
        else:
            raise TypeError("Value must be between 0.0 and 1.0")

    def setSaturation(self, saturation: float) -> None:
        if 0 <= saturation <= 1:
            self.s = float(saturation)
            self.recalc()
        else:
            raise TypeError("Value must be between 0.0 and 1.0")

    def setValue(self, value: float) -> None:
        if 0 <= value <= 1:
            self.v = float(value)
            self.recalc()
        else:
            raise TypeError("Value must be between 0.0 and 1.0")

    def setColor(self, color: QColor) -> None:
        self.h = color.hueF()
        self.s = color.saturationF()
        self.v = color.valueF()
        self.recalc()

    def getHue(self) -> float:
        return self.h

    def getSaturation(self) -> float:
        return self.s

    def getValue(self) -> float:
        return self.v

    def getColor(self) -> QColor:
        return self.selected_color


class ColorCircleDialog(QWidget):
    currentColorChanged = pyqtSignal(QColor)

    def __init__(self, parent: Optional[QWidget] = None, width: int = 500, startupcolor: 'list[int]' = [255, 255, 255]) -> None:
        super().__init__(parent=parent)
        self.resize(width, width)

        lay = AspectLayout(1)
        wid = ColorCircle(self, startupcolor=startupcolor)
        wid.currentColorChanged.connect(
            lambda x: self.currentColorChanged.emit(x))
        lay.addWidget(wid)

        mainlay = QHBoxLayout()
        mainlay.addLayout(lay)
        fader = QSlider()
        fader.setMinimum(0)
        fader.setMaximum(511)
        fader.setValue(511)
        fader.valueChanged.connect(lambda x: wid.setValue(x/511))
        mainlay.addWidget(fader)

        self.setLayout(mainlay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = ColorCircleDialog()
    window.currentColorChanged.connect(lambda x: print(x.getRgb()))
    window.show()
    sys.exit(app.exec_())
