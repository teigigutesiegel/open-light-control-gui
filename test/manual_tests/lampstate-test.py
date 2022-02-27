from OpenLightControlGui.fixture_model import *
from OpenLightControlGui.model import LampState, State, Scene, Address, Lamp, Group


def get_manu() -> 'dict[str, dict[str, Fixture]]':
    import json
    import os

    basepath = os.path.dirname(__file__)
    ofl = os.path.join(basepath, "../../open-fixture-library/fixtures/")

    mans: 'dict[str, Manufacturer]' = {key: Manufacturer(key, val) for key, val in json.load(
        open(ofl+"manufacturers.json")).items() if not "$" in key}
    fixturesByManu: 'dict[str, dict[str, Fixture]]' = {}
    for key, man in mans.items():
        if not key in ["martin", "robe", "beamz", "generic"]:
            continue
        lis = os.listdir(ofl+key)
        fixturesByManu[key] = []
        for fix in lis:
            temp = Fixture(man, fix[:-5], json.load(open(ofl+key+"/"+fix)))
            if not fixturesByManu[key]:
                fixturesByManu[key] = {}
            fixturesByManu[key][fix[:-5]] = temp
    return fixturesByManu

fixturesByManu = get_manu()

# krypt = fixturesByManu["martin"]["mac-250-krypton"]
# k_mode = krypt.modes[1]
# k_channels = k_mode.channels
# k_channel = k_channels[0]
# k_address = Address(0, 0)
# k_lamp = Lamp(1, k_mode, k_address)
# k_cap = k_lamp.capabilities
# k_group = Group(k_lamp)

# sola = fixturesByManu["robe"]["robin-ledwash-600"]
# s_mode = sola.modes[1]
# s_channels = s_mode.channels
# s_address = Address(0, 50)
# s_lamp = Lamp(20, s_mode, s_address)
# s_cap = s_lamp.capabilities
# s_group = Group(s_lamp)

# sola_state = LampState()
# sola_int = LampState.IntensityState()
# sola_int.Intensity = Entity.createFromEntityString("bright")
# sola_col = LampState.ColorState()
# sola_col.Red = Entity(100, "%")
# sola_col.Green = Entity(50, "%")
# sola_col.Blue = Entity(0, "%")
# sola_state.Intensity = sola_int
# sola_state.Color = sola_col

# s_state = State(s_group, sola_state)
# s_scene = Scene(s_state)

# hazer = fixturesByManu["beamz"]['h2000-faze-machine']
# h_mode = hazer.modes[0]
# h_channels = h_mode.channels
# h_address = Address(0, 100)
# h_lamp = Lamp(10, h_mode, h_address)
# h_cap = h_lamp.capabilities
# h_group = Group(h_lamp)

# haze_state = LampState()
# smoke = LampState.IntensityState()
# fan = LampState.IntensityState()
# smoke.Smoke = Entity(100, "%")
# fan.Fan = Entity(20, "%")
# haze_state.Intensity = smoke + fan

# h_state = State(h_group, haze_state)
# h_scene = Scene(h_state)

d = Lamp(1, fixturesByManu["generic"]["desk-channel"].modes[0], Address(0, 1))
r = Lamp(2, fixturesByManu["generic"]["drgb-fader"].modes[0], Address(0, 10))

sola_state = LampState()
sola_int = LampState.IntensityState()
sola_int.Intensity = Entity.createFromEntityString("bright")
sola_col = LampState.ColorState()
sola_col.Red = Entity(100, "%")
sola_col.Green = Entity(50, "%")
sola_col.Blue = Entity(0, "%")
sola_state.Intensity = sola_int
sola_state.Color = sola_col

s_state = State(Group([d, r]), sola_state)
s_scene = Scene(s_state)


print(s_scene.getDmxState())
