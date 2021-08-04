from OpenLightControlGui.fixture_model import *

import json
import os

basepath = os.path.dirname(__file__)
ofl = os.path.join(basepath, "../../open-fixture-library/fixtures/")

mans: 'dict[str, Manufacturer]' = {key: Manufacturer(key, val) for key, val in json.load(
    open(ofl+"manufacturers.json")).items() if not "$" in key}
fixturesByManu: 'dict[str, dict[str, Fixture]]' = {}
for key, man in mans.items():
    if not key in ["martin", "robe", "beamz"]:
        continue
    lis = os.listdir(ofl+key)
    fixturesByManu[key] = []
    for fix in lis:
        temp = Fixture(man, fix[:-5], json.load(open(ofl+key+"/"+fix)))
        if not fixturesByManu[key]:
            fixturesByManu[key] = {}
        fixturesByManu[key][fix[:-5]] = temp

krypt = fixturesByManu["martin"]["mac-250-krypton"]
k_mode = krypt.modes[1]
k_channels = k_mode.channels
k_channel = k_channels[0]

sola = fixturesByManu["robe"]["robin-ledwash-600"]
s_mode = sola.modes[1]
s_channels = s_mode.channels

hazer = fixturesByManu["beamz"]

print()
