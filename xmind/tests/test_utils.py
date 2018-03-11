from xmind.tests import logging_configuration as lc
from xmind.utils import (
    extract,
    compress,
    get_abs_path,
    get_current_time,
    readable_time,
    generate_id,
    prevent,
    check
)
from xmind.tests import base
from unittest.mock import patch, Mock, PropertyMock, call


class TestUtils(base.Base):
    """Tests for utils module"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('Utils')
        return self._logger

    @patch('xmind.utils.zipfile.ZipFile')
    def test_extract(self, mock_zipfile):
        mock_zipfile.return_value = 'extracted_value'
        self.assertEqual('extracted_value', extract('some_path'))
        mock_zipfile.assert_called_once_with('some_path', 'r')

    @patch('xmind.utils.zipfile.ZipFile')
    def test_extract_by_excessive_parameters(self, mock_zipfile):
        mock_zipfile.return_value = 'WillNotReachHere'
        with self.assertRaises(Exception) as _exception_more_parameters:
            extract('some_path2', 2)
        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "extract() takes 1 positional argument but 2 were given") == 0,
            _exception_more_parameters.exception.args[0])
        mock_zipfile.assert_not_called()

    @patch('xmind.utils.zipfile.ZipFile')
    def test_extract_without_parameters(self, mock_zipfile):
        mock_zipfile.return_value = 'WillNotReachHere'
        with self.assertRaises(Exception) as _exception_none_parameters:
            extract()
        self.assertTrue(_exception_none_parameters.exception.args[0].find(
            "extract() missing 1 required positional argument: 'path'") == 0,
            _exception_none_parameters.exception.args[0])
        mock_zipfile.assert_not_called()

    @patch('xmind.utils.zipfile.ZipFile')
    def test_compress(self, mock_zipfile):
        mock_zipfile.return_value = 'extracted_value'
        self.assertEqual('extracted_value', compress('some_path'))
        mock_zipfile.assert_called_once_with('some_path', 'w')

    @patch('xmind.utils.zipfile.ZipFile')
    def test_compress_by_excessive_parameters(self, mock_zipfile):
        mock_zipfile.return_value = 'WillNotReachHere'
        with self.assertRaises(Exception) as _exception_more_parameters:
            compress('some_path2', 2)
        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "compress() takes 1 positional argument but 2 were given") == 0,
            _exception_more_parameters.exception.args[0])
        mock_zipfile.assert_not_called()

    @patch('xmind.utils.zipfile.ZipFile')
    def test_compress_without_parameters(self, mock_zipfile):
        mock_zipfile.return_value = 'WillNotReachHere'
        with self.assertRaises(Exception) as _exception_none_parameters:
            compress()
        self.assertTrue(_exception_none_parameters.exception.args[0].find(
            "compress() missing 1 required positional argument: 'path'") == 0,
            _exception_none_parameters.exception.args[0])
        mock_zipfile.assert_not_called()

    @patch('xmind.utils.os.path.split')
    @patch('xmind.utils.os.getcwd')
    @patch('xmind.utils.os.path.abspath')
    @patch('xmind.utils.os.path.expanduser')
    @patch('xmind.utils.join_path')
    def test_get_abs_path_fp_is_none(
            self,
            join_path,
            os_path_expanduser,
            os_path_abspath,
            os_getcwd,
            os_path_split):
        os_path_split.return_value = (None, 'somePath')
        os_getcwd.return_value = 'NewFp'
        os_path_expanduser.side_effect = Exception('In expanduser')

        with self.assertRaises(Exception) as _exception:
            get_abs_path('super_path')

        self.assertTrue(_exception.exception.args[0].find(
            "In expanduser") == 0,
            _exception.exception.args[0])

        os_path_split.assert_called_once_with('super_path')
        os_getcwd.assert_called_once_with()
        os_path_abspath.assert_not_called()
        os_path_expanduser.assert_called_once_with('NewFp')
        join_path.assert_not_called()

    @patch('xmind.utils.os.path.split')
    @patch('xmind.utils.os.getcwd')
    @patch('xmind.utils.os.path.abspath')
    @patch('xmind.utils.os.path.expanduser')
    @patch('xmind.utils.join_path')
    def test_get_abs_path(
            self,
            join_path,
            os_path_expanduser,
            os_path_abspath,
            os_getcwd,
            os_path_split):
        os_path_split.return_value = ('path', 'filename.ext')
        os_path_expanduser.return_value = 'userName'
        os_path_abspath.return_value = 'newAbsolutePath'
        join_path.return_value = "joined_abs_path"

        self.assertEqual('joined_abs_path', get_abs_path('super_path'))

        os_path_split.assert_called_once_with('super_path')
        os_getcwd.assert_not_called()
        os_path_abspath.assert_called_once_with('userName')
        os_path_expanduser.assert_called_once_with('path')
        join_path.assert_called_once_with('newAbsolutePath', 'filename.ext')

    @patch('xmind.utils.os.path.split')
    @patch('xmind.utils.os.getcwd')
    @patch('xmind.utils.os.path.abspath')
    @patch('xmind.utils.os.path.expanduser')
    @patch('xmind.utils.join_path')
    def test_get_abs_path_by_excessive_parameters(
            self,
            join_path,
            os_path_expanduser,
            os_path_abspath,
            os_getcwd,
            os_path_split):
        with self.assertRaises(Exception) as _exception_more_parameters:
            get_abs_path('some_path2', 2)
        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "get_abs_path() takes 1 positional argument but 2 were given") == 0,
            _exception_more_parameters.exception.args[0])
        os_path_split.assert_not_called()
        os_getcwd.assert_not_called()
        os_path_abspath.assert_not_called()
        os_path_expanduser.assert_not_called()
        join_path.assert_not_called()

    @patch('xmind.utils.os.path.split')
    @patch('xmind.utils.os.getcwd')
    @patch('xmind.utils.os.path.abspath')
    @patch('xmind.utils.os.path.expanduser')
    @patch('xmind.utils.join_path')
    def test_get_abs_path_without_parameters(
            self,
            join_path,
            os_path_expanduser,
            os_path_abspath,
            os_getcwd,
            os_path_split):
        with self.assertRaises(Exception) as _exception_none_parameters:
            get_abs_path()
        self.assertTrue(_exception_none_parameters.exception.args[0].find(
            "get_abs_path() missing 1 required positional argument: 'path'") == 0,
            _exception_none_parameters.exception.args[0])
        os_path_split.assert_not_called()
        os_getcwd.assert_not_called()
        os_path_abspath.assert_not_called()
        os_path_expanduser.assert_not_called()
        join_path.assert_not_called()

    @patch('xmind.utils.time.time')
    def test_get_current_time(self, time_time):
        time_time.return_value = 1.4
        self.assertEqual(1400, get_current_time())
        time_time.assert_called_once_with()

    @patch('xmind.utils.time.time')
    def test_get_current_time_by_excessive_parameters(self, time_time):
        time_time.return_value = 1.4
        with self.assertRaises(Exception) as _exception_more_parameters:
            get_current_time(1400)
        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "get_current_time() takes 0 positional arguments but 1 was given") == 0,
            _exception_more_parameters.exception.args[0])
        time_time.assert_not_called()

    def test_readable_time(self):
        self.assertEqual('02/06/2018 05:00:00', readable_time(1517893200000))

        # excessive paramters
        with self.assertRaises(Exception) as _exception_more_parameters:
            readable_time(1400, 'UTC')
        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "readable_time() takes 1 positional argument but 2 were given") == 0,
            _exception_more_parameters.exception.args[0])

    @patch('xmind.utils.md5')
    @patch('xmind.utils.get_current_time')
    @patch('xmind.utils.random.random')
    def test_generate_id(
            self,
            random_mock,
            get_current_time_mock,
            md5_mock):
        _mock = Mock()
        _mock.hexdigest.side_effect = [
            '55555555555555555555555555555555',
            '12121212121212121212121212121212',
        ]
        md5_mock.return_value = _mock
        get_current_time_mock.return_value = 567890
        random_mock.return_value = 345345

        self.assertEqual('55555555555551212121212121', generate_id())

        random_mock.assert_called_once_with()
        get_current_time_mock.assert_called_once_with()
        self.assertEqual(2, md5_mock.call_count)
        self.assertListEqual(
            [
                call(b'567890'),
                call(b'345345')
            ],
            md5_mock.call_args_list
        )
        self.assertEqual(2, _mock.hexdigest.call_count)

    @patch('xmind.utils.md5')
    @patch('xmind.utils.get_current_time')
    @patch('xmind.utils.random.random')
    def test_generate_id_by_excessive_parameters(
            self,
            random_mock,
            get_current_time_mock,
            md5_mock):

        with self.assertRaises(Exception) as _exception_more_parameters:
            generate_id(1400)

        self.assertTrue(_exception_more_parameters.exception.args[0].find(
            "generate_id() takes 0 positional arguments but 1 was given") == 0,
            _exception_more_parameters.exception.args[0])

        random_mock.assert_not_called()
        get_current_time_mock.assert_not_called()
        md5_mock.assert_not_called()

    def test_prevent_decorator(self):
        @prevent
        def function_to_test(value_to_check_after):
            value_to_check_after['value'] = True
            raise Exception("We will not catch it")

        to_check = dict(value=False)
        function_to_test(to_check)
        self.assertTrue(to_check['value'])

    def test_check_decorator(self):
        class TestObject(object):
            def __init__(self):
                self._some_attribute = 'value'

            @check('_some_attribute')
            def run(self):
                return 'superValue'

            @check('_some_attribute2')
            def run2(self):
                return 'willNotComeHere'

        _object_to_test = TestObject()
        self.assertIsNone(_object_to_test.run2())
        self.assertEqual('superValue', _object_to_test.run())
