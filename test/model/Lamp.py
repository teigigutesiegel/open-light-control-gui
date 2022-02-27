import unittest
import os

from OpenLightControlGui.utils.ofl import get_fixtures
from OpenLightControlGui.model import Address, Lamp

class TestLamp(unittest.TestCase):
    
    def setUp(self):
        basepath = os.path.dirname(__file__)
        ofl = os.path.join(basepath, "../../../open-fixture-library/fixtures/")
        fixturesByManu = get_fixtures(ofl)
        self.desk_channel = fixturesByManu["generic"]["desk-channel"].modes[0]
        self.pan_tilt = fixturesByManu["generic"]["pan-tilt"].modes[0]
        self.rgb = fixturesByManu["generic"]["rgb-fader"].modes[0]
    
    def test_number(self):
        num = 10
        lamp = Lamp(10, self.desk_channel)
        self.assertEqual(lamp.number, num)
    
    def test_set_number(self):
        new_num = 11
        lamp = Lamp(10, self.rgb)
        lamp.number = new_num
        self.assertEqual(lamp.number, new_num)
    
    def test_mode(self):
        mode = self.rgb
        lamp = Lamp(10, mode)
        self.assertEqual(lamp.mode, mode)
    
    def test_fixture(self):
        mode = self.rgb
        fixture = mode.fixture
        lamp = Lamp(10, mode)
        self.assertEqual(lamp.fixture, fixture)
    
    def test_channels(self):
        mode = self.rgb
        channels = mode.channels
        lamp = Lamp(10, mode)
        self.assertEqual(lamp.channels, channels)
    
    def test_dmxRange(self):
        mode = self.rgb
        dmxrange = len(mode.channels)
        lamp = Lamp(10, mode)
        self.assertEqual(lamp.dmxRange, dmxrange)
    
    def test_len(self):
        mode = self.rgb
        dmxrange = len(mode.channels)
        lamp = Lamp(10, mode)
        self.assertEqual(len(lamp), dmxrange)
    
    def test_single_address(self):
        addr = Address(10, 20)
        lamp = Lamp(10, self.rgb, addr)
        self.assertListEqual(lamp.address, [addr])
    
    def test_multiple_addresses(self):
        addrs = [Address(10, 20), Address(11, 32)]
        lamp = Lamp(10, self.rgb, addrs)
        self.assertListEqual(lamp.address, addrs)
    
    def test_set_single_address(self):
        addr_new = Address(10, 23)
        lamp = Lamp(10, self.rgb, Address(23, 123))
        lamp.address = addr_new
        self.assertListEqual(lamp.address, [addr_new])
    
    def test_set_multiple_addresses(self):
        addr_new = [Address(10, 20), Address(11, 32)]
        lamp = Lamp(10, self.rgb, [Address(123, 20), Address(1, 32)])
        lamp.address = addr_new
        self.assertListEqual(lamp.address, addr_new)
    
    def test_add_single_address(self):
        addr1 = Address(10, 20)
        addr2 = Address(11, 20)
        lamp = Lamp(10, self.rgb, addr1)
        lamp.add_address(addr2)
        self.assertListEqual(lamp.address, [addr1, addr2])
    
    def test_add_multiple_addresses(self):
        addr1 = Address(10, 20)
        addr_new = [Address(23, 23), Address(12, 20)]
        lamp = Lamp(10, self.rgb, addr1)
        lamp.add_address(addr_new)
        self.assertListEqual(lamp.address, [addr1]+addr_new)
    
    def test_hasAddress(self):
        lamp = Lamp(10, self.rgb)
        self.assertFalse(lamp.hasAddress)
        lamp.add_address(Address(10, 20))
        self.assertTrue(lamp.hasAddress)
    
    def test_capabilities_desk_channel(self):
        cap = {
            "Intensity": 0,
            "Position": None,
            "Color": None,
            "Beam": None,
            "Maintenance": None
        }
        lamp = Lamp(10, self.desk_channel)
        self.assertDictEqual(lamp.capabilities, cap)
    
    def test_capabilities_rgb(self):
        cap = {
            "Intensity": None,
            "Position": None,
            "Color": {'Blue': 2, 'Green': 1, 'Red': 0},
            "Beam": None,
            "Maintenance": None
        }
        lamp = Lamp(10, self.rgb)
        self.assertDictEqual(lamp.capabilities, cap)
    
    def test_capabilities_pan_tilt(self):
        cap = {
            "Intensity": None,
            "Position": None,
            "Color": None,
            "Beam": None,
            "Maintenance": None
        }
        lamp = Lamp(10, self.pan_tilt)
        self.assertDictEqual(lamp.capabilities, cap)
    
    def test_equal(self):
        mode = self.rgb
        addr = Address(10, 20)
        lamp1 = Lamp(1, mode, addr)
        lamp2 = Lamp(2, mode, addr)
        self.assertEqual(lamp1, lamp2)
    
    def test_str(self):
        lamp = Lamp(1, self.rgb)
        self.assertEqual(str(lamp), "1-RGB Fader")
    
    def test_repr(self):
        lamp = Lamp(1, self.rgb, Address(1, 20))
        self.assertEqual(repr(lamp), "Lamp(1, <...RGB Fader[8 bit]...>, [Address(universe=1, address=20)])")

if __name__ == "__main__":
    unittest.main()
