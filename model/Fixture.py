from .CoarseChannel import CoarseChannel
from .FineChannel import FineChannel
from .Matrix import Matrix
from .Meta import Meta
from .Mode import Mode
from .NullChannel import NullChannel
from .Physical import Physical
from .SwitchingChannel import SwitchingChannel
from .TemplateChannel import TemplateChannel
from .Wheel import Wheel

from typing import TYPE_CHECKING, Any, Optional, Union
from os import environ
from itertools import chain

if TYPE_CHECKING:
    from .AbstractChannel import AbstractChannel
    from .Capability import Capability
    from .Manufacturer import Manufacturer

class RDMInfo():
    _modelId: int
    _softwareVersion: 'Optional[str]'

    def __init__(self, jsonObject: 'dict[str, Any]') -> None:
        self._modelId = jsonObject.get("modelId")
        self._softwareVersion = jsonObject.get("softwareVersion")
    
    modelId: int = property(lambda self: self._modelId)
    softwareVersion: int = property(lambda self: self._softwareVersion)

class Fixture():
    '''A physical DMX device.'''
    _manufacturer: 'Manufacturer'
    _key: str
    _jsonObject: 'dict[str, Any]'
    _cache: 'dict[str, Any]'

    def __init__(self, manufacturer: 'Manufacturer', key: str, jsonObject: 'dict[str, Any]') -> None:
        self._manufacturer = manufacturer
        self._key = key
        self._jsonObject = jsonObject
        self._cache = {}

    def __str__(self) -> str:
        return f"Fixture <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_manufacturer(self) -> 'Manufacturer':
        return self._manufacturer
    
    def _set_manufacturer(self, manufacturer: 'Manufacturer') -> None:
        self._manufacturer = manufacturer
    
    def _get_key(self) -> str:
        return self._key

    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject
    
    def _set_jsonObject(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}

    def _get_url(self) -> str:
        websiteUrl = environ.get(
            "WEBSITE_URL") or "https://open-fixture-library.org/"
        return f"{websiteUrl}{self.manufacturer.key}/{self.key}"
    
    def _get_name(self) -> str:
        return self._jsonObject["name"]
    
    def _get_hasShortName(self) -> bool:
        return "shortName" in self._jsonObject.keys()
    
    def _get_shortName(self) -> str:
        return self._jsonObject.get("shortName", self._jsonObject["name"])
    
    def _get_categories(self) -> 'list[str]':
        return self._jsonObject.get("categories", ["Other"])
    
    def _get_mainCategory(self) -> str:
        return self.categories[0]
    
    def _get_meta(self) -> Meta:
        if not "meta" in self._cache.keys():
            self._cache["meta"] = Meta(
                self._jsonObject.get("meta", {"authors": [""], "createDate": "2000-01-01", "lastModifyDate": "2000-01-01"}))
        
        return self._cache["meta"]
    
    def _get_hasComment(self) -> bool:
        return "comment" in self._jsonObject.keys()
    
    def _get_comment(self) -> str:
        return self._jsonObject.get("comment", "")
    
    def _get_helpWanted(self) -> 'Optional[str]':
        return self._jsonObject.get("helpWanted")
    
    def _get_isHelpWanted(self) -> bool:
        return self.helpWanted != None or self.isCapabilityHelpWanted
    
    def _get_isCapabilityHelpWanted(self) -> bool:
        if not "isCapabilityHelpWanted" in self._cache.keys():
            self._cache["isCapabilityHelpWanted"] = any(getattr(channel, "isHelpWanted", False) for channel in self.allChannels)
        
        return self._cache["isCapabilityHelpWanted"]
    
    def _get_links(self) -> 'Optional[dict[str, list[str]]]':
        return self._jsonObject.get("links")

    def _get_rdm(self) -> 'Optional[RDMInfo]':
        if not "rdm" in self._cache.keys():
            self._cache["rdm"] = RDMInfo(self._jsonObject.get("rdm", {})) if "rdm" in self._jsonObject.keys() else None
        
        return self._cache["rdm"]
    
    def _get_physical(self) -> 'Optional[Physical]':
        if not "physical" in self._cache.keys():
            self._cache["physical"] = Physical(self._jsonObject["physical"]) if "physical" in self._jsonObject.keys() else None
        
        return self._cache["physical"]

    def _get_matrix(self) -> 'Optional[Matrix]':
        if not "matrix" in self._cache.keys():
            self._cache["matrix"] = Matrix(
                self._jsonObject["matrix"]) if "matrix" in self._jsonObject.keys() else None

        return self._cache["matrix"]

    def _get_wheels(self) -> 'list[Wheel]':
        if not "wheels" in self._cache.keys():
            self._cache["wheels"] = [Wheel(wheelName, wheelJson) for wheelName,
                                  wheelJson in self._jsonObject.get("wheels", {}).items()]
        
        return self._cache["wheels"]

    def _get_uniqueChannelNames(self) -> 'dict[str, str]':
        if not "uniqueChannelNames" in self._cache.keys():
            self._cache["uniqueChannelNames"] = {}
            
            names = [channel.name for channel in self.allChannels]

            for index, originalName in enumerate(names):
                duplicates = 1
                while names.index(names[index]) != index:
                    duplicates += 1
                    names[index] = f"{originalName} {duplicates}"
                
                self._cache["uniqueChannelNames"][self.allChannelKeys[index]] = names[index]
        
        return self._cache["uniqueChannelNames"]

    def _get_availableChannelKeys(self) -> 'list[str]':
        if not "availableChannelKeys" in self._cache.keys():
            self._cache["availableChannelKeys"] = self._jsonObject.get(
                "availableChannels", {}).keys()
        
        return self._cache["availableChannelKeys"]
    
    def _get_availableChannels(self) -> 'list[CoarseChannel]':
        if not "availableChannels" in self._cache.keys():
            self._cache["availableChannels"] = [CoarseChannel(
                channelKey, self._jsonObject["availableChannels"][channelKey], self) for channelKey in self.availableChannelKeys]
        
        return self._cache["availableChannels"]

    def _get_coarseChannelKeys(self) -> 'list[str]':
        if not "coarseChannelKeys" in self._cache.keys():
            self._cache["coarseChannelKeys"] = [channel.key for channel in self.coarseChannels]
        
        return self._cache["coarseChannelKeys"]

    def _get_coarseChannels(self) -> 'list[CoarseChannel]':
        if not "coarseChannels" in self._cache.keys():
            self._cache["coarseChannels"] = list(filter(lambda channel: isinstance(channel, CoarseChannel), self.allChannels))
        
        return self._cache["coarseChannels"]
    
    def _get_fineChannelAliases(self) -> 'list[str]':
        if not "fineChannelAliases" in self._cache.keys():
            self._cache["fineChannelAliases"] = [channel.key for channel in self.fineChannels]
        
        return self._cache["fineChannelAliases"]
    
    def _get_fineChannels(self) -> 'list[FineChannel]':
        if not "fineChannels" in self._cache.keys():
            self._cache["fineChannels"] = list(
                filter(lambda channel: isinstance(channel, FineChannel), self.allChannels))

        return self._cache["fineChannels"]

    def _get_switchingChannelAliases(self) -> 'list[str]':
        if not "switchingChannelAliases" in self._cache.keys():
            self._cache["switchingChannelAliases"] = [
                channel.key for channel in self.switchingChannels]

        return self._cache["switchingChannelAliases"]

    def _get_switchingChannels(self) -> 'list[SwitchingChannel]':
        if not "switchingChannels" in self._cache.keys():
            self._cache["switchingChannels"] = list(
                filter(lambda channel: isinstance(channel, SwitchingChannel), self.allChannels))

        return self._cache["switchingChannels"]

    def _get_templateChannelKeys(self) -> 'list[str]':
        return self._jsonObject.get("templateChannels", {}).keys()
    
    def _get_templateChannels(self) -> 'list[TemplateChannel]':
        if not "templateChannels" in self._cache.keys():
            self._cache["templateChannels"] = [TemplateChannel(key, self._jsonObject["templateChannels"][key], self) for key in self.templateChannelKeys]
        
        return self._cache["templateChannels"]

    def _get_matrixChannelKeys(self) -> 'list[str]':
        if not "matrixChannelKeys" in self._cache.keys():
            self._cache["matrixChannelKeys"] = [channel.key for channel in self.matrixChannels]
        
        return self._cache["matrixChannelKeys"]
    
    def _get_matrixChannels(self) -> 'list[AbstractChannel]':
        if self.matrix == None:
            return []
        
        if not "matrixChannels" in self._cache.keys():
            self._cache["matrixChannels"] = list(filter(lambda channel: channel.pixelKey != None, self.allChannels))
        
        return self._cache["matrixChannels"]

    def _get_nullChannelKeys(self) -> 'list[str]':
        return [channel.key for channel in self.nullChannels]
    
    def _get_nullChannels(self) -> 'list[NullChannel]':
        if not "nullChannels" in self._cache.keys():
            maxNullPerMode = max([mode.nullChannelCount for mode in self.modes]+[0])
            self._cache["nullChannels"] = [NullChannel(self) for i in range(maxNullPerMode)]
        
        return self._cache["nullChannels"]

    def _get_allChannelKeys(self) -> 'list[str]':
        if not "allChannelKeys" in self._cache.keys():
            self._cache["allChannelKeys"] = list(self.allChannelsByKey.keys())
        
        return self._cache["allChannelKeys"]

    def _get_allChannels(self) -> 'list[AbstractChannel]':
        if not "allChannels" in self._cache.keys():
            self._cache["allChannels"] = list(self.allChannelsByKey.values())
        
        return self._cache["allChannels"]

    def _get_allChannelsByKey(self) -> 'dict[str, AbstractChannel]':
        if not "allChannelsByKey" in self._cache.keys():
            allChannels = [*list(chain.from_iterable([[mainChannel, *mainChannel.fineChannels, *mainChannel.switchingChannels] for mainChannel in self.availableChannels])), *self.nullChannels]

            allChannelsByKey = {
                channel.key: channel for channel in allChannels}
            allMatrixChannelsByKey = {
                channel.key: channel for templateChannel in self.templateChannels for channel in templateChannel.createMatrixChannels()}
            
            for matkey, matrixChannel in allMatrixChannelsByKey.items():
                if matrixChannel.key in allChannelsByKey.keys():
                    overrideChannel = allChannelsByKey[matrixChannel.key]
                    overrideChannel.pixelKey = matrixChannel.pixelKey
                    del allChannelsByKey[matrixChannel.key]
                    allMatrixChannelsByKey[matkey] = overrideChannel

                def checker(channelKey):
                    if matrixChannel.key == channelKey:
                        return True
                    
                    otherChannel = allChannelsByKey.get(channelKey) or allMatrixChannelsByKey.get(channelKey)
                    if isinstance(otherChannel, SwitchingChannel) and matrixChannel.key in otherChannel.switchToChannelKeys:
                        return True
                    
                    return False
                
                matrixChannelUsed = any(any(checker(channelKey) for channelKey in mode.channelKeys) for mode in self.modes)

                if matrixChannelUsed:
                    allChannelsByKey[matrixChannel.key] = matrixChannel
            
            self._cache["allChannelsByKey"] = allChannelsByKey
        
        return self._cache["allChannelsByKey"]

    def _get_capabilities(self) -> 'list[Capability]':
        if not "capabilities" in self._cache.keys():
            channels: 'list[Union[CoarseChannel, TemplateChannel]]' = self.availableChannels + self.templateChannels
            self._cache["capabilities"] = list(chain.from_iterable(
                [channel.capabilities for channel in channels]))
        
        return self._cache["capabilities"]

    def _get_modes(self) -> 'list[Mode]':
        if not "modes" in self._cache.keys():
            self._cache["modes"] = [Mode(jsonMode, self) for jsonMode in self._jsonObject.get("modes", [])]
        
        return self._cache["modes"]

    manufacturer: 'Manufacturer' = property(_get_manufacturer, _set_manufacturer)
    key: str = property(_get_key)
    jsonObject: 'dict[str, Any]' = property(_get_jsonObject, _set_jsonObject)
    url: str = property(_get_url)
    name: str = property(_get_name)
    hasShortName: bool = property(_get_hasShortName)
    shortName: str = property(_get_shortName)
    categories: 'list[str]' = property(_get_categories)
    mainCategory: str = property(_get_mainCategory)
    meta: 'Meta' = property(_get_meta)
    hasComment: bool = property(_get_hasComment)
    comment: str = property(_get_comment)
    helpWanted: Optional[str] = property(_get_helpWanted)
    isHelpWanted: bool = property(_get_isHelpWanted)
    isCapabilityHelpWanted: bool = property(_get_isCapabilityHelpWanted)
    links: 'Optional[dict[str, list[str]]]' = property(_get_links)
    rdm: 'Optional[RDMInfo]' = property(_get_rdm)
    physical: 'Optional[Physical]' = property(_get_physical)
    matrix: 'Optional[Matrix]' = property(_get_matrix)
    wheels: 'list[Wheel]' = property(_get_wheels)
    uniqueChannelNames: 'dict[str, str]' = property(_get_uniqueChannelNames)
    availableChannelKeys: 'list[str]' = property(_get_availableChannelKeys)
    availableChannels: 'list[CoarseChannel]' = property(_get_availableChannels)
    coarseChannelKeys: 'list[str]' = property(_get_coarseChannelKeys)
    coarseChannels: 'list[CoarseChannel]' = property(_get_coarseChannels)
    fineChannelAliases: 'list[str]' = property(_get_fineChannelAliases)
    fineChannels: 'list[FineChannel]' = property(_get_fineChannels)
    switchingChannelAliases: 'list[str]' = property(_get_switchingChannelAliases)
    switchingChannels: 'list[SwitchingChannel]' = property(_get_switchingChannels)
    templateChannelKeys: 'list[str]' = property(_get_templateChannelKeys)
    templateChannels: 'list[TemplateChannel]' = property(_get_templateChannels)
    matrixChannelKeys: 'list[str]' = property(_get_matrixChannelKeys)
    matrixChannels: 'list[AbstractChannel]' = property(_get_matrixChannels)
    nullChannelKeys: 'list[str]' = property(_get_nullChannelKeys)
    nullChannels: 'list[NullChannel]' = property(_get_nullChannels)
    allChannelKeys: 'list[str]' = property(_get_allChannelKeys)
    allChannels: 'list[AbstractChannel]' = property(_get_allChannels)
    allChannelsByKey: 'dict[str, AbstractChannel]' = property(_get_allChannelsByKey)
    capabilities: 'list[Capability]' = property(_get_capabilities)
    modes: 'list[Mode]' = property(_get_modes)

    def getLinksOfType(self, type_: str) -> 'list[str]':
        '''Returns: list[str] - An array of URLs of the specified type (may be empty).'''
        if self.links == None:
            return []
        
        return self.links.get(type_, [])

    def getWheelByName(self, wheelName: str) -> Optional['Wheel']:
        '''Returns: Wheel | null - The wheel with the given name, or null if no wheel with the given name exists.'''
        if not "wheelByName" in self._cache.keys():
            self._cache["wheelByName"] = {wheel.name: wheel for wheel in self.wheels}
        
        return self._cache["wheelByName"].get(wheelName)

    def getTemplateChannelByKey(self, channelKey: str) -> Optional['TemplateChannel']:
        '''Searches the template channel with the given key. Fine and switching template channel aliases can't be found.
        Returns: TemplateChannel | null - The corresponding template channel.'''
        if not "templateChannelByKey" in self._cache.keys():
            self._cache["templateChannelByKey"] = {}

            for channel in self.templateChannels:
                self._cache["templateChannelByKey"][channel.key] = channel
            
        return self._cache["templateChannelByKey"]

    def getChannelByKey(self, key: str) -> Optional['AbstractChannel']:
        '''Returns: AbstractChannel | null - The found channel, null if not found.'''
        return self.allChannelsByKey.get(key)
