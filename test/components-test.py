from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

from OpenLightControlGui import AbstractDirectoryView, PalletteDirectoryView

app = QApplication(sys.argv)

window = PalletteDirectoryView()
window.show()
sys.exit(app.exec_())
