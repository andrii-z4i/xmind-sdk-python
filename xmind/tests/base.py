import unittest
from unittest.mock import patch, Mock, MagicMock


class Base(unittest.TestCase):
    """Base class for any tests"""

    def setUp(self):
        _logger = getattr(self, 'LOGGER', None)
        if not _logger:
            raise Exception('Logger has to be set in your inherited class')
        self.LOGGER.info('Start test: %s', self._testMethodName)
        self._patchers = []

    def tearDown(self):
        for patcher in self._patchers:
            self._remove_patched_function(patcher)
        self.LOGGER.info('End test: %s', self._testMethodName)

    def _remove_patched_function(self, property_name):
        """Remove patched function by name"""
        _patcher = getattr(self, property_name, None)
        if _patcher:
            _patcher.stop()
            delattr(self, property_name)
            self.LOGGER.debug("Property '%s' has been deleted", property_name)

    def _init_patch_with_name(self, property_name, function_name, return_value=None, thrown_exception=None, autospec=None):
        """Patches the function"""
        def side_effect_function(*a, **kw):
            """Side effect function"""
            if thrown_exception:
                self.LOGGER.error("%s => Throw exception: '%s'",
                                  function_name, thrown_exception)
                raise thrown_exception
            self.LOGGER.debug(
                "%s => called with (%s), returns (%s)", function_name, a, return_value)
            return return_value

        _side_effect = side_effect_function

        if getattr(self, property_name, None):
            raise Exception('Can\'t set property, already exists')

        _patch = patch(
            function_name,
            autospec=autospec
        )

        setattr(self, property_name, _patch)

        _mock = _patch.start()
        _mock.side_effect = _side_effect

        self._patchers.append(property_name)
        self.LOGGER.debug(
            "Property '%s' for function '%s' has been set", property_name, function_name)
        return _mock

    def _test_method_by_excessive_parameters(self, pair, _element):
        _method_name_to_test = pair[0]
        _parameters_count = pair[1]

        _method_to_call = getattr(_element, _method_name_to_test)
        _call_method_with_parameters = [
            i for i in range(_parameters_count + 1)]
        self.LOGGER.debug("Test method '%s' with %d parameters",
                            _method_name_to_test, _parameters_count)
        with self.assertRaises(Exception):
            _method_to_call(*_call_method_with_parameters)

        if _parameters_count > 0:  # Let's test with None as well
            self.LOGGER.debug(
                "Test method '%s' with 0 parameters", _method_name_to_test)
            with self.assertRaises(Exception):
                _method_to_call()
