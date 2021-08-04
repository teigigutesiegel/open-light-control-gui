from OpenLightControlGui import PalletteDirectoryView

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget


class IntensityDirectoryView(PalletteDirectoryView):

    def __init__(self, parent: Optional['QWidget'] = None) -> None:
        super().__init__("Intensity", parent=parent)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = IntensityDirectoryView()
    window.show()
    sys.exit(app.exec_())
