from numbers import Number
from typing import Any, Optional


class Manufacturer():
    '''
    A company or brand that produces fixtures. A fixture is associated to exactly one manufacturer.
    '''

    _jsonObject: 'dict[str, Any]'
    key: str

    def __init__(self, key: str, jsonObject: 'dict[str, Any]') -> None:
        self.key = key
        self._jsonObject = jsonObject
    
    def __str__(self) -> str:
        return f"Manufacturer <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_name(self) -> str:
        return self._jsonObject["name"]

    def _get_comment(self) -> str:
        return self._jsonObject.get("comment", "") or ""

    def _get_hasComment(self) -> bool:
        return "comment" in self._jsonObject.keys()

    def _get_website(self) -> 'Optional[str]':
        return self._jsonObject.get("website", None) or None

    def _get_rdmId(self) -> 'Optional[Number]':
        return self._jsonObject.get("rdmId", None) or None

    name: str = property(_get_name)
    comment: str = property(_get_comment)
    hasComment: bool = property(_get_hasComment)
    website: 'Optional[str]' = property(_get_website)
    rdmId: 'Optional[str]' = property(_get_rdmId)
