from xmind.tests import logging_configuration as lc
from xmind.core.workbook import WorkbookDocument
from xmind.tests import base
from unittest.mock import patch, Mock, MagicMock
from xmind.core.const import *


class TestWorkbookDocument(base.Base):
    """Test class for WorkbookDocument class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('workbookDocument')
        return self._logger

    def setUp(self):
        super(TestWorkbookDocument, self).setUp()
        self._init_document = self._init_patch_with_name('_init', 'xmind.core.Document.__init__')
        self._get_first_child_node_by_tag_name = self._init_patch_with_name('_get_first_child_node_by_tag_name', 'xmind.core.workbook.WorkbookDocument.getFirstChildNodeByTagName')
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement')
        self._append_child = self._init_patch_with_name('_append_child', 'xmind.core.workbook.WorkbookDocument.appendChild')
        self._set_version = self._init_patch_with_name('_set_version', 'xmind.core.workbook.WorkbookDocument.setVersion')

    def _assert_init_methods(self, _workbook_document, _getFirstChildNode_return_value=None):
        self._init_document.assert_called_once_with(None)
        self._get_first_child_node_by_tag_name.assert_called_once_with(TAG_WORKBOOK)
        self._workbook_element.assert_called_once_with(_getFirstChildNode_return_value, _workbook_document)
        self._set_version.assert_called_once_with(VERSION)

    def test_excessive_parameters(self):
        _workbook_document = WorkbookDocument()

        _parameters = [
            ('__init__', (2, False)),
            ('getWorkbookElement', 0),
            ('_create_relationship', 0),
            ('createRelationship', 2),
            ('createTopic', 0),
            ('getSheets', 0),
            ('getPrimarySheet', 0),
            ('createSheet', 0),
            ('addSheet', 2),
            ('removeSheet', 1),
            ('moveSheet', 2),
            ('getVersion', 0),
            ('getModifiedTime', 0),
            ('updateModifiedTime', 0),
            ('setModifiedTime', 0),
            ('get_path', 0),
            ('set_path', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _workbook_document)

        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_init(self):
        _workbook_document = WorkbookDocument()

        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_init_appendChild_is_not_called(self):
        self._remove_patched_function("_get_first_child_node_by_tag_name")

        _workbook_element = Mock()
        self._get_first_child_node_by_tag_name = self._init_patch_with_name('_get_first_child_node_by_tag_name', 'xmind.core.workbook.WorkbookDocument.getFirstChildNodeByTagName', return_value=_workbook_element)

        _workbook_document = WorkbookDocument()
        self._append_child.assert_not_called()
        self._assert_init_methods(_workbook_document, _workbook_element)

    def test_get_workbook_element(self):
        _workbook_document = WorkbookDocument()

        self._append_child.assert_called_once_with(None)
        self.assertIsNone(_workbook_document.getWorkbookElement())
        self._assert_init_methods(_workbook_document)

    def test_create_relationship(self):
        _relationship_element = self._init_patch_with_name('_relationship_element', 'xmind.core.workbook.RelationshipElement', return_value="RelationshipElement")

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document._create_relationship(), "RelationshipElement")
        _relationship_element.assert_called_once_with(None, _workbook_document)
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_createRelationship_sheet_is_none(self):
        _sheet1 = Mock()
        _sheet1.getImplementation.return_value = None
        _end1 = Mock()
        _end1.getOwnerSheet.return_value = _sheet1

        _end2 = Mock()
        _end2.getOwnerSheet.return_value = None

        _workbook_document = WorkbookDocument()

        with self.assertRaises(Exception) as _ex:
            _workbook_document.createRelationship(_end1, _end2)
        self.assertTrue(_ex.exception.args[0].find("Topics not on the same sheet!") != -1)
        _end1.getOwnerSheet.assert_called_once()
        _end2.getOwnerSheet.assert_called_once()
        _sheet1.getImplementation.assert_not_called()
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_createRelationship_implementations_not_equal(self):
        _sheet1 = Mock()
        _sheet1.getImplementation.return_value = "implementation1"
        _end1 = Mock()
        _end1.getOwnerSheet.return_value = _sheet1

        _sheet2 = Mock()
        _sheet2.getImplementation.return_value = "implementation2"
        _end2 = Mock()
        _end2.getOwnerSheet.return_value = _sheet2

        _create_relationship = self._init_patch_with_name('_create_relationship', 'xmind.core.workbook.WorkbookDocument._create_relationship')

        _workbook_document = WorkbookDocument()

        with self.assertRaises(Exception) as _ex:
            _workbook_document.createRelationship(_end1, _end2)
        self.assertTrue(_ex.exception.args[0].find("Topics not on the same sheet!") != -1)
        _end1.getOwnerSheet.assert_called_once()
        _end2.getOwnerSheet.assert_called_once()
        _sheet1.getImplementation.assert_called_once()
        _sheet2.getImplementation.assert_called_once()
        _create_relationship.assert_not_called()
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_createRelationship(self):
        _sheet1 = Mock()
        _sheet1.getImplementation.return_value = "implementation"
        _sheet1.addRelationships.return_value = None
        _end1 = Mock()
        _end1.getOwnerSheet.return_value = _sheet1
        _end1.getID.return_value = "ID1"

        _sheet2 = Mock()
        _sheet2.getImplementation.return_value = "implementation"
        _end2 = Mock()
        _end2.getOwnerSheet.return_value = _sheet2
        _end2.getID.return_value = "ID2"

        _rel = Mock()
        _rel.setEnd1ID.return_value = None
        _rel.setEnd2ID.return_value = None

        _create_relationship = self._init_patch_with_name('_create_relationship', 'xmind.core.workbook.WorkbookDocument._create_relationship', return_value=_rel)

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document.createRelationship(_end1, _end2), _rel)
        _end1.getOwnerSheet.assert_called_once()
        _end2.getOwnerSheet.assert_called_once()
        _sheet1.getImplementation.assert_called_once()
        _sheet2.getImplementation.assert_called_once()
        _create_relationship.assert_called_once()
        _end1.getID.assert_called_once()
        _end2.getID.assert_called_once()
        _rel.setEnd1ID.assert_called_once_with("ID1")
        _rel.setEnd2ID.assert_called_once_with("ID2")
        _sheet1.addRelationships.assert_called_once_with(_rel)
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_create_topic(self):
        _topic_element = self._init_patch_with_name('_relationship_element', 'xmind.core.workbook.TopicElement', return_value="TopicElement")

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document.createTopic(), "TopicElement")
        _topic_element.assert_called_once_with(None, _workbook_document)
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_get_sheets(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.getSheets.return_value = ["sheet1", "sheet2"]
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertListEqual(_workbook_document.getSheets(), ["sheet1", "sheet2"])
        _obj.getSheets.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_get_primary_sheets(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.getSheetByIndex.return_value = "sheet1"
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document.getPrimarySheet(), "sheet1")
        _obj.getSheetByIndex.assert_called_once_with(0)
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_create_sheet(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.createSheet.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.createSheet())
        _obj.createSheet.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_add_sheet(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.addSheet.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.addSheet("sheet1"))
        _obj.addSheet.assert_called_once_with("sheet1", None)
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_remove_sheet(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.removeSheet.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.removeSheet("sheet"))
        _obj.removeSheet.assert_called_once_with("sheet")
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_move_sheet(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.moveSheet.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.moveSheet(0, 2))
        _obj.moveSheet.assert_called_once_with(0, 2)
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_get_version(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.getVersion.return_value = "Version"
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document.getVersion(), "Version")
        _obj.getVersion.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_get_modified_time(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.getModifiedTime.return_value = "ModifiedTime"
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertEqual(_workbook_document.getModifiedTime(), "ModifiedTime")
        _obj.getModifiedTime.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_update_modified_time(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.updateModifiedTime.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.updateModifiedTime())
        _obj.updateModifiedTime.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_set_modified_time(self):
        self._remove_patched_function("_workbook_element")
        _obj = Mock()
        _obj.setModifiedTime.return_value = None
        self._workbook_element = self._init_patch_with_name('_workbook_element', 'xmind.core.workbook.WorkbookElement', return_value=_obj)

        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.setModifiedTime())
        _obj.setModifiedTime.assert_called_once()
        self._append_child.assert_called_once_with(_obj)
        self._assert_init_methods(_workbook_document)

    def test_get_path_is_none(self):
        _get_abs_path = self._init_patch_with_name('_get_abs_path', 'xmind.core.utils.get_abs_path')
        _workbook_document = WorkbookDocument()

        self.assertIsNone(_workbook_document.get_path())
        _get_abs_path.assert_not_called()
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_get_path_is_not_none(self):
        _get_abs_path = self._init_patch_with_name('_get_abs_path', 'xmind.core.utils.get_abs_path', return_value="abs_path")
        _workbook_document = WorkbookDocument(None, "path")

        self.assertEqual(_workbook_document.get_path(), "abs_path")
        _get_abs_path.assert_called_with("path")
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

    def test_set_path(self):
        _get_abs_path = self._init_patch_with_name('_get_abs_path', 'xmind.core.utils.get_abs_path', return_value="abs_path")
        _workbook_document = WorkbookDocument(None, "path")

        self.assertIsNone(_workbook_document.set_path("path"))
        self.assertEqual(_workbook_document._path, "abs_path")
        _get_abs_path.assert_called_with("path")
        self._append_child.assert_called_once_with(None)
        self._assert_init_methods(_workbook_document)

