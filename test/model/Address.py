import unittest

from OpenLightControlGui.model import Address

class TestAddress(unittest.TestCase):

    def test_address(self):
        test = 10
        addr = Address(0, test)
        self.assertEqual(addr.address, test)
    
    def test_universe(self):
        test = 10
        addr = Address(test, 1)
        self.assertEqual(addr.universe, test)
    
    def test_eqal(self):
        addr1 = Address(10, 20)
        addr2 = Address(10, 20)
        self.assertEqual(addr1, addr2)
    
    def test_gt_universe1(self):
        addr1 = Address(1, 30)
        addr2 = Address(2, 40)
        self.assertGreater(addr2, addr1)
    
    def test_gt_universe2(self):
        addr1 = Address(1, 30)
        addr2 = Address(4, 1)
        self.assertGreater(addr2, addr1)
    
    def test_gt_address(self):
        addr1 = Address(1, 20)
        addr2 = Address(1, 40)
        self.assertGreater(addr2, addr1)
    
    def test_lt_universe1(self):
        addr1 = Address(1, 30)
        addr2 = Address(2, 40)
        self.assertLess(addr1, addr2)
    
    def test_lt_universe2(self):
        addr1 = Address(1, 30)
        addr2 = Address(4, 1)
        self.assertLess(addr1, addr2)
    
    def test_lt_address(self):
        addr1 = Address(1, 20)
        addr2 = Address(1, 40)
        self.assertLess(addr1, addr2)
    
    def test_str(self):
        addr = Address(1, 10)
        self.assertEqual(str(addr), "1:10")

if __name__ == '__main__':
    unittest.main()
