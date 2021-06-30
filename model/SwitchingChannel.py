from .AbstractChannel import AbstractChannel
from .Range import Range

from typing import Literal, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .Fixture import Fixture

SwitchingChannelBehavior = Literal['keyOnly',
                                   'defaultOnly', 'switchedOnly', 'all']


def _findIndex(flist, func):
    for i, v in enumerate(flist):
        if func(v):
            return i
    return -1


class TriggerCapability():
    dmxRange: 'Range'
    switchTo: str

    def __init__(self, dmxRange: 'Range', switchTo: str) -> None:
        self.dmxRange = dmxRange
        self.switchTo = switchTo


class SwitchingChannel(AbstractChannel):
    '''Represents a channel that switches its behavior depending on trigger channel's value.'''

    _triggerChannel: AbstractChannel
    _cache: 'dict[str, Any]'

    def __init__(self, alias: str, triggerChannel: AbstractChannel) -> None:
        super().__init__(alias)
        self._triggerChannel = triggerChannel
        self._cache = {}

    def _get_triggerChannel(self) -> AbstractChannel:
        return self._triggerChannel

    def _get_fixture(self) -> 'Fixture':
        return self._triggerChannel.fixture

    def _get_triggerCapabilities(self) -> 'list[TriggerCapability]':
        if not "triggerCapabilities" in self._cache.keys():
            self._cache["triggerCapabilities"] = []
            for cap in self.triggerChannel.capabilities:
                self._cache["triggerCapabilities"].append(TriggerCapability(cap.dmxRange, cap.switchChannels[self.key]))

        return self._cache["triggerCapabilities"]

    def _get_triggerRanges(self) -> 'dict[str, list[Range]]':
        if not "triggerRanges" in self._cache.keys():
            ranges = {}

            for capability in self.triggerCapabilities:
                if not capability.switchTo in ranges.keys():
                    ranges[capability.switchTo] = []
                ranges[capability.switchTo].append(capability.dmxRange)

            for channel in ranges.keys():
                ranges[channel] = Range.getMergedRanges(ranges[channel])

            self._cache["triggerRanges"] = ranges

        return self._cache["triggerRanges"]

    def _get_defaultChannelKey(self) -> str:
        if not "defaultChannelKey" in self._cache.keys():
            for cap in self.triggerCapabilities:
                if cap.dmxRange.contains(self.triggerChannel.defaultValue):
                    self._cache["defaultChannelKey"] = cap.switchTo
                    break
            # self._cache["defaultChannelKey"] = self.triggerCapabilities[_findIndex(
            #     self.triggerCapabilities, lambda cap: cap.dmxRange.contains(self.triggerChannel.defaultValue))].switchTo

        return self._cache["defaultChannelKey"]

    def _get_defaultChannel(self) -> AbstractChannel:
        if not "defaultChannel" in self._cache.keys():
            self._cache["defaultChannel"] = self.fixture.getChannelByKey(
                self.defaultChannelKey)

        return self._cache["defaultChannel"]

    def _get_switchToChannelKeys(self) -> 'list[str]':
        if not "switchToChannelKeys" in self._cache.keys():
            self._cache["switchToChannelKeys"] = list(dict.fromkeys(
                [cap.switchTo for cap in self.triggerCapabilities]))

        return self._cache["switchToChannelKeys"]

    def _get_switchToChannels(self) -> 'list[AbstractChannel]':
        if not "switchToChannels" in self._cache.keys():
            self._cache["switchToChannels"] = [self.fixture.getChannelByKey(
                chkey) for chkey in self.switchToChannelKeys]

        return self._cache["switchToChannels"]

    def usesChannelKey(self, channelKey: str, switchingChannelBehavior: SwitchingChannelBehavior = "all") -> bool:
        if switchingChannelBehavior == "keyOnly":
            return self.key == channelKey
        if switchingChannelBehavior == "defaultOnly":
            return self.defaultChannel.key == channelKey
        if switchingChannelBehavior == "switchedOnly":
            return channelKey in self.switchToChannelKeys

        return channelKey in self.switchToChannelKeys or self.key == channelKey

    def _get_isHelpWanted(self) -> bool:
        if not "isHelpWanted" in self._cache.keys():
            self._cache["isHelpWanted"] = any(
                getattr(ch, "isHelpWanted", False) for ch in self.switchToChannels)

        return self._cache["isHelpWanted"]

    fixture: 'Fixture' = property(_get_fixture)
    triggerChannel: AbstractChannel = property(_get_triggerChannel)
    triggerCapabilities: 'list[TriggerCapability]' = property(
        _get_triggerCapabilities)
    triggerRanges: 'dict[str, list[Range]]' = property(_get_triggerRanges)
    defaultChannelKey: str = property(_get_defaultChannelKey)
    defaultChannel: AbstractChannel = property(_get_defaultChannel)
    switchToChannelKeys: 'list[str]' = property(_get_switchToChannelKeys)
    switchToChannels: 'list[AbstractChannel]' = property(_get_switchToChannels)
    isHelpWanted: bool = property(_get_isHelpWanted)
