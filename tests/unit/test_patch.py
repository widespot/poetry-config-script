import random
import sys
import unittest
from unittest.mock import patch as mock_patch

from poetry_config_script import patch


# Fake configure_poetry() method in non existing widespot package
# To allow later mocking
klass_configure_poetry = type("configure_poetry", (object, ), {
                '_importing_path': 'widespot.configure_poetry',
                '__all__': [],
})
klass_widespot = type("widespot", (object, ), {
    'configure_poetry': klass_configure_poetry,
    '__all__': ['configure_poetry'],
})
sys.modules['widespot'] = klass_widespot
sys.modules['widespot.configure_poetry'] = klass_configure_poetry


class TestPatch(unittest.TestCase):

    def test_patch_getter_keep_content_when_no_config_script(self):
        input = {'anything': random.random()}
        self.assertEqual(input, patch.patch_getter(input))

    @mock_patch('widespot.configure_poetry')
    def test_patch_getter_with_config_script(self, mock_configure_poetry):
        r = random.random()
        input = {
            'config_script': 'widespot:configure_poetry',
            'anything': r,
        }
        output = {'blabetiblou', 'test'}

        mock_configure_poetry.return_value = output

        # make sure patch_getter returns the output of widespot:configure_poetry()
        self.assertEqual(output, patch.patch_getter(input))
        # make sure widespot:configure_poetry() was called once
        self.assertEqual(1, mock_configure_poetry.call_count)
        # Make sure widespot:configure_poetry() was called with the init input
        # but not the config_script attribute
        self.assertEqual(({'anything': r},), mock_configure_poetry.call_args_list[0].args)


if __name__ == '__main__':
    unittest.main()

