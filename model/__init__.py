from .AbstractChannel import AbstractChannel
from .Capability import Capability
from .CoarseChannel import CoarseChannel
from .Entity import Entity
from .FineChannel import FineChannel
from .Fixture import Fixture
from .Manufacturer import Manufacturer
from .Matrix import Matrix
from .Meta import Meta
from .Mode import Mode
from .NullChannel import NullChannel
from .Physical import Physical
from .Range import Range
from .Resource import Resource
from .SwitchingChannel import SwitchingChannel
from .TemplateChannel import TemplateChannel
from .Wheel import Wheel
from .WheelSlot import WheelSlot

from .scale_dmx_value import DmxScaler


def getAllFixturesFromDirectory(man: Manufacturer, dir: str) -> 'list[Fixture]':
    import os
    import json

    fixtures = []
    lis = os.listdir(dir)
    for fix in lis:
        temp = Fixture(man, fix[:-5], json.load(open(os.path.join(dir, fix))))
        fixtures.append(temp)

    return fixtures


def getAllFixtures(ofl: str) -> 'dict[str, list[Fixture]]':
    import os
    import json

    mans: 'dict[str, Manufacturer]' = {key: Manufacturer(key, val) for key, val in json.load(
        open(os.path.join(ofl, "manufacturers.json"))).items() if not "$" in key}

    fixturesByManu = {}
    for key, man in mans.items():
        fixturesByManu[key] = getAllFixturesFromDirectory(
            man, os.path.join(ofl, key))

    return fixturesByManu


__all__ = ["AbstractChannel", "Capability", "CoarseChannel", "Entity", "FineChannel", "Fixture", "Manufacturer", "Matrix",
           "Meta", "Mode", "NullChannel", "Physical", "Range", "Resource", "SwitchingChannel", "TemplateChannel", "Wheel", "WheelSlot", "DmxScaler"]
