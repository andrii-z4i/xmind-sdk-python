import unittest
from unittest.mock import patch, Mock, MagicMock
from xmind.core.loader import WorkbookLoader
from xmind.tests import logging_configuration as lc
from xmind.tests import base


class LoaderTest(base.Base):
    """Loader test"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('loaderTest')
        return self._logger

    def _patch_get_abs_path(self, return_value=None, thrown_exception=None):
        """Patch get_abs_path function"""
        return self._init_patch_with_name('_get_abs_path', 'xmind.utils.get_abs_path', return_value, thrown_exception)

    def _patch_split_ext(self, return_value=None, thrown_exception=None):
        """Patch split_ext function"""
        return self._init_patch_with_name('_split_ext', 'xmind.utils.split_ext', return_value, thrown_exception)

    def test_init_get_abs_path_throws(self):
        """test case when get_abs_path throws exception"""

        self._patch_get_abs_path(
            'c:\\projects\\whatever\\d.aa', Exception("No file with such name"))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        self.getLogger().warning("Exception: %s", ex.exception)

    def test_init_split_ext_throws(self):
        """test case when split_ext throws exception"""
        self._patch_get_abs_path('dd')
        self._patch_split_ext(('a', '.xmind'), Exception('Can\'t access file'))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        self.getLogger().warning("Exception: %s", ex.exception)

    def test_init_throws_no_xmind_extension(self):
        """test case when exception comes because there is no xmind extension"""
        self._patch_get_abs_path('dd')
        self._patch_split_ext(('a', '.xm'))

        with self.assertRaises(Exception) as ex:
            WorkbookLoader('dd')  # create loader and waits for Exception

        self.getLogger().warning("Exception: %s", ex.exception)

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
        _input_stream_mock.namelist = MagicMock(
            return_value=['something', 'content.xml'])
        _input_stream_mock.read = MagicMock()
        _stream_mock = Mock()
        _stream_mock.__enter__ = MagicMock(return_value=_input_stream_mock)
        _stream_mock.__exit__ = MagicMock()
        _utils_extract_mock = self._init_patch_with_name(
            '_utils_extract', 'xmind.utils.extract', _stream_mock)
        _parse_dom_string_mock = self._init_patch_with_name(
            '_parse_dom_string', 'xmind.utils.parse_dom_string', 'something')
        _wb_mock = self._init_patch_with_name(
            '_wb', 'xmind.core.loader.WorkbookDocument', autospec=True)

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
