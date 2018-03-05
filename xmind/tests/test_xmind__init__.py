from xmind.tests import logging_configuration as lc
from xmind.tests import base
from xmind import *
from unittest.mock import Mock, call


class TestXmindInit(base.Base):
    """Tests for xmind.__init__.py file"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('xmindInit')
        return self._logger

    def test_excessive_parameters(self):
        _workbook_loader = self._init_patch_with_name(
            '_workbook_loader', 'xmind.WorkbookLoader')
        _workbook_saver = self._init_patch_with_name(
            '_workbook_saver', 'xmind.WorkbookSaver')

        with self.assertRaises(TypeError) as _ex:
            load("test", "test")
        self.getLogger().debug("Got an exception: '%s'", _ex.exception.args[0])
        self.assertTrue(_ex.exception.args[0].find(
            "%s() takes" % "load") != -1)

        with self.assertRaises(TypeError) as _exNone:
            load()
        self.getLogger().debug("Got an exception: '%s'",
                               _exNone.exception.args[0])
        self.assertTrue(_exNone.exception.args[0].find(
            "%s() missing" % "load") != -1)

        with self.assertRaises(TypeError) as _ex:
            save("test", "test", "test")
        self.getLogger().debug("Got an exception: '%s'", _ex.exception.args[0])
        self.assertTrue(_ex.exception.args[0].find(
            "%s() takes" % "save") != -1)

        with self.assertRaises(TypeError) as _exNone:
            save()
        self.getLogger().debug("Got an exception: '%s'",
                               _exNone.exception.args[0])
        self.assertTrue(_exNone.exception.args[0].find(
            "%s() missing" % "save") != -1)

        _workbook_loader.assert_not_called()
        _workbook_saver.assert_not_called()

    def test_load(self):
        _workbook_loader_obj = Mock()
        _workbook_loader_obj.get_workbook.return_value = "workbook"
        _workbook_loader = self._init_patch_with_name(
            '_workbook_loader', 'xmind.WorkbookLoader', return_value=_workbook_loader_obj)

        self.assertEqual(load("path"), "workbook")
        _workbook_loader.assert_called_once_with("path")
        _workbook_loader_obj.get_workbook.assert_called_once()

    def test_save(self):
        _workbook_saver_obj = Mock()
        _workbook_saver_obj.save.return_value = None
        _workbook_saver = self._init_patch_with_name(
            '_workbook_saver', 'xmind.WorkbookSaver', return_value=_workbook_saver_obj)

        self.assertIsNone(save("workbook1"))
        self.assertIsNone(save("workbook2", "path"))

        self.assertEqual(2, _workbook_saver.call_count)
        self.assertListEqual(
            [
                call("workbook1"),
                call("workbook2")
            ],
            _workbook_saver.call_args_list
        )

        self.assertEqual(2, _workbook_saver_obj.save.call_count)
        self.assertListEqual(
            [
                call(None),
                call("path")
            ],
            _workbook_saver_obj.save.call_args_list
        )
