from OpenLightControlGui import PalletteDirectoryView

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget


class PositionDirectoryView(PalletteDirectoryView):

    def __init__(self, parent: Optional['QWidget'] = None, placeholder: int = 1000) -> None:
        super().__init__("Position", parent=parent, placeholder=placeholder)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = PositionDirectoryView()
    window.show()
    sys.exit(app.exec_())
