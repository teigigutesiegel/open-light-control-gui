from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QDialogButtonBox, QWidget, QLabel, QSpacerItem, QSizePolicy, QPushButton

from typing import Dict, Optional
import re

from OpenLightControlGui import CollapsibleBox, HiddenSpinBox
from OpenLightControlGui.fixture_model import Fixture
from OpenLightControlGui.utils.ofl import get_fixtures

class AddFixtureWidget(QDialog):
    _mainLay: QVBoxLayout
    _topBar: QHBoxLayout
    _searchInput: QLineEdit
    _mainScroll: QScrollArea
    _fixLay: QVBoxLayout
    _bottomBar: QDialogButtonBox
    
    _fixturedict: 'Dict[str, Dict[str, Fixture]]'
    _fixture_count: 'Dict[str, int]'
    _search: str
    
    def __init__(self, fixturedict: 'Dict[str, Dict[str, Fixture]]', parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self._fixturedict = fixturedict
        self._fixture_count = {}
        self._search = ""
        self.setWindowTitle("Add Fixtures")

        self._mainLay = QVBoxLayout()

        self._topBar = QHBoxLayout()
        self._mainLay.addLayout(self._topBar)
        self._topBar.addWidget(QLabel("Search fixture Name"))
        self._searchInput = QLineEdit()
        self._searchInput.textChanged.connect(self._textchanged) # type: ignore
        self._topBar.addWidget(self._searchInput)

        self._mainScroll = QScrollArea()
        self._fill_list()
        self._mainScroll.setWidgetResizable(True)
        self._mainLay.addWidget(self._mainScroll)

        self._bottomBar = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._mainLay.addWidget(self._bottomBar)
        self._bottomBar.accepted.connect(self.accept) # type: ignore
        self._bottomBar.rejected.connect(self.reject) # type: ignore

        self.setLayout(self._mainLay)
    
    def getFixtureCount(self) -> 'Dict[str, int]':
        return self._fixture_count

    def setFixtureCount(self, fixture_count: 'Dict[str, int]') -> None:
        self._fixture_count = fixture_count
        self._fill_list()
    
    def _textchanged(self, text: str) -> None:
        self._search = text
        self._fill_list()
    
    def _fill_list(self) -> None:
        search_re = re.compile(self._search, re.IGNORECASE)
        self._fixLay = QVBoxLayout()
        for man, fixs in self._fixturedict.items():
            collap = CollapsibleBox(
                fixs[list(fixs.keys())[0]].manufacturer.name)
            colllay = QVBoxLayout()
            for key, fix in fixs.items():
                for mode in fix.modes:
                    text = f"{fix.name} {mode.name}"
                    if search_re.search(text):
                        linelay = QHBoxLayout()
                        linelay.addWidget(QLabel(text))
                        spin = HiddenSpinBox()
                        if self._fixture_count.get(f"{man}/{fix.key}/{mode.name}"):
                            spin.setValue(self._fixture_count[f"{man}/{fix.key}/{mode.name}"])
                        spin.valueChanged.connect(
                            lambda num, fix=f"{man}/{fix.key}/{mode.name}": self._fixture_count.__setitem__(fix, num))
                        spin.setMaximumWidth(100)
                        linelay.addWidget(spin)
                        linelay.addWidget(QLabel(f"{len(mode.channelKeys)}ch"))
                        colllay.addLayout(linelay)
            collap.setContentLayout(colllay)
            if colllay.count():
                self._fixLay.addWidget(collap)
        vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self._fixLay.addSpacerItem(vspacer)
        wid = QWidget()
        wid.setLayout(self._fixLay)
        self._mainScroll.setWidget(wid)

if __name__ == "__main__":
    import os
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    basepath = os.path.dirname(__file__)
    ofl = os.path.join(basepath, "../../../../open-fixture-library/fixtures/")
    fixturesByManu = get_fixtures(ofl)

    window = QPushButton("Add Fixture")

    def clicked():
        dlg = AddFixtureWidget(fixturesByManu, window)
        if dlg.exec():
            print(dlg.getFixtureCount())
        else:
            print("Cancel!")
    
    window.pressed.connect(clicked) # type: ignore
    window.show()

    sys.exit(app.exec_())
