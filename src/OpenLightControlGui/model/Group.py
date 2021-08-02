from typing import Iterable, Optional, Union

from OpenLightControlGui.model.Lamp import Lamp

class Group():
    _lamps: 'list[Union[Lamp, Group]]'

    def __init__(self, lamps: 'Optional[Union[Lamp, Iterable[Lamp], Group]]' = None) -> None:
        self._lamps = []
        if lamps:
            if isinstance(lamps, Iterable):
                for lamp in lamps:
                    self.addItem(lamp)
            else:
                self.addItem(lamps)
    
    def addItem(self, item: 'Union[Lamp, Group]') -> None:
        if not item in self._lamps:
            self._lamps.append(item)
    
    def removeItem(self, item: 'Union[Lamp, Group]') -> None:
        if item in self._lamps:
            self._lamps.pop(self._lamps.index(item))
    
    def getLamps(self) -> 'list[Lamp]':
        ret_list = []
        for item in self._lamps:
            if isinstance(item, Group):
                ret_list.extend(item.lamps)
            else:
                ret_list.append(item)
        return ret_list
    
    lamps: 'list[Lamp]' = property(getLamps)
    
    def includes(self, lamp: Lamp) -> bool:
        return lamp in self._lamps
    
    def copy(self) -> 'Group':
        return Group(self._lamps)
    
    def __add__(self, o: 'Union[Lamp, Iterable[Lamp], Group]') -> 'Group':
        g = self.copy()
        if isinstance(o, (Group, Lamp)):
            g += o
        elif isinstance(o, Iterable):
            for lamp in o:
                g += lamp
        return g
    
    def __iadd__(self, o: 'Union[Lamp, Iterable[Lamp], Group]') -> 'Group':
        if isinstance(o, (Group, Lamp)):
            self.addItem(o)
        elif isinstance(o, Iterable):
            for lamp in o:
                self.addItem(lamp)
        return self
    
    def __sub__(self, o: 'Union[Lamp, Iterable[Lamp], Group]') -> 'Group':
        g = self.copy()
        if isinstance(o, Group):
            if o in g._lamps:
                g -= o
            else:
                g -= o.lamps
        elif isinstance(o, Iterable):
            for lamp in o:
                g -= lamp
        elif isinstance(o, Lamp):
            g -= o
        return g

    def __isub__(self, o: 'Union[Lamp, Iterable[Lamp], Group]') -> 'Group':
        if isinstance(o, (Lamp, Group)):
            self.removeItem(o)
        elif isinstance(o, Iterable):
            for lamp in o:
                self.removeItem(lamp)
        return self

    def __str__(self) -> str:
        return f"Group {', '.join(str(x) for x in self.getLamps())}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec: str) -> str:
        return self.__str__()
