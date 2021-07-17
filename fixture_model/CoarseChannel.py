from .AbstractChannel import AbstractChannel
from .Capability import Capability
from .Entity import Entity
from .FineChannel import FineChannel
from .SwitchingChannel import SwitchingChannel, SwitchingChannelBehavior

from .scale_dmx_value import DmxScaler
scaleDmxValue = DmxScaler.scaleDmxValue

from typing import TYPE_CHECKING, Any, Literal, Optional
from numbers import Number
from math import floor
from itertools import chain

if TYPE_CHECKING:
    from .Fixture import Fixture
    from .Mode import Mode

channelTypeConstraints = {
    'Single Color': ['ColorIntensity'],
    'Multi-Color': {
        'required': ['ColorPreset', 'WheelSlot'],
        'predicate': lambda channel: all(cap.type != "WheelSlot" or (len(cap.wheels) > 0 and cap.wheels[0] and cap.wheels[0].type == "Color") for cap in channel.capabilities)
    },
    'Pan': ['Pan', 'PanContinuous'],
    'Tilt': ['Tilt', 'TiltContinuous'],
    'Focus': ['Focus'],
    'Zoom': ['Zoom'],
    'Iris': ['Iris', 'IrisEffect'],
    'Gobo': {
        'required': ['WheelSlot', 'WheelShake'],
        'predicate': lambda channel: all(all(wheel and wheel.type == "Gobo" for wheel in cap.wheels) for cap in channel.capabilities)
    },
    'Prism': ['Prism'],
    'Color Temperature': ['ColorTemperature'],
    'Effect': ['Effect', 'EffectParameter', 'Frost', 'FrostEffect', 'SoundSensitivity', 'WheelSlot'],
    'Strobe': {
        'required': ['ShutterStrobe'],
        'predicate': lambda channel: any(cap.type == "ShutterStrobe" and not cap.shutterEffect in ["Open", "Closed"] for cap in channel.capabilities)
    },
    'Shutter': ['ShutterStrobe', 'BladeInsertion', 'BladeRotation', 'BladeSystemRotation'],
    'Fog': ['Fog', 'FogOutput', 'FogType'],
    'Speed': ['StrobeSpeed', 'StrobeDuration', 'PanTiltSpeed', 'EffectSpeed', 'EffectDuration', 'BeamAngle', 'BeamPosition', 'PrismRotation', 'Rotation', 'Speed', 'Time', 'WheelSlotRotation', 'WheelRotation', 'WheelShake'],
    'Maintenance': ['Maintenance'],
    'Intensity': ['Intensity', 'Generic'],
    'NoFunction': ['NoFunction']
}


def _findIndex(flist, func):
    for i, v in enumerate(flist):
        if func(v):
            return i
    return -1



class Resolution(int):
    pass


RESOLUTION_8BIT: Resolution = Resolution(1)
RESOLUTION_16BIT: Resolution = Resolution(2)
RESOLUTION_24BIT: Resolution = Resolution(3)
RESOLUTION_32BIT: Resolution = Resolution(4)

class CoarseChannel(AbstractChannel):
    '''
    A single DMX channel, either created as availableChannel or resolved templateChannel.
    Only the MSB (most significant byte) channel if it's a multi-byte channel.
    '''

    _jsonObject: 'dict[str, Any]'
    _fixture: 'Fixture'
    _cache: 'dict[str, Any]'

    def __init__(self, key: str, jsonObject: 'dict[str, Any]', fixture: 'Fixture') -> None:
        super().__init__(key)
        self._jsonObject = jsonObject
        self._fixture = fixture
        self._cache = {}
    
    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject

    def _set_jsonObject(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}
    
    def _get_fixture(self) -> 'Fixture':
        return self._fixture

    def _get_name(self) -> str:
        return self._jsonObject.get("name", self.key)

    def _get_type(self) -> str:
        if not "type" in self._cache.keys():
            types = list(channelTypeConstraints.keys())
            def finder(type_):
                constraints = channelTypeConstraints[type_]

                if isinstance(constraints, list):
                    constraints = {
                        "required": constraints
                    }
                
                requiredCapabilityTypeUsed = any(cap.type in constraints["required"] for cap in self.capabilities)
                predicateFulfilled = not "predicate" in constraints or constraints["predicate"](self)

                return requiredCapabilityTypeUsed and predicateFulfilled
            i = _findIndex(types, finder)
            self._cache["type"] = types[i] if i >= 0 else "Unkown"
        
        return self._cache["type"]

    def _get_color(self) -> 'Optional[str]':
        if not "color" in self._cache.keys():
            colorCapability = self.capabilities[_findIndex(
                self.capabilities, lambda cap: cap.type == "ColorIntensity")]
            self._cache["color"] = colorCapability.color if colorCapability else None
        
        return self._cache["color"]

    def _get_fineChannelAliases(self) -> 'Optional[list[str]]':
        return self._jsonObject.get("fineChannelAliases") or []

    def _get_fineChannels(self) -> 'list[FineChannel]':
        if not "fineChannels" in self._cache.keys():
            self._cache["fineChannels"] = [FineChannel(alias, self) for alias in self.fineChannelAliases]
        
        return self._cache["fineChannels"]

    def _get_maxResolution(self) -> Resolution:
        return Resolution(1 + len(self.fineChannelAliases))

    def _get_dmxValueResolution(self) -> Resolution:
        if not "dmxValueResolution" in self._cache.keys():
            if "dmxValueResolution" in self._jsonObject.keys():
                resolutionStringToResolution = {
                    '8bit': RESOLUTION_8BIT,
                    '16bit': RESOLUTION_16BIT,
                    '24bit': RESOLUTION_24BIT,
                }

                self._cache["dmxValueResolution"] = resolutionStringToResolution[self._jsonObject["dmxValueResolution"]]
            else:
                self._cache["dmxValueResolution"] = self.maxResolution
        
        return self._cache["dmxValueResolution"]

    def _get_maxDmxBound(self) -> int:
        return 256**self.maxResolution - 1

    def _get_hasDefaultValue(self) -> bool:
        return "defaultValue" in self._jsonObject.keys()

    def _get_defaultValue(self) -> int:
        return self.getDefaultValueWithResolution(self.maxResolution)

    def _get_hasHighlightValue(self) -> bool:
        return "highlightValue" in self._jsonObject.keys()
    
    def _get_highlightValue(self) -> int:
        return self.getHighlightValueWithResolution(self.maxResolution)

    def _get_isInverted(self) -> bool:
        if not "isInverted" in self._cache.keys():
            proportionalCapabilities = list(filter(lambda cap: not cap.isStep, self.capabilities))
            
            self._cache["isInverted"] = len(proportionalCapabilities) > 0 and all(cap.isInverted for cap in proportionalCapabilities)
        
        return self._cache["isInverted"]

    def _get_isConstant(self) -> bool:
        return "constant" in self._jsonObject.keys() and self._jsonObject["constant"]

    def _get_canCrossfade(self) -> bool:
        if not "canCrossfade" in self._cache.keys():
            self._cache["canCrossfade"] = not self.isConstant and self.type != "NoFunction" if len(self.capabilities) == 1 else all(
                index + 1 == len(self.capabilities) or cap.canCrossfadeTo(self.capabilities[index + 1]) for index, cap in enumerate(self.capabilities)) and any(not cap.isStep for cap in self.capabilities)

        return self._cache["canCrossfade"]

    def _get_precedence(self) -> 'Literal["HTP", "LTP"]':
        return self._jsonObject.get("precedence", "LTP") or "LTP"

    def _get_switchingChannelAliases(self) -> 'list[str]':
        if not "switchingChannelAliases" in self._cache.keys():
            self._cache["switchingChannelAliases"] = list(self.capabilities[0].switchChannels.keys())
        
        return self._cache["switchingChannelAliases"]
    
    def _get_switchingChannels(self) -> 'list[SwitchingChannel]':
        if not "switchingChannels" in self._cache.keys():
            self._cache["switchingChannels"] = [SwitchingChannel(alias, self) for alias in self.switchingChannelAliases]
        
        return self._cache["switchingChannels"]

    def _get_switchToChannelKeys(self) -> 'list[str]':
        if not "switchToChannelKeys" in self._cache.keys():
            self._cache["switchToChannelKeys"] = list(chain.from_iterable([switch.switchToChannelKeys for switch in self.switchingChannels]))
        
        return self._cache["switchToChannelKeys"]

    def _get_capabilities(self) -> 'list[Capability]':
        if not "capabilities" in self._cache.keys():
            if "capability" in self._jsonObject.keys():
                capabilityData = {"dmxRange": [
                    0, 256**self.dmxValueResolution - 1], **self._jsonObject["capability"]}
                self._cache["capabilities"] = [Capability(
                    capabilityData, self.dmxValueResolution, self)]
            else:
                self._cache["capabilities"] = [
                    Capability(cap, self.dmxValueResolution, self) for cap in self._jsonObject.get("capabilities", [])]

        return self._cache["capabilities"]

    def _get_isHelpWanted(self) -> bool:
        if not "isHelpWanted" in self._cache.keys():
            self._cache["isHelpWanted"] = any(cap.helpWanted != None for cap in self.capabilities)

        return self._cache["isHelpWanted"]

    jsonObject: 'dict[str, Any]' = property(_get_jsonObject, _set_jsonObject)
    fixture: 'Fixture' = property(_get_fixture)
    type: str = property(_get_type)
    color: 'Optional[str]' = property(_get_color)
    fineChannelAliases: 'Optional[list[str]]' = property(_get_fineChannelAliases)
    fineChannels: 'list[FineChannel]' = property(_get_fineChannels)
    maxResolution: Resolution = property(_get_maxResolution)
    dmxValueResolution: Resolution = property(_get_dmxValueResolution)
    maxDmxBound: int = property(_get_maxDmxBound)
    hasDefaultValue: bool = property(_get_hasDefaultValue)
    defaultValue: int = property(_get_defaultValue)
    hasHighlightValue: bool = property(_get_hasHighlightValue)
    highlightValue: int = property(_get_highlightValue)
    isInverted: bool = property(_get_isInverted)
    isConstant: bool = property(_get_isConstant)
    canCrossfade: bool = property(_get_canCrossfade)
    precedence: 'Literal["HTP", "LTP"]' = property(_get_precedence)
    switchingChannelAliases: 'list[str]' = property(
        _get_switchingChannelAliases)
    switchingChannels: 'list[SwitchingChannel]' = property(
        _get_switchingChannels)
    switchToChannelKeys: 'list[str]' = property(_get_switchToChannelKeys)
    capabilities: 'list[Capability]' = property(_get_capabilities)
    isHelpWanted: bool = property(_get_isHelpWanted)

    def ensureProperResolution(self, uncheckedResolution: Resolution) -> None:
        if uncheckedResolution > self.maxResolution or uncheckedResolution < RESOLUTION_8BIT or uncheckedResolution % 1 != 0:
            raise ValueError(
                "resolution must be a positive integer not greater than maxResolution")

    def getResolutionInMode(self, mode: 'Mode', switchingChannelBehavior: SwitchingChannelBehavior) -> Resolution:
        channelKeys = [self.key] + self.fineChannelAliases
        usedChannels = list(filter(lambda channelKey: mode.getChannelIndex(channelKey, switchingChannelBehavior) != -1), channelKeys)

        return len(usedChannels)

    def getDefaultValueWithResolution(self, desiredResolution: Resolution) -> int:
        self.ensureProperResolution(desiredResolution)

        if not "defaultValuePerResolution" in self._cache.keys():
            rawDefaultValue = self._jsonObject.get("defaultValue", 0) or 0

            if not isinstance(rawDefaultValue, int):
                percentage = Entity.createFromEntityString(
                    rawDefaultValue).number / 100
                rawDefaultValue = floor(
                    percentage * (256 ** self.dmxValueResolution) - 1)

            self._cache["defaultValuePerResolution"] = {}
            for index in range(1, self.maxResolution + 1):
                self._cache["defaultValuePerResolution"][index] = scaleDmxValue(
                    rawDefaultValue, self.dmxValueResolution, index)

        return self._cache["defaultValuePerResolution"][desiredResolution]

    def getHighlightValueWithResolution(self, desiredResolution: Resolution) -> int:
        self.ensureProperResolution(desiredResolution)

        if not "highlightValuePerResolution" in self._cache.keys():
            rawHighlightValue = self._jsonObject.get("highlightValue")

            if not isinstance(rawHighlightValue, int):
                maxDmxBoundInResolution = 256**self.dmxValueResolution - 1

                if self.hasHighlightValue:
                    percentage = Entity.createFromEntityString(rawHighlightValue).number / 100
                    rawHighlightValue = floor(percentage * maxDmxBoundInResolution)
                else:
                    rawHighlightValue = maxDmxBoundInResolution
            
            self._cache["highlightValuePerResolution"] = {}
            for index in range(1, self.maxResolution + 1):
                self._cache["highlightValuePerResolution"][index] = scaleDmxValue(rawHighlightValue, self.dmxValueResolution, index)
            
        return self._cache["highlightValuePerResolution"][desiredResolution]
