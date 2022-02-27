from OpenLightControlGui.fixture_model import *

import json
import os

basepath = os.path.dirname(__file__)
ofl = os.path.join(basepath, "../../open-fixture-library/fixtures/")


def check_prop(obj, checkagain=True):
    v = vars(type(obj))
    keys = [key for key in v.keys() if not "_" in key]
    for key in keys:
        # try:
        temp = getattr(obj, key)
        if checkagain:
            if isinstance(temp, list):
                for i in temp:
                    check_prop(i, False)
            elif type(temp) in [AbstractChannel, Capability, CoarseChannel, Entity, FineChannel, Manufacturer, Matrix, Meta, Mode, NullChannel, Physical, Range, Resource, SwitchingChannel, TemplateChannel, Wheel, WheelSlot, DmxScaler]:
                check_prop(temp, False)
        # except:
        #     print("##### failed", obj, key)


mans: 'dict[str, Manufacturer]' = {key: Manufacturer(key, val) for key, val in json.load(open(ofl+"manufacturers.json")).items() if not "$" in key}
fixturesByManu = {}
fixtures: 'list[Fixture]' = []
for key, man in mans.items():
    lis = os.listdir(ofl+key)
    fixturesByManu[key] = []
    for fix in lis:
        temp = Fixture(man, fix[:-5], json.load(open(ofl+key+"/"+fix)))
        fixturesByManu[key].append(temp)
        fixtures.append(temp)

for fixture in fixtures:
    print(f"{fixture.manufacturer.key}/{fixture.key}")
    # check_prop(fixture)
