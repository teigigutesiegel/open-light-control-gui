import unittest

from Lamp import TestLamp
from OpenLightControlGui.model import Address, Lamp, Group
from OpenLightControlGui.fixture_model import Mode, Fixture

class TestGroup(unittest.TestCase):
    desk_channel: Mode
    pan_tilt: Mode
    rgb: Mode

    def setUp(self):
        TestLamp.setUp(self)
        self.lamp1 = Lamp(1, self.desk_channel, Address(1, 10))
        self.lamp2 = Lamp(2, self.pan_tilt, Address(1, 2))
        self.lamp3 = Lamp(3, self.rgb, [Address(1, 4), Address(2, 4)])

    def test_empty_group(self):
        grp = Group()
        self.assertListEqual(grp.lamps, [])
        self.assertEqual(grp.name, "")
    
    def test_name_init(self):
        name = "Test"
        grp = Group(name=name)
        self.assertEqual(grp.name, name)
    
    def test_name_change(self):
        grp = Group(name="Tesasd")
        new_name = "hello"
        grp.name = new_name
        self.assertEqual(grp.name, new_name)

    def test_single_lamp(self):
        grp = Group(self.lamp1)
        self.assertListEqual(grp.lamps, [self.lamp1])
    
    def test_mutli_lamp(self):
        l = [self.lamp1, self.lamp2]
        grp = Group(l)
        self.assertListEqual(grp.lamps, l)
    
    def test_add_lamp(self):
        grp = Group(self.lamp1)
        grp.addItem(self.lamp2)
        self.assertListEqual(grp.lamps, [self.lamp1, self.lamp2])
    
    def test_remove_lamp(self):
        grp = Group([self.lamp1, self.lamp2])
        grp.removeItem(self.lamp2)
        self.assertListEqual(grp.lamps, [self.lamp1])
    
    def test_add_group(self):
        grp = Group(self.lamp1)
        grp.addItem(Group([self.lamp2]))
        self.assertListEqual(grp.lamps, [self.lamp1, self.lamp2])
    
    def test_remove_group(self):
        grp1 = Group(self.lamp1)
        grp2 = Group([self.lamp1, grp1])
        grp2.removeItem(grp1)
        self.assertListEqual(grp2.lamps, [self.lamp1])
    
    def test_equal(self):
        grp1 = Group(self.lamp1)
        grp2 = Group(self.lamp1)
        self.assertEqual(grp1, grp2)
        grp1.addItem(self.lamp2)
        self.assertNotEqual(grp1, grp2)
        grp2.addItem(self.lamp2)
        self.assertEqual(grp1, grp2)
    
    def test_add(self):
        grp = Group(self.lamp1) + Group(self.lamp2)
        self.assertListEqual(grp.lamps, [self.lamp1, self.lamp2])
    
    def test_iadd(self):
        grp = Group(self.lamp1)
        grp += [self.lamp2, Group(self.lamp3)]
        self.assertListEqual(grp.lamps, [self.lamp1, self.lamp2, self.lamp3])
    
    def test_sub(self):
        grp = Group([self.lamp1, self.lamp2]) - self.lamp1
        self.assertListEqual(grp.lamps, [self.lamp2])
    
    def test_isub(self):
        grp = Group([self.lamp1, self.lamp2])
        grp -= self.lamp2
        self.assertListEqual(grp.lamps, [self.lamp1])
    
    def test_str(self):
        grp = Group([self.lamp1, self.lamp2])
        self.assertEqual(str(grp), "Group <1-Desk Channel, 2-Pan/Tilt Fader> [2]")
    
    def test_str_over_2(self):
        grp = Group([self.lamp1, self.lamp1, self.lamp2, self.lamp3])
        self.assertEqual(str(grp), "Group <1-Desk Channel, 1-Desk Channel, ...> [4]")
    
    def test_repr(self):
        grp = Group([self.lamp1, self.lamp2])
        self.assertEqual(repr(grp), "Group([Lamp(1, <...Desk Channel[8 bit]...>, [Address(universe=1, address=10)]) ,Lamp(2, <...Pan/Tilt Fader[8 bit]...>, [Address(universe=1, address=2)])])")

if __name__ == "__main__":
    unittest.main()
