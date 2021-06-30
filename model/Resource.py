from typing import Any, Optional, Literal
import urllib


class Resource():
    '''Information about a resource.'''

    _jsonObject: 'dict[str, Any]'
    _cache: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}
    
    def __str__(self) -> str:
        return f"Resource <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_name(self) -> str:
        return self._jsonObject["name"]

    def _get_keywords(self) -> 'list[str]':
        return self._jsonObject.get("keywords", "").split(" ")

    def _get_source(self) -> 'Optional[str]':
        return self._jsonObject.get("source", None) or None

    def _get_key(self) -> str:
        return self._jsonObject["key"]

    def _get_type(self) -> str:
        return self._jsonObject["type"]

    def _get_alias(self) -> 'Optional[str]':
        return self._jsonObject.get("alias", None) or None

    def _get_hasImage(self) -> bool:
        return "image" in self._jsonObject.keys()

    def _get_imageExtension(self) -> 'Optional[str]':
        return self._jsonObject["image"]["extension"] if self.hasImage else None

    def _get_imageMimeType(self) -> 'Optional[str]':
        return self._jsonObject["image"]["mimeType"] if self.hasImage else None

    def _get_imageData(self) -> 'Optional[str]':
        return self._jsonObject["image"]["data"] if self.hasImage else None

    def _get_imageEncoding(self) -> 'Optional[Literal["base64", "utf8"]]':
        return self._jsonObject["image"]["encoding"] if self.hasImage else None

    def _get_imageDataUrl(self) -> 'Optional[str]':
        if not self.hasImage:
            return None

        if not "dataUrl" in self._cache.keys():
            mimeType = self.imageMimeType

            imageData = urllib.parse.quote(self.imageData, safe='').replace(
                "(", "%28").replace(")", "%29")

            if self.imageEncoding == "base64":
                mimeType += ";base64"

            self._cache["dataUrl"] = f"data:{mimeType},{imageData}"

        return self._cache["dataUrl"]

    name: str = property(_get_name)
    keywords: 'list[str]' = property(_get_keywords)
    source: 'Optional[str]' = property(_get_source)
    key: str = property(_get_key)
    type: str = property(_get_type)
    alias: 'Optional[str]' = property(_get_alias)
    hasImage: bool = property(_get_hasImage)
    imageExtension: 'Optional[str]' = property(_get_imageExtension)
    imageMimeType: 'Optional[str]' = property(_get_imageMimeType)
    imageData: 'Optional[str]' = property(_get_imageData)
    imageEncoding: 'Optional[Literal["base64", "utf8"]]' = property(
        _get_imageEncoding)
    imageDataUrl: 'Optional[str]' = property(_get_imageDataUrl)
