from PyQt5.QtWidgets import QLayout
from PyQt5.QtCore import Qt, QSize

class AspectLayout(QLayout):
    def __init__(self, aspect):
        self.aspect = aspect
        self.item = None
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

    def addItem(self, item):
        assert self.item is None, "AspectLayout can contain only 1 widget"
        self.item = item

    def itemAt(self, index):
        if index != 0:
            return None
        if self.item is None:
            return None
        return self.item

    def takeAt(self, index):
        if index != 0:
            return None
        if self.item is None:
            return None
        result = self.item
        self.item = None
        return result

    def setGeometry(self, rect):
        super().setGeometry(rect)
        margins = self.getContentsMargins()
        if self.item is not None:
            availW = rect.width() - margins[1] - margins[3]
            availH = rect.height() - margins[0] - margins[2]
            h = availH
            w = h * self.aspect
            if w > availW:
                x = margins[1]
                w = availW
                h = w/self.aspect
                if self.item.alignment() & Qt.AlignTop:
                    y = margins[0]
                elif self.item.alignment() & Qt.AlignBottom:
                    y = rect.height() - margins[2] - h
                else:
                    y = margins[0] + (availH-h) / 2
            else:
                y = margins[0]
                if self.item.alignment() & Qt.AlignLeft:
                    x = margins[1]
                elif self.item.alignment() & Qt.AlignRight:
                    x = rect.width() - margins[3] - w
                else:
                    x = margins[1] + (availW-w) / 2
            self.item.widget().setGeometry(
                int(rect.x() + x),
                int(rect.y() + y),
                int(w), int(h))

    def sizeHint(self):
        margins = self.getContentsMargins()
        if self.item is None:
            return QSize(margins[0]+margins[2], margins[1]+margins[3])
        s = self.item.sizeHint()
        w, h = s.width(), s.height()
        return QSize(margins[0]+margins[2] + w, margins[1]+margins[3] + h)

    def minimumSize(self):
        margins = self.getContentsMargins()
        if self.item is None:
            return QSize(margins[0]+margins[2], margins[1]+margins[3])
        s = self.item.minimumSize()
        w, h = s.width(), s.height()
        return QSize(margins[0]+margins[2] + w, margins[1]+margins[3] + h)

    def expandingDirections(self):
       return Qt.Horizontal | Qt.Vertical

    def hasHeightForWidth(self):
        return False

    def count(self):
        if self.item is None:
            return 0
        else:
            return 1

    def heightForWidth(self, width):
        margins = self.getContentsMargins()
        height = (width - margins[1] - margins[3]) / self.aspect
        height += margins[0] + margins[2]
        return int(height)
