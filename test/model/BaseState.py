import unittest

from OpenLightControlGui.model import LampState
from OpenLightControlGui.fixture_model import Entity

class TestBaseState(unittest.TestCase):

    def setUp(self):
        self.str_vals = {"test1": "test", "test2": "hello"}
        self.str_vals2 = {"test3": "world"}
        self.ent_vals = {"abc": Entity(10, "m"), "def": Entity(30, "ms")}
        self.ent_vals2 = {"hello": Entity(13, "m")}
    
    def test_init(self):
        st = LampState.BaseState(self.str_vals)
        self.assertDictEqual(st.vals, self.str_vals)
    
    def test_ent_init(self):
        st = LampState.BaseState(self.ent_vals)
        self.assertDictEqual(st.vals, self.ent_vals)
    
    def test_equal(self):
        st1 = LampState.BaseState(self.ent_vals)
        st2 = LampState.BaseState(self.ent_vals)
        self.assertEqual(st1, st2)
    
    def test_copy(self):
        st = LampState.BaseState(self.str_vals)
        stc = st.copy()
        self.assertEqual(st, stc)
        self.assertIsNot(st, stc)
        for v1, v2 in zip(st.vals.values(), stc.vals.values()): # type: ignore
            self.assertEqual(v1, v2)
            if isinstance(v1, Entity):
                self.assertIsNot(v1, v2)
    
    def test_getitem(self):
        st = LampState.BaseState(self.str_vals)
        self.assertEqual(st["test1"], self.str_vals["test1"])
    
    def test_setitem(self):
        st = LampState.BaseState(self.str_vals)
        a = "test"
        st["a"] = a
        self.assertEqual(st["a"], a)
    
    def test_add(self):
        st = LampState.BaseState(self.str_vals) + LampState.BaseState(self.str_vals2)
        a = self.str_vals.copy()
        a.update(self.str_vals2)
        self.assertDictEqual(st.vals, a)
    
    def test_add_add(self):
        st1 = LampState.BaseState(self.ent_vals)
        b = {"abc": Entity(11, "m")}
        st2 = LampState.BaseState(b, additive=True)
        st = st1 + st2
        self.assertEqual(st.vals["abc"], Entity(21, "m"))
    
    def test_add_iadd(self):
        st1 = LampState.BaseState(self.ent_vals)
        b = {"abc": Entity(11, "m")}
        st2 = LampState.BaseState(b, additive=True)
        st1 += st2
        self.assertEqual(st1.vals["abc"], Entity(21, "m"))


if __name__ == "__main__":
    unittest.main()
