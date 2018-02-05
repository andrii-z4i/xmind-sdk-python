import unittest
from abc import abstractmethod
from unittest.mock import patch, Mock, MagicMock


class PatcherWrapper(object):
    def __init__(self, patch, name):
        self.patch = patch
        self.name = name
        self.deleted = False


class Base(unittest.TestCase):
    """Base class for any tests"""

    @abstractmethod
    def getLogger(self):
        raise NotImplementedError()

    def setUp(self):
        self.getLogger().info('Start test: %s', self._testMethodName)
        self._patchers = []

    def tearDown(self):
        _patcher_names = map(lambda x: x.name, self._patchers)
        for name in _patcher_names:
            self._remove_patched_function(name)
        self.getLogger().info('End test: %s', self._testMethodName)

    def _remove_patched_function(self, property_name):
        """Remove patched function by name"""
        _exisiting_patches = [i for i in filter(
            lambda x: x.name == property_name, self._patchers)]
        _exisiting_running_patches = [i for i in filter(
            lambda x: not x.deleted, _exisiting_patches)]
        if len(_exisiting_running_patches) > 1:
            raise Exception(
                "More than one patch with a name '%s'" % property_name)

        if not len(_exisiting_running_patches):
            self.getLogger().debug(
                'No running mock for with a name "%s". Nothing to stop', property_name)
            return

        _patch_wrapper = _exisiting_running_patches[0]
        _patch_wrapper.patch.stop()
        self.getLogger().debug("Property '%s' has been deleted", property_name)
        _patch_wrapper.deleted = True

    def _init_patch_with_name(self, property_name, function_name, return_value=None, thrown_exception=None, autospec=None, return_value_as_side_effect=False):
        """Patches the function"""
        def side_effect_function(*a, **kw):
            """Side effect function"""
            if thrown_exception:
                self.getLogger().error("%s => Throw exception: '%s'",
                                       function_name, thrown_exception)
                raise thrown_exception
            self.getLogger().debug(
                "%s => called with (%s), returns (%s)", function_name, a, return_value)
            return return_value

        _side_effect = return_value if isinstance(
            return_value, list) and return_value_as_side_effect else side_effect_function

        _exisiting_patches = [i for i in filter(
            lambda x: x.name == property_name, self._patchers)]
        _exisiting_running_patches = [i for i in filter(
            lambda x: not x.deleted, _exisiting_patches)]

        if len(_exisiting_running_patches):
            raise Exception(
                "Can\'t init patch '%s' for '%s', it already exists with the same name" %
                (property_name, function_name))

        _patch = patch(
            function_name,
            autospec=autospec
        )

        self._patchers.append(PatcherWrapper(_patch, property_name))

        _mock = _patch.start()
        _mock.side_effect = _side_effect

        self.getLogger().debug(
            "Property '%s' for function '%s' has been set", property_name, function_name)
        return _mock

    def _test_method_by_excessive_parameters(self, pair, _element):
        _method_name_to_test = pair[0]
        _parameters_count = pair[1]
        _check_for_none = True

        if isinstance(_parameters_count, tuple):
            _p = _parameters_count
            _parameters_count = _p[0]
            _check_for_none = _p[1]

        _method_to_call = getattr(_element, _method_name_to_test)
        _call_method_with_parameters = [
            i for i in range(_parameters_count + 1)]
        self.getLogger().debug("Test method '%s' with %d parameters",
                               _method_name_to_test, _parameters_count)
        with self.assertRaises(TypeError) as _ex:
            _method_to_call(*_call_method_with_parameters)

        self.getLogger().debug("Got an exception: '%s'", _ex.exception.args[0])
        self.assertTrue(_ex.exception.args[0].find(
            "%s() takes" % _method_name_to_test) != -1)

        if _parameters_count > 0 and _check_for_none:  # Let's test with None as well
            self.getLogger().debug(
                "Test method '%s' with 0 parameters", _method_name_to_test)
            with self.assertRaises(TypeError) as _exNone:
                _method_to_call()

            self.getLogger().debug("Got an exception: '%s'",
                                   _exNone.exception.args[0])
            self.assertTrue(_exNone.exception.args[0].find(
                "%s() missing" % _method_name_to_test) != -1)
