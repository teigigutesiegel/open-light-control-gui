from OpenLightControlGui.model.Address import Address
from OpenLightControlGui.model.Lamp import Lamp
from OpenLightControlGui.model.Group import Group
from OpenLightControlGui.model.State import State
from OpenLightControlGui.model.LampState import LampState

from OpenLightControlGui.fixture_model.Fixture import Fixture
from OpenLightControlGui.fixture_model.Manufacturer import Manufacturer

f = Fixture(Manufacturer("test", {}), "Testing", {"name": "Testing"})
l = LampState()

l0 = Lamp(0, f, Address(1, 0))
l1 = Lamp(1, f, Address(1, 1))
l2 = Lamp(2, f, Address(1, 2))
l3 = Lamp(3, f, Address(1, 3))

g0 = Group([l0, l1, l2])
g1 = Group(g0)
g1 += Lamp(4, f, Address(1, 4))

g0 += l3

print(g1)
