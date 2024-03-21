import unittest
from unittest.mock import MagicMock

from poetry_config_script import utils


def make_demo():
    class Demo:

        def __init__(self, prop_value):
            self._prop = prop_value

        @property
        def prop(self):
            return self._prop

    return Demo


class TestUtils(unittest.TestCase):

    def test_make_demo(self):
        Demo = make_demo()

        demo = Demo(4)
        self.assertEqual(4, demo.prop)

    def test_patch_class_property(self):
        Demo = make_demo()

        mock = MagicMock(return_value=3)

        utils.patch_class_property(Demo, "prop", mock)
        self.assertEqual(3, Demo(12).prop)
        self.assertEqual(mock.call_count, 1)
        self.assertEqual(mock.call_args_list[0].args, (12,))


if __name__ == '__main__':
    unittest.main()
