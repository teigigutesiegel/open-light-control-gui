from typing import Iterable, TYPE_CHECKING, Optional, Literal, Any, Callable, Union
from .Entity import Entity
from .Range import Range

from .scale_dmx_value import DmxScaler
from numbers import Number
import re
scaleDmxRange = DmxScaler.scaleDmxRange


if TYPE_CHECKING:
    from .CoarseChannel import CoarseChannel
    from .Wheel import Wheel
    from .WheelSlot import WheelSlot


class Resolution(int):
    pass


START_END_ENTITIES = ['speed', 'duration', 'time', 'brightness', 'slotNumber', 'angle', 'horizontalAngle', 'verticalAngle', 'colorTemperature',
                      'soundSensitivity', 'shakeAngle', 'shakeSpeed', 'distance', 'openPercent', 'frostIntensity', 'insertion', 'fogOutput', 'parameter']

Colors = Optional[Literal['Red', 'Green', 'Blue', 'Cyan', 'Magenta', 'Yellow',
                          'Amber', 'White', 'Warm White', 'Cold White', 'UV', 'Lime', 'Indigo']]


def _flatter(array: list) -> list:
    ret_array = []
    for ele in array:
        if isinstance(ele, list):
            ret_array.extend(ele)
        else:
            ret_array.append(ele)
    return ret_array


def appendInBrackets(string: str, *inBrackets: 'str') -> str:
    inBrackets_ = list(filter(
        lambda inBracket: inBracket and inBracket != None and inBracket != "", inBrackets))

    if len(inBrackets_) == 0:
        return string

    return f"{string} ({', '.join(inBrackets_)})"


def getSlotCapabilityName(cap: 'Capability') -> str:
    '''returns the name for the cap, without the comment appended (if any).'''
    if cap.wheelSlot == None:
        return "Unkown wheel slot"

    return cap.wheelSlot[0].name if cap.slotNumber[0].number == cap.slotNumber[1].number else " ... ".join(slot.name for slot in cap.wheelSlot)


def startEndToString(startend: 'tuple[Entity, Entity]', propertyName: 'Optional[str]' = None, propertyNameBeforeValue: bool = False) -> str:
    start, end = startend

    def handleKeywords() -> str:
        if start == end:
            return start.keyword

        hasSpecifier = re.compile(" (?:CW|CCW|reverse)$")
        if hasSpecifier.match(start.keyword) and hasSpecifier.match(end.keyword):
            speedStart, specifierStart = start.keyword.split(" ")
            speedEnd, specifierEnd = end.keyword.split(" ")

            if specifierStart == specifierEnd:
                return f"{specifierStart} {speedStart}...{speedEnd}"

        return f"{start.keyword}...{end.keyword}"

    if start.keyword:
        return handleKeywords()

    unitAliases = {
        'deg': '°',
        'm^3/min': 'm³/min',
    }

    unit = unitAliases.get(start.unit, start.unit)
    words = []

    if not start == end:
        words.append(f"{start.number}...{end.number}{unit}")
    else:
        words.append(f"{start.number}{unit}")

    if propertyName and unit == "%":
        words.append(propertyName)

    if propertyNameBeforeValue:
        words.reverse()

    return " ".join(words)


def colorTemperaturesToString(startend: 'tuple[Entity, Entity]') -> str:
    start, end = startend

    def colorTemperatureToString(temperature: Number) -> str:
        if temperature < 0:
            return f"{-temperature}% warm"
        if temperature > 0:
            return f"{temperature}% cold"
        return "default"

    if start.keyword or start.unit != "%":
        return startEndToString(startend)

    if start == end:
        return colorTemperatureToString(start.number)

    if start <= 0:
        if end <= 0:
            return f"{-start}...{-end}% warm"
        return f"{-start}% warm ... {end}% cold"

    if end <= 0:
        return f"{start}% cold ... {-end}% warm"

    return f"{start}...{end}% cold"


def _ShutterStrobe(cap: 'Capability') -> str:
    name = {
        "Open": 'Shutter open',
        "Closed": 'Shutter closed',
        "Strobe": 'Strobe',
        "Pulse": 'Pulse strobe',
        "RampUp": 'Ramp up strobe',
        "RampDown": 'Ramp down strobe',
        "RampUpDown": 'Ramp up and down strobe',
        "Lightning": 'Lightning strobe effect',
        "Spikes": 'Spikes strobe effect',
    }[cap.shutterEffect]

    if cap.randomTiming:
        name = f"Random {name.lower()}"

    if cap.isSoundControlled:
        name += ' sound-controlled'

    if cap.speed:
        name += f" {startEndToString(cap.speed, 'speed')}"

    if cap.duration:
        name += f" {startEndToString(cap.duration, 'duration')}"

    return appendInBrackets(name, cap.comment)


def _ColorPreset(cap: 'Capability') -> str:
    name = cap.comment or "Color preset"

    if cap.colorTemperature:
        name += f" ({colorTemperaturesToString(cap.colorTemperature)})"

    return name


def _PanTiltSpeed(cap: 'Capability') -> str:
    speedOrDuration = "speed" if cap.speed != None else "duration"
    name = "Pan/tilt movement "

    if getattr(cap, speedOrDuration)[0].keyword == None and getattr(cap, speedOrDuration)[0].unit == "%":
        name += "{speedOrDuration} "

    name += startEndToString(getattr(cap, speedOrDuration))

    return appendInBrackets(name, cap.comment)


def _WheelShake(cap: 'Capability') -> str:
    name = getSlotCapabilityName(cap) if cap.slotNumber else ", ".join(
        wheel.name for wheel in cap.wheels)

    if cap.isShaking == "slot":
        name += " slot"

    name += " shake"

    if cap.shakeAngle:
        name += f" {startEndToString(cap.shakeAngle, 'angle', True)}"

    if cap.shakeSpeed:
        name += f" {startEndToString(cap.shakeSpeed, 'speed', True)}"

    return appendInBrackets(name, cap.comment)


def _WheelSlotRotation(cap: 'Capability') -> str:
    if cap.wheelSlot:
        wheelSlotName = cap.wheelSlot[0].name
    elif cap.wheels[0]:
        wheelSlotName = cap.wheels[0].type.replace("Gobo", "Gobo stencil")
    else:
        wheelSlotName = 'Wheel slot'

    speedOrAngle = 'speed' if cap.speed != None else 'angle'
    return appendInBrackets(f"{wheelSlotName} rotation {startEndToString(getattr(cap, speedOrAngle), speedOrAngle, True)}", cap.comment)


def _WheelRotation(cap: 'Capability') -> str:
    speedOrAngle = 'speed' if cap.speed != None else 'angle'
    return appendInBrackets(f"{cap.wheels[0].name if cap.wheels[0] else 'Wheel'} rotation {startEndToString(getattr(cap, speedOrAngle), speedOrAngle, True)}", cap.comment)


def _Effect(cap: 'Capability') -> str:
    name = cap.effectName

    if cap.effectPreset != None and cap.isSoundControlled:
        name += ' sound-controlled'

    if cap.parameter:
        name += f" {startEndToString(cap.parameter)}"

    if cap.speed:
        name += f" {startEndToString(cap.speed, 'speed')}"

    if cap.duration:
        name += f" {startEndToString(cap.duration, 'duration')}"

    soundSensitivity = None
    if cap.soundSensitivity:
        soundSensitivity = f'sound sensitivity {startEndToString(cap.soundSensitivity)}'

    return appendInBrackets(name, soundSensitivity, cap.comment)


def _BeamPosition(cap: 'Capability') -> str:
    if cap.horizontalAngle and cap.verticalAngle:
      return appendInBrackets(f"Beam position ({startEndToString(cap.horizontalAngle)}, {startEndToString(cap.verticalAngle)})", cap.comment)

    orientation = "Horizontal" if cap.horizontalAngle else "Vertical"
    angleStartEnd = getattr(cap, f"{orientation.lower()}Angle")

    hasOrientationKeyword = any(
        entity.keyword != None and entity.keyword != "center" for entity in angleStartEnd)
    prefix = "Beam position" if hasOrientationKeyword else f"{orientation} beam position"
    return appendInBrackets(f"{prefix} {startEndToString(angleStartEnd)}", cap.comment)


def _IrisEffect(cap: 'Capability') -> str:
    name = f"Iris {cap.effectName}"

    if cap.speed:
      name += f" {startEndToString(cap.speed, 'speed')}"

    return appendInBrackets(name, cap.comment)


def _FrostEffect(cap: 'Capability') -> str:
    name = f"Frost {cap.effectName}"

    if cap.speed:
      name += f" {startEndToString(cap.speed, 'speed')}"

    return appendInBrackets(name, cap.comment)


def _Prism(cap: 'Capability') -> str:
    name = "Prism"

    if cap.speed:
      name += f" {startEndToString(cap.speed, 'speed')}"
    elif cap.angle:
      name += f" {startEndToString(cap.angle, 'angle')}"

    return appendInBrackets(name, cap.comment)


def _PrismRotation(cap: 'Capability') -> str:
    speedOrAngle = "speed" if cap.speed != None else "angle"
    return appendInBrackets(f"Prism rotation {startEndToString(getattr(cap, speedOrAngle), speedOrAngle, True)}", cap.comment)


def _Fog(cap: 'Capability') -> str:
    name = cap.fogType or "Fog"

    if cap.fogOutput:
      name += f" {startEndToString(cap.fogOutput)}"

    return appendInBrackets(name, cap.comment)


def _Rotation(cap: 'Capability') -> str:
    speedOrAngle = "speed" if cap.speed != None else "angle"
    return appendInBrackets(f"Rotation {startEndToString(getattr(cap, speedOrAngle), speedOrAngle, True)}", cap.comment)


def _Maintenance(cap: 'Capability') -> str:
    name = cap.comment or "Maintenance"

    if cap.parameter:
      name += f" {startEndToString(cap.parameter)}"

    holdString = None
    if cap.hold:
      holdString = f"hold {startEndToString([cap.hold, cap.hold])}"

    return appendInBrackets(name, holdString)


namePerType: 'dict[str, Callable[[Capability], str]]' = {
    "NoFunction": lambda cap: cap.comment or "No Function",
    "ShutterStrobe": _ShutterStrobe,
    "StrobeSpeed": lambda cap: appendInBrackets(f"Strobe speed {startEndToString(cap.speed)}", cap.comment),
    "StrobeDuration": lambda cap: appendInBrackets(f"Strobe duration {startEndToString(cap.duration)}", cap.comment),
    "Intensity": lambda cap: appendInBrackets(f"Intensity {startEndToString(cap.brightness)}", cap.comment),
    "ColorIntensity": lambda cap: appendInBrackets(f"{cap.color} {startEndToString(cap.brightness)}", cap.comment),
    "ColorPreset": _ColorPreset,
    "ColorTemperature": lambda cap: appendInBrackets(f"Color temperature {startEndToString(cap.colorTemperature)}", cap.comment),
    "Pan": lambda cap: appendInBrackets(f"Pan {startEndToString(cap.angle, 'angle', True)}", cap.comment),
    "PanContinuous": lambda cap: appendInBrackets(f"Pan {startEndToString(cap.speed, 'speed', True)}", cap.comment),
    "Tilt": lambda cap: appendInBrackets(f"Tilt {startEndToString(cap.angle, 'angle', True)}", cap.comment),
    "TiltContinuous": lambda cap: appendInBrackets(f"Tilt {startEndToString(cap.speed, 'speed', True)}", cap.comment),
    "PanTiltSpeed": _PanTiltSpeed,
    "WheelSlot": lambda cap: appendInBrackets(getSlotCapabilityName(cap), cap.comment),
    "WheelShake": _WheelShake,
    "WheelSlotRotation": _WheelSlotRotation,
    "WheelRotation": _WheelRotation,
    "Effect": _Effect,
    "EffectSpeed": lambda cap: appendInBrackets(f"Effect speed {startEndToString(cap.speed)}", cap.comment),
    "EffectDuration": lambda cap: appendInBrackets(f"Effect duration {startEndToString(cap.duration)}", cap.comment),
    "EffectParameter": lambda cap: f"{cap.comment or 'Effect parameter'} {startEndToString(cap.parameter)}",
    "SoundSensitivity": lambda cap: appendInBrackets(f"Sound sensitivity {startEndToString(cap.soundSensitivity)}", cap.comment),
    "BeamAngle": lambda cap: appendInBrackets(f"Beam {startEndToString(cap.angle, 'angle', True)}", cap.comment),
    "BeamPosition": _BeamPosition,
    "Focus": lambda cap: appendInBrackets(f"Focus {startEndToString(cap.distance, 'distance')}", cap.comment),
    "Zoom": lambda cap: appendInBrackets(f"Zoom {startEndToString(cap.angle, 'beam angle')}", cap.comment),
    "Iris": lambda cap: appendInBrackets(f"Iris {startEndToString(cap.openPercent, 'open')}", cap.comment),
    "IrisEffect": _IrisEffect,
    "Frost": lambda cap: appendInBrackets(f"Frost {startEndToString(cap.frostIntensity)}", cap.comment),
    "FrostEffect": _FrostEffect,
    "Prism": _Prism,
    "PrismRotation": _PrismRotation,
    "BladeInsertion": lambda cap: appendInBrackets(f"Blade {cap.blade} insertion {startEndToString(cap.insertion)}", cap.comment),
    "BladeRotation": lambda cap: appendInBrackets(f"Blade {cap.blade} rotation {startEndToString(cap.angle, 'angle', True)}", cap.comment),
    "BladeSystemRotation": lambda cap: appendInBrackets(f"Blade system rotation {startEndToString(cap.angle, 'angle', True)}", cap.comment),
    "Fog": _Fog,
    "FogOutput": lambda cap: appendInBrackets(f"Fog output {startEndToString(cap.fogOutput)}", cap.comment),
    "FogType": lambda cap: appendInBrackets(f"Fog type: {cap.fogType}", cap.comment),
    "Rotation": _Rotation,
    "Speed": lambda cap: appendInBrackets(f"Speed {startEndToString(cap.speed)}", cap.comment),
    "Time": lambda cap: appendInBrackets(f"Time {startEndToString(cap.time)}", cap.comment),
    "Maintenance": _Maintenance,
    "Generic": lambda cap: cap.comment or "Generic",
}


class Capability():
    START_END_ENTITIES = START_END_ENTITIES

    _jsonObject: 'dict[str, Any]'
    _resolution: Resolution
    _channel: 'CoarseChannel'
    _cache: 'dict[str, Any]'

    def __init__(self, jsonObject: 'dict[str, Any]', resolution: Resolution, channel: 'CoarseChannel') -> None:
        self.jsonObject = jsonObject
        self._resolution = resolution
        self._channel = channel

    def __str__(self) -> str:
        return f"Capability <{self.name}>"

    def __format__(self, format_spec: str) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def _get_jsonObject(self) -> 'dict[str, Any]':
        return self._jsonObject

    def _set_jsonObject(self, jsonObject: 'dict[str, Any]') -> None:
        self._jsonObject = jsonObject
        self._cache = {}
        self._cache["dmxRangePerResolution"] = {}

    def _get_dmxRange(self) -> Range:
        return self.getDmxRangeWithResolution(self._channel.maxResolution)

    def _get_rawDmxRange(self) -> Range:
        return self.getDmxRangeWithResolution(self._resolution)

    def _get_type(self) -> str:
        return self._jsonObject["type"]

    def _get_name(self) -> str:
        if not "name" in self._cache.keys():
            self._cache["name"] = namePerType[self.type](
                self) if self.type in namePerType.keys() else f"{self.type}: {self.comment}"

        return self._cache["name"]

    def _get_hasComment(self) -> bool:
        return "comment" in self._jsonObject.keys()

    def _get_comment(self) -> str:
        return self._jsonObject.get("comment", "")

    def _get_isStep(self) -> bool:
        if not "isStep" in self._cache.keys():
            steppedStartEndProperties = all(getattr(self, prop)[0].number == getattr(
                self, prop)[1].number for prop in self.usedStartEndEntities)
            steppedColors = not self.colors or self.colors.get("isStep")
            
            self._cache["isStep"] = steppedStartEndProperties and steppedColors

        return self._cache["isStep"]

    def _get_isInverted(self) -> bool:
        if not "isInverted" in self._cache.keys():
            if self.isStep:
                self._cache["isInverted"] = False
            else:
                proportionalProperties = [prop for prop in self.usedStartEndEntities if getattr(
                    self, prop)[0].number != getattr(self, prop)[1].number]

                self._cache["isInverted"] = len(proportionalProperties) > 0 and all(
                    abs(getattr(self, prop)[0].number) > abs(getattr(self, prop)[1].number) for prop in proportionalProperties)

        return self._cache["isInverted"]

    def _get_usedStartEndEntities(self) -> 'list[str]':
        if not "usedStartEndEntities" in self._cache.keys():
            self._cache["usedStartEndEntities"] = []
            for prop in Capability.START_END_ENTITIES:
                if getattr(self, prop, None):
                    self._cache["usedStartEndEntities"].append(prop)

        return self._cache["usedStartEndEntities"]

    def _get_helpWanted(self) -> 'Optional[str]':
        return self._jsonObject.get("helpWanted")

    def _get_menuClick(self) -> "Literal['start', 'center', 'end', 'hidden']":
        return self._jsonObject.get("menuClick", "start")

    def _get_menuClickDmxValue(self) -> int:
        return self.getMenuClickDmxValueWithResolution(self._channel.maxResolution)

    def _get_switchChannels(self) -> 'dict[str, str]':
        return self._jsonObject.get("switchChannels", {})

    jsonObject: 'dict[str, Any]' = property(_get_jsonObject, _set_jsonObject)
    dmxRange: Range = property(_get_dmxRange)
    rawDmxRange: Range = property(_get_rawDmxRange)
    type: str = property(_get_type)
    name: str = property(_get_name)
    hasComment: bool = property(_get_hasComment)
    comment: str = property(_get_comment)
    isStep: bool = property(_get_isStep)
    isInverted: bool = property(_get_isInverted)
    usedStartEndEntities: 'list[str]' = property(_get_usedStartEndEntities)
    helpWanted: 'Optional[str]' = property(_get_helpWanted)
    menuClick: "Literal['start', 'center', 'end', 'hidden']" = property(
        _get_menuClick)
    menuClickDmxValue: int = property(_get_menuClickDmxValue)
    switchChannels: 'dict[str, str]' = property(_get_switchChannels)

    # TYPE-SPECIFIC PROPERTIES (no start-end)
    def _get_shutterEffect(self) -> 'Optional[str]':
        return self._jsonObject.get("shutterEffect")

    def _get_color(self) -> Colors:
        return self._jsonObject.get("color")

    def _get_colors(self) -> 'Optional[dict[str, Any]]':
        if not "colors" in self._cache.keys():
            startColors = self._jsonObject.get("colors")
            endColors = self._jsonObject.get("colors")
            isStep = True

            if self.wheelSlot != None and self.wheelSlot[0].colors != None and self.wheelSlot[1].colors != None:
                startColors = self.wheelSlot[0].colors
                endColors = self.wheelSlot[1].colors
                isStep = self.slotNumber[0].number == self.slotNumber[1].number
            elif "colorsStart" in self._jsonObject.keys():
                startColors = self._jsonObject["colorsStart"]
                endColors = self._jsonObject["colorsEnd"]
                isStep = False

            self._cache["colors"] = {
                "startColors": startColors,
                "endColors": endColors,
                "allColors": startColors + [] if isStep else startColors + endColors,
                "isStep": isStep
            } if startColors else None

        return self._cache["colors"]

    def _get_wheels(self) -> 'list[Wheel]':
        if not "wheels" in self._cache.keys():
            if "wheel" in self._jsonObject.keys():
                wheelNames = _flatter([self._jsonObject["wheel"]])
            elif "Wheel" in self.type:
                wheelNames = [self._channel.name]
            else:
                wheelNames = []

            self._cache["wheels"] = [self._channel.fixture.getWheelByName(
                wheelName) for wheelName in wheelNames]

        return self._cache["wheels"]

    def _get_isShaking(self) -> 'Literal["slot", "wheel"]':
        return self._jsonObject.get("isShaking", "wheel")

    def _get_effectName(self) -> 'Optional[str]':
        if not "effectName" in self._cache.keys():
            if "effectName" in self._jsonObject.keys():
                self._cache["effectName"] = self._jsonObject["effectName"]
            elif "effectPreset" in self._jsonObject.keys():
                self._cache["effectName"] = {
                    "ColorFade": "Color fade",
                    "ColorJump": "Color jump"
                }.get(self._jsonObject["effectPreset"])
            else:
                self._cache["effectName"] = None

        return self._cache["effectName"]

    def _get_effectPreset(self) -> 'Optional[str]':
        return self._jsonObject.get("effectPreset")

    def _get_isSoundControlled(self) -> 'Optional[bool]':
        return self._jsonObject.get("isSoundControlled")

    def _get_randomTiming(self) -> 'Optional[bool]':
        return self._jsonObject.get("randomTiming") == True

    def _get_blade(self) -> "Optional[Union[Literal['Top', 'Right', 'Bottom', 'Left'], Number]]":
        return self._jsonObject.get("blade")

    def _get_fogType(self) -> "Optional[Literal['Fog', 'Haze']]":
        return self._jsonObject.get("fogType")

    def _get_hold(self) -> 'Optional[Entity]':
        if not "hold" in self._cache.keys():
            self._cache["hold"] = Entity.createFromEntityString(
                self._jsonObject["hold"]) if "hold" in self._jsonObject.keys() else None

        return self._cache["hold"]

    shutterEffect: 'Optional[str]' = property(_get_shutterEffect)
    color: Colors = property(_get_color)
    colors: 'Optional[dict[str, Any]]' = property(_get_colors)
    wheels: 'list[Wheel]' = property(_get_wheels)
    isShaking: 'Literal["slot", "wheel"]' = property(_get_isShaking)
    effectName: 'Optional[str]' = property(_get_effectName)
    effectPreset: 'Optional[str]' = property(_get_effectPreset)
    isSoundControlled: 'Optional[bool]' = property(_get_isSoundControlled)
    randomTiming: 'Optional[bool]' = property(_get_randomTiming)
    blade: "Optional[Union[Literal['Top', 'Right', 'Bottom', 'Left'], Number]]" = property(
        _get_blade)
    fogType: "Optional[Literal['Fog', 'Haze']]" = property(_get_fogType)
    hold: 'Optional[Entity]' = property(_get_hold)

    def _get_speed(self) -> 'Optional[list[Entity]]':
        if not 'speed' in self._cache.keys():
            self._cache['speed'] = self._getStartEndArray('speed')

        return self._cache['speed']

    def _get_duration(self) -> 'Optional[list[Entity]]':
        if not 'duration' in self._cache.keys():
            self._cache['duration'] = self._getStartEndArray('duration')

        return self._cache['duration']

    def _get_time(self) -> 'Optional[list[Entity]]':
        if not 'time' in self._cache.keys():
            self._cache['time'] = self._getStartEndArray('time')

        return self._cache['time']

    def _get_brightness(self) -> 'Optional[list[Entity]]':
        if not 'brightness' in self._cache.keys():
            brightness = self._getStartEndArray('brightness')

            if brightness == None and self.type in ['Intensity', 'ColorIntensity']:
                brightness = [Entity.createFromEntityString(
                    'off'), Entity.createFromEntityString("bright")]

            self._cache['brightness'] = brightness

        return self._cache['brightness']

    def _get_slotNumber(self) -> 'Optional[list[Entity]]':
        if not 'slotNumber' in self._cache.keys():
            self._cache['slotNumber'] = self._getStartEndArray('slotNumber')

        return self._cache['slotNumber']

    def _get_wheelSlot(self) -> 'Optional[list[WheelSlot]]':
        if self.slotNumber == None:
            return None

        if len(self.wheels) != 1:
            raise ValueError(
                'When accessing the current wheel slot, the referenced wheel must be unambiguous.')

        if not 'wheelSlot' in self._cache.keys():
            self._cache['wheelSlot'] = [self.wheels[0].getSlot(
                slotNumber.number) for slotNumber in self.slotNumber] if self.wheels[0] else None

        return self._cache['wheelSlot']

    def _get_angle(self) -> 'Optional[list[Entity]]':
        if not 'angle' in self._cache.keys():
            self._cache['angle'] = self._getStartEndArray('angle')

        return self._cache['angle']

    def _get_horizontalAngle(self) -> 'Optional[list[Entity]]':
        if not 'horizontalAngle' in self._cache.keys():
            self._cache['horizontalAngle'] = self._getStartEndArray(
                'horizontalAngle')

        return self._cache['horizontalAngle']

    def _get_verticalAngle(self) -> 'Optional[list[Entity]]':
        if not 'verticalAngle' in self._cache.keys():
            self._cache['verticalAngle'] = self._getStartEndArray(
                'verticalAngle')

        return self._cache['verticalAngle']

    def _get_colorTemperature(self) -> 'Optional[list[Entity]]':
        if not 'colorTemperature' in self._cache.keys():
            self._cache['colorTemperature'] = self._getStartEndArray(
                'colorTemperature')

        return self._cache['colorTemperature']

    def _get_soundSensitivity(self) -> 'Optional[list[Entity]]':
        if not 'soundSensitivity' in self._cache.keys():
            self._cache['soundSensitivity'] = self._getStartEndArray(
                'soundSensitivity')

        return self._cache['soundSensitivity']

    def _get_shakeAngle(self) -> 'Optional[list[Entity]]':
        if not 'shakeAngle' in self._cache.keys():
            self._cache['shakeAngle'] = self._getStartEndArray('shakeAngle')

        return self._cache['shakeAngle']

    def _get_shakeSpeed(self) -> 'Optional[list[Entity]]':
        if not 'shakeSpeed' in self._cache.keys():
            self._cache['shakeSpeed'] = self._getStartEndArray('shakeSpeed')

        return self._cache['shakeSpeed']

    def _get_distance(self) -> 'Optional[list[Entity]]':
        if not 'distance' in self._cache.keys():
            self._cache['distance'] = self._getStartEndArray('distance')

        return self._cache['distance']

    def _get_openPercent(self) -> 'Optional[list[Entity]]':
        if not 'openPercent' in self._cache.keys():
            self._cache['openPercent'] = self._getStartEndArray('openPercent')

        return self._cache['openPercent']

    def _get_frostIntensity(self) -> 'Optional[list[Entity]]':
        if not 'frostIntensity' in self._cache.keys():
            self._cache['frostIntensity'] = self._getStartEndArray(
                'frostIntensity')

        return self._cache['frostIntensity']

    def _get_insertion(self) -> 'Optional[list[Entity]]':
        if not 'insertion' in self._cache.keys():
            self._cache['insertion'] = self._getStartEndArray('insertion')

        return self._cache['insertion']

    def _get_fogOutput(self) -> 'Optional[list[Entity]]':
        if not 'fogOutput' in self._cache.keys():
            self._cache['fogOutput'] = self._getStartEndArray('fogOutput')

        return self._cache['fogOutput']

    def _get_parameter(self) -> 'Optional[list[Entity]]':
        if not 'parameter' in self._cache.keys():
            self._cache['parameter'] = self._getStartEndArray('parameter')

        return self._cache['parameter']

    speed: 'Optional[list[Entity]]' = property(_get_speed)
    duration: 'Optional[list[Entity]]' = property(_get_duration)
    time: 'Optional[list[Entity]]' = property(_get_time)
    brightness: 'Optional[list[Entity]]' = property(_get_brightness)
    slotNumber: 'Optional[list[Entity]]' = property(_get_slotNumber)
    wheelSlot: 'Optional[list[WheelSlot]]' = property(_get_wheelSlot)
    angle: 'Optional[list[Entity]]' = property(_get_angle)
    horizontalAngle: 'Optional[list[Entity]]' = property(_get_horizontalAngle)
    verticalAngle: 'Optional[list[Entity]]' = property(_get_verticalAngle)
    colorTemperature: 'Optional[list[Entity]]' = property(
        _get_colorTemperature)
    soundSensitivity: 'Optional[list[Entity]]' = property(
        _get_soundSensitivity)
    shakeAngle: 'Optional[list[Entity]]' = property(_get_shakeAngle)
    shakeSpeed: 'Optional[list[Entity]]' = property(_get_shakeSpeed)
    distance: 'Optional[list[Entity]]' = property(_get_distance)
    openPercent: 'Optional[list[Entity]]' = property(_get_openPercent)
    frostIntensity: 'Optional[list[Entity]]' = property(_get_frostIntensity)
    insertion: 'Optional[list[Entity]]' = property(_get_insertion)
    fogOutput: 'Optional[list[Entity]]' = property(_get_fogOutput)
    parameter: 'Optional[list[Entity]]' = property(_get_parameter)

    def getDmxRangeWithResolution(self, desiredResolution: int) -> 'Range':
        '''Returns: Range - The cap's DMX bounds scaled (down) to the given resolution.'''
        self._channel.ensureProperResolution(desiredResolution)

        if not self._cache["dmxRangePerResolution"].get(desiredResolution):
            self._cache["dmxRangePerResolution"][desiredResolution] = Range(scaleDmxRange(
                self._jsonObject["dmxRange"][0], self._jsonObject["dmxRange"][1], self._resolution, desiredResolution))

        return self._cache["dmxRangePerResolution"][desiredResolution]

    def canCrossfadeTo(self, nextCapability: 'Capability') -> bool:
        '''Returns: Boolean - Whether this cap's end value equals the given cap's start value, i. e. one can fade from this cap to the given one.'''
        if self.type != nextCapability.type:
            return False

        if len(self.usedStartEndEntities) == 0 or len(self.usedStartEndEntities) != len(nextCapability.usedStartEndEntities):
            return False

        usesSameStartEndEntities = all(
            prop in nextCapability.usedStartEndEntities for prop in self.usedStartEndEntities)
        if not usesSameStartEndEntities:
            return False

        return all(abs(getattr(nextCapability, prop)[0].number - getattr(self, prop)[1].number) <= int(prop != "slotNumber") for prop in self.usedStartEndEntities)

    def getMenuClickDmxValueWithResolution(self, desiredResolution: int) -> 'Range':
        '''Returns: Range - The cap's DMX bounds scaled (down) to the given resolution.'''
        dmxRange = self.getDmxRangeWithResolution(desiredResolution)

        try:
            return {
                "start": dmxRange.start,
                "center": dmxRange.center,
                "end": dmxRange.end,
                "hidden": -1
            }[self.menuClick]
        except:
            raise ValueError(
                f"Unknown menuClick value '{self.menuClick}' in capability '{self.name}' ({self.rawDmxRange}).")

    def isSlotType(self, slotType: str) -> bool:
        '''Returns: Boolean - True if the cap references a slot (or range of slots) of the given type, false otherwise.'''
        slotTypeRegExp = slotType if isinstance(
            slotType, re.Pattern) else re.compile(f"^{slotType}$")

        def isCorrectSlotType(slot: 'WheelSlot') -> bool:
            return slotTypeRegExp.match(slot.type) or (slot.type in ["Open", "Closed"] and slotTypeRegExp.match(self.wheels[0].type))

        return self.slotNumber != None and all(isCorrectSlotType(slot) or (slot.type == "Split" and isCorrectSlotType(slot.floorSlot) and isCorrectSlotType(slot.ceilSlot)) for slot in self.wheelSlot)

    def _getStartEndArray(self, prop: str) -> 'Optional[list]':
        '''Returns: Array | null - Start and end value of the property (may be equal), parsed to Entity instances. null if it isn't defined in JSON.'''
        if prop in self._jsonObject.keys():
            return [Entity.createFromEntityString(str(value)) for value in [self._jsonObject[prop], self._jsonObject[prop]]]

        if f"{prop}Start" in self._jsonObject.keys():
            return [Entity.createFromEntityString(str(value)) for value in [self._jsonObject[f"{prop}Start"], self._jsonObject[f"{prop}End"]]]

        return None
