from .Physical import Physical
from .SwitchingChannel import SwitchingChannel, SwitchingChannelBehavior
from .TemplateChannel import TemplateChannel

from typing import TYPE_CHECKING, Any, Optional, Union
from numbers import Number
from itertools import chain

if TYPE_CHECKING:
    from .AbstractChannel import AbstractChannel
    from .Fixture import Fixture


def _findIndex(flist, func):
    for i, v in enumerate(flist):
        if func(v):
            return i
    return -1


class Mode():
    '''A fixture's configuration that enables a fixed set of channels and channel order.'''
    _jsonObject: 'dict[str, Any]'
    _fixture: 'Fixture'
    _cache: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]', fixture: 'Fixture') -> None:
        self._jsonObject = jsonObject
        self._fixture = fixture
        self._cache = {}

    def __str__(self) -> str:
        return f"Mode <{self.name}>"

    def __repr__(self) -> str:
        return f"<...{self.fixture.name}[{self.name}]...>"

    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject

    def _set_jsonObject(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}

    def _get_fixture(self) -> 'Fixture':
        return self._fixture

    def _set_fixture(self, fixture: 'Fixture') -> None:
        self._fixture = fixture
        self._cache = {}

    def _get_name(self) -> str:
        return self._jsonObject["name"]

    def _get_shortName(self) -> str:
        return self._jsonObject.get("shortName", self.name)

    def _get_hasShortName(self) -> bool:
        return "shortName" in self._jsonObject.keys()

    def _get_rdmPersonalityIndex(self) -> 'Optional[Number]':
        return self._jsonObject.get("rdmPersonalityIndex", None) or None

    def _get_physicalOverride(self) -> 'Optional[Physical]':
        if not "physicalOverride" in self._cache.keys():
            self._cache["physicalOverride"] = Physical(
                self._jsonObject["physicalOverride"]) if "physicalOverride" in self._jsonObject.keys() else None

        return self._cache["physicalOverride"]

    def _get_physical(self) -> 'Optional[Physical]':
        if not "physical" in self._cache.keys():
            if self.fixture.physical == None:
                self._cache["physical"] = self.physicalOverride
            elif self.physicalOverride == None:
                self._cache["physical"] = self.fixture.physical
            else:
                fixturePhysical = self.fixture.physical.jsonObject
                physicalOverride = self._jsonObject["physical"]
                physicalData = {**fixturePhysical, **physicalOverride}

                for prop in ["bulb", "lens", "matrixPixels"]:
                    if prop in physicalData.keys():
                        physicalData[prop] = {
                            **fixturePhysical[prop], **physicalOverride[prop]}

                self._cache["physical"] = Physical(physicalData)

        return self._cache["physical"]

    def _get_channelKeys(self) -> 'list[str]':
        if not "channelKeys" in self._cache.keys():
            self._cache["channelKeys"] = []
            for rawReference in self._jsonObject["channels"]:
                if rawReference != None and isinstance(rawReference, dict) and rawReference["insert"] == "matrixChannels":
                    self._cache["channelKeys"].extend(self._getMatrixChannelKeysFromInsertBlock(rawReference))
                else:
                    self._cache["channelKeys"].append(rawReference)

        return self._cache["channelKeys"]

    def _get_nullChannelCount(self) -> int:
        return self.channelKeys.count(None)

    def _getMatrixChannelKeysFromInsertBlock(self, channelInsert: 'dict[str, Any]') -> 'list[str]':
        '''
        Resolves the matrix channel insert block into a list of channel keys
        returns list[str] The resolved channel keys
        '''
        pixelKeys = self._getRepeatForPixelKeys(channelInsert["repeatFor"])

        channelKeys = []
        if channelInsert.get("channelOrder", None) == "prePixel":
            for pixelKey in pixelKeys:
                for templateChannelKey in channelInsert.get("templateChannels", []):
                    channelKeys.append(TemplateChannel.resolveTemplateString(
                        templateChannelKey, {"pixelKey": pixelKey}))
        elif channelInsert.get("channelOrder", None) == "perChannel":
            for templateChannelKey in channelInsert.get("templateChannels", []):
                for pixelKey in pixelKeys:
                    channelKeys.append(TemplateChannel.resolveTemplateString(
                        templateChannelKey, {"pixelKey": pixelKey}))

        return channelKeys

    def _getRepeatForPixelKeys(self, repeatFor: 'Union[str, list[str]]') -> 'list[str]':
        if isinstance(repeatFor, list):
            return repeatFor

        matrix = self.fixture.matrix

        if repeatFor == "eachPixelGroup":
            return matrix.pixelGroupKeys

        if repeatFor == "eachPixelABC":
            return matrix.pixelKeys

        orderByAxes = list(repeatFor.replace("eachPixel", ""))
        return matrix.getPixelKeysByOrder(*orderByAxes)

    def _get_channels(self) -> 'list[AbstractChannel]':
        if not "channels" in self._cache.keys():
            nullChannelsFound = 0
            self._cache["channels"] = []
            for channelKey in self.channelKeys:
                if channelKey == None:
                    nullChannelsFound += 1
                    self._cache["channels"].append(nullChannelsFound - 1)
                else:
                    self._cache["channels"].append(
                        self.fixture.getChannelByKey(channelKey))

        return self._cache["channels"]

    jsonObject: 'dict[str, Any]' = property(_get_jsonObject, _set_jsonObject)
    fixture: 'Fixture' = property(_get_fixture, _set_fixture)
    name: str = property(_get_name)
    shortName: str = property(_get_shortName)
    hasShortName: bool = property(_get_hasShortName)
    rdmPersonalityIndex: 'Optional[Number]' = property(
        _get_rdmPersonalityIndex)
    physicalOverride: 'Optional[Physical]' = property(_get_physicalOverride)
    physical: 'Optional[Physical]' = property(_get_physical)
    channelKeys: 'list[str]' = property(_get_channelKeys)
    nullChannelCount: int = property(_get_nullChannelCount)
    channels: 'list[AbstractChannel]' = property(_get_channels)

    def getChannelIndex(self, channelKey: str, switchingChannelBehavior: SwitchingChannelBehavior = "all") -> int:
        def filtering(channel: 'AbstractChannel') -> bool:
            if channel == None:
                return False

            if isinstance(channel, SwitchingChannel):
                return channel.usesChannelKey(channelKey, switchingChannelBehavior)

            return channel.key == channelKey

        return _findIndex(self.channels, filtering)
