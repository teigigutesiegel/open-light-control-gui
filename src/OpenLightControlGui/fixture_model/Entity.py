import re
from typing import Union, Optional, Any, Dict

KEYWORDS = {
    'fast reverse': -100,
    'slow reverse': -1,
    'stop': 0,
    'slow': 1,
    'fast': 100,
    'fast CCW': -100,
    'slow CCW': -1,
    'slow CW': 1,
    'fast CW': 100,
    'instant': 0,
    'short': 1,
    'long': 100,
    'near': 1,
    'far': 100,
    'off': 0,
    'dark': 1,
    'bright': 100,
    'warm': -100,
    'CTO': -100,
    'default': 0,
    'cold': 100,
    'CTB': 100,
    'weak': 1,
    'strong': 100,
    'left': -100,
    'top': -100,
    'center': 0,
    'right': 100,
    'bottom': 100,
    'closed': 0,
    'narrow': 1,
    'wide': 100,
    'low': 1,
    'high': 100,
    'out': 0,
    'in': 100,
    'open': 100,
    'small': 1,
    'big': 100,
}

unitConversions: 'Dict[str, Dict[str, Union[str, float]]]' = {
    'ms': {
        'baseUnit': 's',
        'factor': 1 / 1000,
    },
    'bpm': {
        'baseUnit': 'Hz',
        'factor': 1 / 60,
    },
    'rpm': {
        'baseUnit': 'Hz',
        'factor': 1 / 60,
    },
}


class Entity():
    '''
    A physical entity with numerical value and unit information.
    '''
    _number: 'Union[float, int]'
    _unit: str
    _keyword: 'Optional[str]'
    _cache: 'Dict[str, Any]'

    def __init__(self, number: 'Union[float, int]', unit: str, keyword: Optional[str] = None) -> None:
        self._number = number
        self._unit = unit
        self._keyword = keyword
        self._cache = {}

    @property
    def number(self) -> 'Union[float, int]':
        return self._number
    
    @number.setter
    def number(self, number: 'Union[float, int]') -> None:
        self._number = number

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def keyword(self) -> Optional[str]:
        return self._keyword or None


    def copy(self) -> 'Entity':
        return Entity(self.number, self.unit, self.keyword)

    def getBaseUnitEntity(self) -> 'Entity':
        '''returns <Entity> An entity of the same value, but scaled to the base unit. Returns the entity itself if it is already in the base unit.'''
        if not 'baseUnitEntity' in self._cache.keys():
            if self.unit in unitConversions.keys():
                baseUnit, factor = unitConversions[self.unit].values()
                self._cache["baseUnitEntity"] = Entity(self.number * factor, baseUnit, self.keyword) # type: ignore
            else:
                self._cache["baseUnitEntity"] = self
        return self._cache["baseUnitEntity"]

    def __add__(self, o: 'Union[Entity, float, int]') -> 'Entity':
        if not isinstance(o, (Entity, float, int)):
            return NotImplemented
        new = self.copy()
        new += o
        return new
    
    def __iadd__(self, o: 'Union[Entity, float, int]') -> 'Entity':
        if isinstance(o, Entity):
            if self.unit != o.unit:
                raise TypeError(f"Can't add Entity of type {self.unit} and {o.unit}")
            self.number += o.number
        elif isinstance(o, (float, int)):
            self.number += o
        else:
            return NotImplemented
        return self

    def __lt__(self, x: 'Entity') -> bool:
        return self.number < x.number

    def __gt__(self, x: 'Entity') -> bool:
        return self.number > x.number

    def __str__(self) -> str:
        return self.keyword or f"{self.number}{self.unit}"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: 'object') -> bool:
        if not isinstance(o, Entity):
            return False
        return self.number == o.number and self.unit == o.unit and self.keyword == o.keyword

    @classmethod
    def createFromEntityString(cls, entityString: str) -> 'Entity':
        if entityString in KEYWORDS.keys():
            return Entity(KEYWORDS[entityString], "%", entityString)

        try:
            temp = re.compile("^([\d.-]+)(.*)$").match(entityString)
            if temp is None:
                raise ValueError()
            numberString, unitString = temp.groups()
            return Entity(float(numberString), unitString)
        except:
            raise ValueError(f"'{entityString}'' is not a vaild entity string.")
