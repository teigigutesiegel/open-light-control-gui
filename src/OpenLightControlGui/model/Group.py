from typing import Iterable, List, Optional, Union

from OpenLightControlGui.model.Lamp import Lamp

class Group():
    _lamps: 'List[Union[Lamp, Group]]'
    _name: str

    def __init__(self, lamps: 'Optional[Union[Lamp, Group, Iterable[Union[Lamp, Group]]]]' = None, *, name: str = None) -> None:
        if not name:
            self._name = ""
        else:
            self._name = name
        self._lamps = []
        if lamps:
            if isinstance(lamps, Iterable):
                for lamp in lamps:
                    self.addItem(lamp)
            else:
                self.addItem(lamps)

    def addItem(self, item: 'Union[Lamp, Group]') -> None:
        self._lamps.append(item)

    def addItems(self, items: 'Iterable[Union[Lamp, Group]]') -> None:
        for item in items:
            self.addItem(item)

    def removeItem(self, item: 'Union[Lamp, Group]') -> None:
        if item in self._lamps:
            self._lamps.pop(self._lamps.index(item))
        elif isinstance(item, Group):
            self.removeItems(item.lamps)

    def removeItems(self, items: 'Iterable[Union[Lamp, Group]]') -> None:
        for item in items:
            self.removeItem(item)

    @property
    def lamps(self) -> 'List[Lamp]':
        ret_list = []
        for item in self._lamps:
            if isinstance(item, Group):
                ret_list.extend(item.lamps)
            else:
                ret_list.append(item)
        return ret_list

    def getLamps(self) -> 'List[Lamp]':
        return self.lamps

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def includes(self, lamp: 'Union[Lamp, Group]') -> bool:
        return lamp in self._lamps

    def copy(self) -> 'Group':
        return Group(self._lamps.copy())

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Group):
            return NotImplemented
        return self.lamps == o.lamps

    def __len__(self) -> int:
        return len(self.lamps)

    def __add__(self, o: 'Union[Lamp, Group, Iterable[Union[Lamp, Group]]]') -> 'Group':
        g = self.copy()
        g += o
        return g

    def __iadd__(self, o: 'Union[Lamp, Group, Iterable[Union[Lamp, Group]]]') -> 'Group':
        if isinstance(o, (Group, Lamp)):
            self.addItem(o)
        elif isinstance(o, Iterable):
            self.addItems(o)
        return self

    def __sub__(self, o: 'Union[Lamp, Group, Iterable[Union[Lamp, Group]]]') -> 'Group':
        g = self.copy()
        g -= o
        return g

    def __isub__(self, o: 'Union[Lamp, Group, Iterable[Union[Lamp, Group]]]') -> 'Group':
        if isinstance(o, (Lamp, Group)):
            self.removeItem(o)
        elif isinstance(o, Iterable):
            self.removeItems(o)
        return self

    def __repr__(self) -> str:
        return f"Group([{' ,'.join(repr(x) for x in self._lamps)}])"

    def __str__(self) -> str:
        if len(self) > 2:
            return f"Group <{', '.join([str(x) for x in self.getLamps()][:2])}, ...> [{len(self)}]"
        return f"Group <{', '.join([str(x) for x in self.getLamps()])}> [{len(self)}]"
