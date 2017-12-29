import unittest
from unittest.mock import patch, Mock, MagicMock
from xmind.core.loader import WorkbookLoader
import logging

LOGGER = logging.getLogger('loaderTest')


class LoaderTest(unittest.TestCase):
    """Loader test"""

    def setUp(self):
        LOGGER.info('Start test: %s', self._testMethodName)
        self._patchers = []

    def tearDown(self):
        for patcher in self._patchers:
            self._remove_patched_function(patcher)
        LOGGER.info('End test: %s', self._testMethodName)

    def _remove_patched_function(self, property_name):
        """Remove patched function by name"""
        _patcher = getattr(self, property_name, None)
        if _patcher:
            _patcher.stop()
            delattr(self, property_name)
            LOGGER.debug("Property '%s' has been deleted", property_name)

    def _patch_get_abs_path(self, return_value=None, thrown_exception=None):
        """Patch get_abs_path function"""
        return self._init_patch_with_name('_get_abs_path', 'xmind.utils.get_abs_path', return_value, thrown_exception)

    def _patch_split_ext(self, return_value=None, thrown_exception=None):
        """Patch split_ext function"""
        return self._init_patch_with_name('_split_ext', 'xmind.utils.split_ext', return_value, thrown_exception)

    def _init_patch_with_name(self, property_name, function_name, return_value=None, thrown_exception=None, autospec=None):
        """Patches the function"""
        def side_effect_function(*a, **kw):
            """Side effect function"""
            if thrown_exception:
                LOGGER.error("%s => Throw exception: '%s'", function_name, thrown_exception)
                raise thrown_exception
            LOGGER.debug("%s => called with (%s), returns (%s)", function_name, a, return_value)
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
        LOGGER.debug("Property '%s' for function '%s' has been set", property_name, function_name)
        return _mock


    def test_init_get_abs_path_throws(self):
        """test case when get_abs_path throws exception"""

        self._patch_get_abs_path('c:\\projects\\whatever\\d.aa', Exception("No file with such name"))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        LOGGER.warning("Exception: %s", ex.exception)

    def test_init_split_ext_throws(self):
        """test case when split_ext throws exception"""
        self._patch_get_abs_path('dd')
        self._patch_split_ext(('a', '.xmind'), Exception('Can\'t access file'))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        LOGGER.warning("Exception: %s", ex.exception)

    def test_init_throws_no_xmind_extension(self):
        """test case when exception comes because there is no xmind extension"""
        self._patch_get_abs_path('dd')
        self._patch_split_ext(('a', '.xm'))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        LOGGER.warning("Exception: %s", ex.exception)

    def test_init_no_exception(self):
        """test case when no exception comes even though there are no data"""
        self._patch_get_abs_path('dd')
        self._patch_split_ext(('a', '.xmind'))

        WorkbookLoader('dd')  # create loader and waits for Exception

    def test_get_workbook(self):
        """Tests if get workbook function will be able to return fake workbook document"""

        _get_abs_path_mock = self._patch_get_abs_path('dd')
        _split_ext_mock = self._patch_split_ext(('a', '.xmind'))
        _input_stream_mock = Mock()
        _input_stream_mock.namelist = MagicMock(return_value=['something', 'content.xml'])
        _input_stream_mock.read = MagicMock()
        _stream_mock = Mock()
        _stream_mock.__enter__ = MagicMock(return_value=_input_stream_mock)
        _stream_mock.__exit__ = MagicMock()
        _utils_extract_mock = self._init_patch_with_name('_utils_extract', 'xmind.utils.extract', _stream_mock)
        _parse_dom_string_mock = self._init_patch_with_name('_parse_dom_string', 'xmind.utils.parse_dom_string', 'something')
        _wb_mock = self._init_patch_with_name('_wb', 'xmind.core.loader.WorkbookDocument', autospec=True)

        wb = WorkbookLoader('dd')
        wb.get_workbook()

        _get_abs_path_mock.assert_called_once()
        _split_ext_mock.assert_called_once_with('dd')
        _stream_mock.__enter__.assert_called_once()
        _stream_mock.__exit__.assert_called_once()
        _input_stream_mock.namelist.assert_called_once()
        _input_stream_mock.read.assert_called_once()
        _utils_extract_mock.assert_called_once()
        _parse_dom_string_mock.assert_called_once()
        _wb_mock.assert_called()
