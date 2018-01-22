import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from xmind.core.mixin import WorkbookMixinElement
import logging
from . import base


class WorkbookMixinElementTest(base.Base):
    """WorkbookMixinElement test"""

    def setUp(self):
        super(WorkbookMixinElementTest, self).setUp()

        self._init_method = self._init_patch_with_name(
            '_init', 'xmind.core.Element.__init__')

        self._ownerWorkbook = MagicMock()

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = logging.getLogger('WorkbookMixinElementTest')
        return self._logger

    def test_init_with_parameters(self):
        """Test __init__ method with parameters"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj._owner_workbook, self._ownerWorkbook)
        self._init_method.assert_called_once_with("test")
        self._registOwnerWorkbook_method.assert_called_once()

    def test_excessive_parameters(self):
        _get_attribute = self._init_patch_with_name(
            '_get_attribute', 'xmind.core.Element.getOwnerDocument')
        _set_attribute = self._init_patch_with_name(
            '_set_attribute', 'xmind.core.Element.setOwnerDocument')
        _getAttribute_method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute')
        _readable_time_method = self._init_patch_with_name(
            '_readable_time', 'xmind.utils.readable_time')
        _get_current_time_method = self._init_patch_with_name(
            '_get_current_time', 'xmind.utils.get_current_time')
        _setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute')

        _element = WorkbookMixinElement()
        self._init_method.assert_called_once_with(None)

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

        _get_attribute.assert_not_called()
        _set_attribute.assert_not_called()
        _getAttribute_method.assert_not_called()
        _readable_time_method.assert_not_called()
        _get_current_time_method.assert_not_called()
        _setAttribute__method.assert_not_called()

    def test_regist_owner_workbook(self):
        """Test registOwnerWorkbook method with NOT empty ownerWorkbook object"""
        self._setOwnerDocument_method = self._init_patch_with_name(
            '_setOwnerDocument', 'xmind.core.Element.setOwnerDocument')
        self._ownerWorkbook.getOwnerDocument.return_value = "owner"

        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        obj.registOwnerWorkbook()

        self.assertEqual(self._setOwnerDocument_method.call_count, 2)

    def test_regist_none_owner_workbook(self):
        """Test registOwnerWorkbook method with empty ownerWorkbook object"""
        self._setOwnerDocument_method = self._init_patch_with_name(
            '_setOwnerDocument', 'xmind.core.Element.setOwnerDocument')
        self._ownerWorkbook.getOwnerDocument.return_value = "owner"

        self._ownerWorkbook = None
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        obj.registOwnerWorkbook()

        self._setOwnerDocument_method.assert_not_called()

    def test_get_owner_workbook(self):
        """Test getOwnerWorkbook method"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getOwnerWorkbook(), self._ownerWorkbook)

    def test_set_owner_workbook(self):
        """Test setOwnerWorkbook method with None owner_workbook"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        obj._owner_workbook = None

        obj.setOwnerWorkbook(self._ownerWorkbook)
        self.assertNotEqual(None, obj._owner_workbook)

    def test_set_already_set_owner_workbook(self):
        """Test setOwnerWorkbook method when owner_workbook is set"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        obj = WorkbookMixinElement("test", self._ownerWorkbook)
        owner = self._ownerWorkbook
        self._ownerWorkbook = MagicMock()
        obj.setOwnerWorkbook(self._ownerWorkbook)
        self.assertEqual(obj.getOwnerWorkbook(), owner)

    def test_get_modified_time_with_none_timestamp(self):
        """Test getModifiedTime method when getAttribute returns None obj"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._getAttribute_method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute', return_value=None)
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        _value = obj.getModifiedTime()
        self._getAttribute_method.assert_called_once_with('timestamp')
        self.assertEqual(_value, None)

    def test_get_modified_time(self):
        """Test getModifiedTime method when getAttribute returns number"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._getAttribute_method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute', return_value=1)
        self._readable_time_method = self._init_patch_with_name(
            '_readable_time', 'xmind.utils.readable_time', return_value="time")
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getModifiedTime(), "time")
        self._getAttribute_method.assert_called_once_with('timestamp')
        self._readable_time_method.assert_called_once_with(1)

    def test_set_modified_time(self):
        """Test setModifiedTime method, input parameter is number"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute')
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        obj.setModifiedTime(1234)
        self._setAttribute__method.assert_called_once_with("timestamp", 1234)

    def test_set_modified_time_throws(self):
        """Test setModifiedTime method, input parameter is NOT number"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute', Exception("ValueError"))
        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        with self.assertRaises(Exception) as ex:
            obj.setModifiedTime(None)

        self._setAttribute__method.assert_not_called()

        self.getLogger().warning("Exception: %s", ex.exception)

    def test_update_modified_time(self):
        """Test updateModifiedTime method"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._get_current_time_method = self._init_patch_with_name(
            '_get_current_time', 'xmind.utils.get_current_time', return_value=12345)
        self._setAttribute__method = self._init_patch_with_name(
            '_setAttribute', 'xmind.core.Element.setAttribute')

        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        obj.updateModifiedTime()
        self._get_current_time_method.assert_called_once()
        self._setAttribute__method.assert_called_once_with("timestamp", 12345)

    def test_get_ID(self):
        """Test getID method"""
        self._registOwnerWorkbook_method = self._init_patch_with_name(
            '_registOwnerWorkbook', 'xmind.core.mixin.WorkbookMixinElement.registOwnerWorkbook')
        self._getAttribute__method = self._init_patch_with_name(
            '_getAttribute', 'xmind.core.Element.getAttribute', return_value="value")

        obj = WorkbookMixinElement("test", self._ownerWorkbook)

        self.assertEqual(obj.getID(), "value")
        self._getAttribute__method.assert_called_once_with("id")
