from datetime import date
from typing import Any, Optional


class Meta():
    '''
    Information about a fixture's author and history.
    '''

    _jsonObject: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject

    def _get_authors(self) -> 'list[str]':
        return self._jsonObject["authors"]

    def _get_createDate(self) -> date:
        return date.fromisoformat(self._jsonObject["createDate"])

    def _get_lastModifyDate(self) -> date:
        return date.fromisoformat(self._jsonObject["lastModifyDate"])

    def _get_importPlugin(self) -> 'Optional[str]':
        if "importPlugin" in self._jsonObject.keys():
            return self._jsonObject["importPlugin"]["plugin"]
        else:
            return None

    def _get_importDate(self) -> 'Optional[date]':
        if "importPlugin" in self._jsonObject.keys():
            return self._jsonObject["importPlugin"]["date"]
        else:
            return None

    def _get_importComment(self) -> 'Optional[str]':
        if "importPlugin" in self._jsonObject.keys():
            return self._jsonObject["importPlugin"].get("comment", "")
        else:
            return None

    def _get_hasImportComment(self) -> bool:
        return self.importPlugin != None and "comment" in self._jsonObject["importPlugin"].keys()

    authors: 'list[str]' = property(_get_authors)
    createDate: date = property(_get_createDate)
    lastModifyDate: date = property(_get_lastModifyDate)
    importPlugin: 'Optional[str]' = property(_get_importPlugin)
    importDate: 'Optional[date]' = property(_get_importDate)
    importComment: 'Optional[str]' = property(_get_importComment)
    hasImportComment: bool = property(_get_hasImportComment)
