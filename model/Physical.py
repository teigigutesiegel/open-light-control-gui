from typing import Any, Optional
from numbers import Number


class Physical():
    '''A fixture's technical data, belonging to the hardware and not the DMX protocol.'''

    _jsonObject: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject

    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject

    def _get_dimensions(self) -> 'Optional[list[Number]]':
        return self._jsonObject.get("dimensions", None) or None

    def _get_width(self) -> 'Optional[Number]':
        return self.dimensions[0] if self.dimensions != None else None

    def _get_height(self) -> 'Optional[Number]':
        return self.dimensions[1] if self.dimensions != None else None

    def _get_depth(self) -> 'Optional[Number]':
        return self.dimensions[2] if self.dimensions != None else None

    def _get_weight(self) -> 'Optional[Number]':
        return self._jsonObject.get("weight", None) or None

    def _get_power(self) -> 'Optional[Number]':
        return self._jsonObject.get("power", None) or None

    def _get_DMXconnector(self) -> 'Optional[str]':
        return self._jsonObject.get("DMXconnector", None) or None

    def _get_hasBulb(self) -> bool:
        return "bulb" in self._jsonObject.keys()

    def _get_bulbType(self) -> 'Optional[str]':
        return self._jsonObject["bulb"].get("type", None) if self.hasBulb else None

    def _get_bulbColorTemperature(self) -> 'Optional[Number]':
        return self._jsonObject["bulb"].get("colorTemperature", None) if self.hasBulb else None

    def _get_bulbLumens(self) -> 'Optional[Number]':
        return self._jsonObject["bulb"].get("lumens", None) if self.hasBulb else None

    def _get_hasLens(self) -> bool:
        return "lens" in self._jsonObject.keys()

    def _get_lensName(self) -> str:
        return self._jsonObject["lens"].get("name", None) if self.hasLens else None

    def _get_lensDegreesMin(self) -> 'Optional[Number]':
        return self._jsonObject["lens"]["degreesMinMax"][0] if self.hasLens and "degreesMinMax" in self._jsonObject["lens"].keys() else None

    def _get_lensDegreesMax(self) -> 'Optional[Number]':
        return self._jsonObject["lens"]["degreesMinMax"][1] if self.hasLens and "degreesMinMax" in self._jsonObject["lens"].keys() else None

    def _get_hasMatrixPixels(self) -> bool:
        return "matrixPixels" in self._jsonObject.keys()

    def _get_matrixPixelsDimensions(self) -> str:
        return self._jsonObject["matrixPixels"]["dimensions"] if self.hasMatrixPixels else None

    def _get_matrixPixelsSpacing(self) -> str:
        return self._jsonObject["matrixPixels"]["spacing"] if self.hasMatrixPixels else None

    jsonObject: 'dict[str, Any]' = property(_get_jsonObject)
    dimensions: 'Optional[list[Number]]' = property(_get_dimensions)
    width: 'Optional[Number]' = property(_get_width)
    height: 'Optional[Number]' = property(_get_height)
    depth: 'Optional[Number]' = property(_get_depth)
    weight: 'Optional[Number]' = property(_get_weight)
    power: 'Optional[Number]' = property(_get_power)
    DMXconnector: 'Optional[str]' = property(_get_DMXconnector)
    hasBulb: bool = property(_get_hasBulb)
    bulbType: 'Optional[str]' = property(_get_bulbType)
    bulbColorTemperature: 'Optional[Number]' = property(
        _get_bulbColorTemperature)
    bulbLumens: 'Optional[Number]' = property(_get_bulbLumens)
    hasLens: bool = property(_get_hasLens)
    lensName: str = property(_get_lensName)
    lensDegreesMin: 'Optional[Number]' = property(_get_lensDegreesMin)
    lensDegreesMax: 'Optional[Number]' = property(_get_lensDegreesMax)
    hasMatrixPixels: bool = property(_get_hasMatrixPixels)
    matrixPixelsDimensions: str = property(_get_matrixPixelsDimensions)
    matrixPixelsSpacing: str = property(_get_matrixPixelsSpacing)
