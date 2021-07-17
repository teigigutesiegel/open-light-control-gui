from .CoarseChannel import CoarseChannel

from typing import TYPE_CHECKING, Any
import json
if TYPE_CHECKING:
    from .AbstractChannel import AbstractChannel
    from .Fixture import Fixture


class TemplateChannel(CoarseChannel):
    '''
    Represents a blueprint channel of which several similar channels can be generated.
    Currently used to create matrix channels.
    '''
    _cache: 'dict[str, Any]'

    def __init__(self, key: str, jsonObject: 'dict[str, Any]', fixture: 'Fixture') -> None:
        super().__init__(key, jsonObject, fixture)
        self._cache = {}

    def _get_allTemplateKeys(self) -> 'list[str]':
        if not "allTemplateKeys" in self._cache.keys():
            self._cache["allTemplateKeys"] = [self.key] + \
                self.fineChannelAliases + self.switchingChannelAliases

        return self._cache["allTemplateKeys"]

    def _get_possibleMatrixChannelKeys(self) -> 'dict[str, list[str]]':
        if not "possibleMatrixChannelKeys" in self._cache.keys():
            resolvedChannelKeys = {}

            for templateKey in self.allTemplateKeys:
                pixelKeys = self.fixture.matrix.pixelKeys + self.fixture.matrix.pixelGroupKeys
                resolvedChannelKeys[templateKey] = [TemplateChannel.resolveTemplateString(
                    templateKey, {"pixelKey": pixelKey}) for pixelKey in pixelKeys]

            self._cache["possibleMatrixChannelKeys"] = resolvedChannelKeys

        return self._cache["possibleMatrixChannelKeys"]

    def createMatrixChannels(self) -> 'list[AbstractChannel]':
        '''
        Creates matrix channels from this template channel (together with its fine and switching channels if defined) and all pixel keys.
        returns list[<AbstractChannel>] The generated channels associated to the given pixel key and its fine and switching channels.
        '''
        matrixChannels = []

        pixelKeys = self.fixture.matrix.pixelKeys + self.fixture.matrix.pixelGroupKeys
        for pixelKey in pixelKeys:
            templateVariables = {"pixelKey": pixelKey}

            jsonData = TemplateChannel.resolveTemplateObject(
                self._jsonObject, templateVariables)
            channelKey = TemplateChannel.resolveTemplateString(
                self._key, templateVariables)
            mainChannel = CoarseChannel(channelKey, jsonData, self.fixture)

            channels = [mainChannel] + mainChannel.fineChannels + \
                mainChannel.switchingChannels
            for channel in channels:
                channel.pixelKey = pixelKey
            matrixChannels.extend(channels)

        return matrixChannels

    @staticmethod
    def resolveTemplateObject(object_: 'dict', variables: 'dict[str, str]') -> 'dict':
        '''Replaces the specified variables in the specified object by cloning the object.'''
        return json.loads(TemplateChannel.resolveTemplateString(json.dumps(object_), variables))

    @staticmethod
    def resolveTemplateString(string_: str, variables: 'dict[str, str]') -> str:
        '''Replaces the specified variables in the specified string.'''
        for variable in variables:
            string_ = string_.replace(f"${variable}", variables[variable])
        return string_

    allTemplateKeys: 'list[str]' = property(_get_allTemplateKeys)
    possibleMatrixChannelKeys: 'dict[str, list[str]]' = property(
        _get_possibleMatrixChannelKeys)
