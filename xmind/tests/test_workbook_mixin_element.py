import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from xmind.core.mixin import WorkbookMixinElement
from xmind.tests import logging_configuration as lc
from xmind.tests import base
from xmind.core.const import ATTR_TIMESTAMP, ATTR_ID


class WorkbookMixinElementTest(base.Base):
    """WorkbookMixinElement test"""

    def setUp(self):
        super(WorkbookMixinElementTest, self).setUp()

        self._init_method = self._init_patch_with_name(
            '_init',
            'xmind.core.Element.__init__',
            autospec=True
        )
        self._registOwnerWorkbook = self._init_patch_with_name(
            '_registOwnerWorkbook',
            'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook',
            autospec=True
        )
        self._ownerWorkbook = MagicMock()

    def _assert_init_with_object(self, element, node=None):
        self._init_method.assert_called_once_with(element, node)
        self._registOwnerWorkbook.assert_called_once_with(element)

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('WorkbookMixinElementTest')
        return self._logger

    def test_init_with_parameters(self):
        """Test __init__ method with parameters"""
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        self.assertEqual(obj._owner_workbook, self._ownerWorkbook)
        self._assert_init_with_object(obj, "test")

    def test_excessive_parameters(self):

        _element = WorkbookMixinElement()
        self._assert_init_with_object(_element)
        self._remove_patched_function('_registOwnerWorkbook')

        _parameters = [
            ('registOwnerWorkbook', 0),
            ('getOwnerWorkbook', 0),
            ('setOwnerWorkbook', 1),
            ('getModifiedTime', 0),
            ('setModifiedTime', 1),
            ('updateModifiedTime', 0),
            ('getID', 0)
        ]
        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_regist_owner_workbook(self):
        """Test registOwnerWorkbook method with NOT empty ownerWorkbook object"""
        self._setOwnerDocument_method = self._init_patch_with_name(
            '_setOwnerDocument', 'xmind.core.Element.setOwnerDocument', autospec=True)
        self._ownerWorkbook.getOwnerDocument.return_value = "owner"

        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        self._assert_init_with_object(obj, "test")
        self._remove_patched_function('_registOwnerWorkbook')

        obj.registOwnerWorkbook()
        self._setOwnerDocument_method.assert_called_once_with(obj, "owner")

    def test_regist_none_owner_workbook(self):
        """Test registOwnerWorkbook method with empty ownerWorkbook object"""
        self._setOwnerDocument_method = self._init_patch_with_name(
            '_setOwnerDocument', 'xmind.core.Element.setOwnerDocument', autospec=True)
        self._ownerWorkbook.getOwnerDocument.return_value = "owner"

        obj = WorkbookMixinElement("test", None)
        self._assert_init_with_object(obj, "test")
        self._remove_patched_function('_registOwnerWorkbook')

        obj.registOwnerWorkbook()

        self._setOwnerDocument_method.assert_not_called()

    def test_get_owner_workbook(self):
        """Test getOwnerWorkbook method"""
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getOwnerWorkbook(), self._ownerWorkbook)

        self._assert_init_with_object(obj, "test")

    def test_set_owner_workbook(self):
        """Test setOwnerWorkbook method with None owner_workbook"""
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        obj._owner_workbook = None
        self.assertIsNone(obj._owner_workbook)

        obj.setOwnerWorkbook('newOwner')
        self.assertEqual('newOwner', obj._owner_workbook)
        self._assert_init_with_object(obj, "test")

    def test_set_already_set_owner_workbook(self):
        """Test setOwnerWorkbook method when owner_workbook is set"""
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        obj.setOwnerWorkbook("bbb")
        self.assertEqual(obj.getOwnerWorkbook(), self._ownerWorkbook)
        self._assert_init_with_object(obj, "test")

    def test_get_modified_time_with_none_timestamp(self):
        """Test getModifiedTime method when getAttribute returns None obj"""
        self._getAttribute_method = self._init_patch_with_name(
            '_getAttribute',
            'xmind.core.Element.getAttribute',
            return_value=None,
            autospec=True
        )
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        self.assertIsNone(obj.getModifiedTime())

        self._getAttribute_method.assert_called_once_with(obj, ATTR_TIMESTAMP)
        self._assert_init_with_object(obj, "test")

    def test_get_modified_time(self):
        """Test getModifiedTime method when getAttribute returns number"""
        self._getAttribute_method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute', return_value=1, autospec=True)
        self._readable_time_method = self._init_patch_with_name(
            '_readable_time', 'xmind.utils.readable_time', return_value="time", autospec=True)

        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getModifiedTime(), "time")
        self._getAttribute_method.assert_called_once_with(obj, ATTR_TIMESTAMP)
        self._readable_time_method.assert_called_once_with(1)
        self._assert_init_with_object(obj, "test")

    def test_set_modified_time(self):
        """Test setModifiedTime method, input parameter is number"""
        self._setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute', autospec=True)
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        obj.setModifiedTime(1234)
        self._setAttribute__method.assert_called_once_with(
            obj, "timestamp", 1234)
        self._assert_init_with_object(obj, "test")

    def test_set_modified_time_throws(self):
        """Test setModifiedTime method, input parameter is NOT number"""
        self._setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute',
            thrown_exception=Exception("super error"), autospec=True)
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        with self.assertRaises(Exception) as ex:
            obj.setModifiedTime(0)

        self.assertTrue(ex.exception.args[0].find(
            "super error") == 0)

        self._setAttribute__method.assert_called_once_with(
            obj, ATTR_TIMESTAMP, 0)
        self._assert_init_with_object(obj, "test")

    def test_update_modified_time(self):
        """Test updateModifiedTime method"""
        self._get_current_time_method = self._init_patch_with_name(
            '_get_current_time', 'xmind.utils.get_current_time', return_value=12345, autospec=True)

        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        with patch.object(obj, 'setModifiedTime') as _mock:
            self.assertIsNone(obj.updateModifiedTime())

        self._get_current_time_method.assert_called_once_with()
        _mock.assert_called_once_with(12345)
        self._assert_init_with_object(obj, "test")

    def test_get_ID(self):
        """Test getID method"""
        self._getAttribute__method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute', return_value="value", autospec=True)

        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getID(), "value")
        self._getAttribute__method.assert_called_once_with(obj, ATTR_ID)
        self._assert_init_with_object(obj, 'test')
