from xmind.tests import logging_configuration as lc
from xmind.tests import base
from unittest.mock import patch, MagicMock, mock_open
from xmind.core.saver import WorkbookSaver
from xmind.core.const import CONTENT_XML, XMIND_EXT


class WorkbookSaverTest(base.Base):

    def setUp(self):
        super(WorkbookSaverTest, self).setUp()
        self._workbook = MagicMock()
        self._test_el = WorkbookSaver(self._workbook)

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('WoorkbookSaverTest')
        return self._logger

    def test_excessive_parameters(self):
        _parameters = [
            ('_get_content', 0),
            ('save', (1, False)),
            ('__init__', 1)
        ]
        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, self._test_el)

    def test_WoorkbookSaver_init(self):
        # Call with one parameter
        _test_object = WorkbookSaver('workbook')
        self.assertEqual(_test_object._workbook, 'workbook')

    def test_get_content(self):
        _utils_join_path = patch('xmind.utils.join_path').start()
        _utils_join_path.return_value = 'joined path'
        _utils_temp_dir = patch('xmind.utils.temp_dir').start()
        _utils_temp_dir.return_value = 'temp dir'
        _output = patch.object(self._workbook, 'output').start()
        _m = mock_open()  # to test with statement

        with patch('codecs.open', _m, create=True):
            _el = self._test_el._get_content()

        _utils_temp_dir.assert_called_once_with()
        _utils_join_path.assert_called_once_with('temp dir', CONTENT_XML)
        _m.assert_called_once_with('joined path', 'w', encoding="utf-8")
        _output.assert_called_once_with(_m())
        self.assertEqual(_el, 'joined path')

    def test_save_with_no_path_no_get_path(self):
        _get_path = patch.object(self._workbook, 'get_path').start()
        _get_path.return_value = None

        _test_el = WorkbookSaver(self._workbook)
        with self.assertRaises(Exception) as _ex:
            _test_el.save()

        self.assertTrue(_ex.exception.args[0].find(
            "Please specify a filename for the XMind file") != -1)
        _get_path.assert_called_once_with()

    def test_save_is_path(self):
        _get_abs_path = patch('xmind.utils.get_abs_path').start()
        _get_abs_path.side_effect = Exception('stop point')

        with self.assertRaises(Exception) as _ex:
            self._test_el.save('path')

        self.assertTrue(_ex.exception.args[0].find("stop point") == 0)
        _get_abs_path.assert_called_once_with('path')

    def test_save_no_path_is_get_path(self):
        _get_abs_path = patch('xmind.utils.get_abs_path').start()
        _get_abs_path.side_effect = Exception('stop point')
        self._workbook.get_path.return_value = 'get path'

        with self.assertRaises(Exception) as _ex:
            self._test_el.save()

        self.assertTrue(_ex.exception.args[0].find("stop point") == 0)
        _get_abs_path.assert_called_once_with('get path')
        self._workbook.get_path.assert_called_once_with()

    def test_save_if_ext_is_not_equal_xmind_ext(self):
        _get_abs_path = patch('xmind.utils.get_abs_path').start()
        _get_abs_path.return_value = 'abs path'
        _split_ext = patch('xmind.utils.split_ext').start()
        _split_ext.return_value = 'name', 'ext'

        with self.assertRaises(Exception) as _ex:
            self._test_el.save('path')

        self.assertTrue(_ex.exception.args[0].find(
            "XMind filenames require a '%s' extension" % XMIND_EXT) != -1)
        _get_abs_path.assert_called_once_with('path')
        _split_ext.assert_called_once_with('abs path')

    def test_save_if_ext_is_equal_xmind_ext(self):
        _get_abs_path = patch('xmind.utils.get_abs_path').start()
        _get_abs_path.return_value = 'abs path'
        _split_ext = patch('xmind.utils.split_ext').start()
        _split_ext.return_value = 'name', XMIND_EXT
        _get_content = patch.object(self._test_el, '_get_content').start()
        _get_content.return_value = 'content'
        _f = MagicMock()
        _compress = patch('xmind.utils.compress').start()
        _compress.return_value = _f
        _write = patch.object(_f, 'write').start()

        self._test_el.save('path')

        _get_abs_path.assert_called_once_with('path')
        _split_ext.assert_called_once_with('abs path')
        _get_content.assert_called_once_with()
        _compress.assert_called_once_with('abs path')
        _write.assert_called_once_with('content', CONTENT_XML)
