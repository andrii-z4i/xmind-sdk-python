from xmind.tests import logging_configuration as lc
from xmind.core.sheet import SheetElement
from xmind.tests import base
from unittest.mock import patch, Mock, MagicMock
from xmind.core.const import *


class TestSheetElement(base.Base):
    """Test class for SheetElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('sheetElement')
        return self._logger

    def setUp(self):
        super(TestSheetElement, self).setUp()
        self._init_method = self._init_patch_with_name(
            '_init', 'xmind.core.sheet.WorkbookMixinElement.__init__')
        self._add_id_attribute = self._init_patch_with_name(
            '_add_id_attribute', 'xmind.core.sheet.SheetElement.addIdAttribute')
        self._get_root_topic = self._init_patch_with_name(
            '_get_root_topic', 'xmind.core.sheet.SheetElement._get_root_topic')

    def _assert_init_methods(self):
        self._init_method.assert_called_once_with(None, None)
        self._add_id_attribute.assert_called_once_with(ATTR_ID)
        self._get_root_topic.assert_called_once()

    def test_excessive_parameters(self):
        _element = SheetElement()
        self._assert_init_methods()

        self._remove_patched_function("_get_root_topic")

        _parameters = [
            ('__init__', (2, False)),
            ('_get_root_topic', 0),
            ('createRelationship', 3),
            ('_getRelationships', 0),
            ('addRelationship', 1),
            ('removeRelationship', 1),
            ('getRootTopic', 0),
            ('_get_title', 0),
            ('getTitle', 0),
            ('setTitle', 1),
            ('getParent', 0),
            ('updateModifiedTime', 0)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_init(self):
        SheetElement()
        self._assert_init_methods()

    def test_get_root_topic_without_topic(self):
        _get_child_nodes_by_tag_name = self._init_patch_with_name(
            '_get_child_nodes_by_tag_name', 'xmind.core.sheet.SheetElement.getChildNodesByTagName', return_value=[])
        _owner_workbook = Mock()
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_owner_workbook)
        _obj_topic_element = Mock()
        _topic_element = self._init_patch_with_name(
            '_topic_element', 'xmind.core.sheet.TopicElement', return_value=_obj_topic_element)
        _append_child = self._init_patch_with_name(
            '_append_child', 'xmind.core.sheet.SheetElement.appendChild')

        _obj = SheetElement()
        self._assert_init_methods()
        self._remove_patched_function("_get_root_topic")
        self.assertEqual(_obj._get_root_topic(), _obj_topic_element)

        _get_child_nodes_by_tag_name.assert_called_once_with(TAG_TOPIC)

        _get_owner_workbook.assert_called_once()

        _topic_element.assert_called_once()
        _topic_element.assert_called_with(ownerWorkbook=_owner_workbook)

        _append_child.assert_called_once()
        _append_child.assert_called_with(_obj_topic_element)

    def test_get_root_topic_with_topic(self):
        _get_child_nodes_by_tag_name = self._init_patch_with_name(
            '_get_child_nodes_by_tag_name', 'xmind.core.sheet.SheetElement.getChildNodesByTagName', return_value=[1])
        _owner_workbook = Mock()
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_owner_workbook)
        _obj_topic_element = Mock()
        _topic_element = self._init_patch_with_name(
            '_topic_element', 'xmind.core.sheet.TopicElement', return_value=_obj_topic_element)

        _obj = SheetElement()
        self._assert_init_methods()
        self._remove_patched_function("_get_root_topic")

        self.assertEqual(_obj._get_root_topic(), _obj_topic_element)

        _get_child_nodes_by_tag_name.assert_called_once_with(TAG_TOPIC)

        _get_owner_workbook.assert_called_once()
        _topic_element.assert_called_once()
        _topic_element.assert_called_with(1, _owner_workbook)

    def test_create_relationship_without_title(self):
        _rel = Mock()
        _rel.setEnd1ID.return_value = None
        _rel.setEnd2ID.return_value = None
        _rel.setTitle.return_value = None
        _owner_workbook = Mock()
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_owner_workbook)
        _relationship_element = self._init_patch_with_name(
            '_relationship_element', 'xmind.core.sheet.RelationshipElement', return_value=_rel)

        _obj = SheetElement()

        self.assertEqual(_obj.createRelationship("one", "two"), _rel)

        _get_owner_workbook.assert_called_once()
        _relationship_element.assert_called_once_with(
            ownerWorkbook=_owner_workbook)
        _rel.setEnd1ID.assert_called_with("one")
        _rel.setEnd2ID.assert_called_with("two")
        _rel.setTitle.assert_not_called()
        self._assert_init_methods()

    def test_create_relationship_with_title(self):
        _rel = Mock()
        _rel.setEnd1ID.return_value = None
        _rel.setEnd2ID.return_value = None
        _rel.setTitle.return_value = None
        _owner_workbook = Mock()
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_owner_workbook)
        _relationship_element = self._init_patch_with_name(
            '_relationship_element', 'xmind.core.sheet.RelationshipElement', return_value=_rel)

        _obj = SheetElement()

        _title = Mock()
        self.assertEqual(_obj.createRelationship("one", "two", _title), _rel)

        _get_owner_workbook.assert_called_once()
        _relationship_element.assert_called_once_with(
            ownerWorkbook=_owner_workbook)
        _rel.setEnd1ID.assert_called_with("one")
        _rel.setEnd2ID.assert_called_with("two")
        _rel.setTitle.assert_called_with(_title)
        self._assert_init_methods()

    def test_get_relationships(self):
        _get_first_child_node_by_tag_name = self._init_patch_with_name(
            '_get_first_child_node_by_tag_name', 'xmind.core.sheet.SheetElement.getFirstChildNodeByTagName')

        _obj = SheetElement()

        self.assertIsNone(_obj._getRelationships())
        _get_first_child_node_by_tag_name.assert_called_once_with(
            TAG_RELATIONSHIPS)
        self._assert_init_methods()

    def test_addRelationship_rels_are_none(self):
        _get_relationships = self._init_patch_with_name(
            '_get_relationships', 'xmind.core.sheet.SheetElement._getRelationships')
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')
        _rels = Mock()
        _rels.appendChild.return_value = None
        _relationships_element = self._init_patch_with_name(
            '_relationships_element', 'xmind.core.sheet.RelationshipsElement', return_value=_rels)
        _append_child = self._init_patch_with_name(
            '_append_child', 'xmind.core.sheet.SheetElement.appendChild')

        _obj = SheetElement()

        self.assertIsNone(_obj.addRelationship("test"))
        _get_relationships.assert_called_once()
        _get_owner_workbook.assert_called_once()
        _relationships_element.assert_called_once_with(None, None)
        _append_child.assert_called_once_with(_rels)
        _rels.appendChild.assert_called_once_with("test")
        self._assert_init_methods()

    def test_addRelationship_with_rels(self):
        _got_rel = Mock()
        _get_relationships = self._init_patch_with_name(
            '_get_relationships', 'xmind.core.sheet.SheetElement._getRelationships', return_value=_got_rel)
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')
        _rels = Mock()
        _rels.appendChild.return_value = None
        _relationships_element = self._init_patch_with_name(
            '_relationships_element', 'xmind.core.sheet.RelationshipsElement', return_value=_rels)
        _append_child = self._init_patch_with_name(
            '_append_child', 'xmind.core.sheet.SheetElement.appendChild')

        _obj = SheetElement()

        self.assertIsNone(_obj.addRelationship("test"))
        _get_relationships.assert_called_once()
        _get_owner_workbook.assert_called_once()
        _relationships_element.assert_called_once_with(_got_rel, None)
        _append_child.assert_not_called()
        _rels.appendChild.assert_called_once_with("test")
        self._assert_init_methods()

    def test_remove_relationship_without_set_up_relationships(self):
        _get_relationships = self._init_patch_with_name(
            '_get_relationships', 'xmind.core.sheet.SheetElement._getRelationships')

        _rel = Mock()
        _rel.getImplementation.return_value = None

        _obj = SheetElement()

        self.assertIsNone(_obj.removeRelationship(_rel))
        _get_relationships.assert_called_once()
        _rel.getImplementation.assert_not_called()
        self._assert_init_methods()

    def test_remove_relationship_with_set_up_relationships_and_without_child_nodes(self):
        _rels = Mock()
        _rels.removeChild.return_value = None
        _rels.hasChildNodes.return_value = None
        _get_relationships = self._init_patch_with_name(
            '_get_relationships', 'xmind.core.sheet.SheetElement._getRelationships', return_value=_rels)

        _get_implementation_obj = Mock()
        _get_implementation_obj.removeChild.return_value = None
        _get_implementation = self._init_patch_with_name(
            '_get_implementation', 'xmind.core.sheet.SheetElement.getImplementation', return_value=_get_implementation_obj)

        _update_modified_time = self._init_patch_with_name(
            '_update_modified_time', 'xmind.core.sheet.SheetElement.updateModifiedTime', )

        _rel = Mock()
        _rel.getImplementation.return_value = "test"

        _obj = SheetElement()

        self.assertIsNone(_obj.removeRelationship(_rel))
        _get_relationships.assert_called_once()
        _rel.getImplementation.assert_called_once()
        _rels.removeChild.assert_called_once_with("test")
        _rels.hasChildNodes.assert_called_once()
        _get_implementation.assert_called_once()
        _get_implementation_obj.removeChild.assert_called_once_with(_rels)
        _update_modified_time.assert_called_once()
        self._assert_init_methods()

    def test_remove_relationship_with_set_up_relationships_and_with_child_nodes(self):
        _rels = Mock()
        _rels.removeChild.return_value = None
        _rels.hasChildNodes.return_value = Mock()
        _get_relationships = self._init_patch_with_name(
            '_get_relationships', 'xmind.core.sheet.SheetElement._getRelationships', return_value=_rels)

        _get_implementation_obj = Mock()
        _get_implementation_obj.removeChild.return_value = None
        _get_implementation = self._init_patch_with_name(
            '_get_implementation', 'xmind.core.sheet.SheetElement.getImplementation', return_value=_get_implementation_obj)

        _update_modified_time = self._init_patch_with_name(
            '_update_modified_time', 'xmind.core.sheet.SheetElement.updateModifiedTime', )

        _rel = Mock()
        _rel.getImplementation.return_value = "test"

        _obj = SheetElement()

        self.assertIsNone(_obj.removeRelationship(_rel))
        _get_relationships.assert_called_once()
        _rel.getImplementation.assert_called_once()
        _rels.removeChild.assert_called_once_with("test")
        _rels.hasChildNodes.assert_called_once()
        _get_implementation.assert_not_called()
        _get_implementation_obj.removeChild.assert_not_called()
        _update_modified_time.assert_called_once()
        self._assert_init_methods()

    def test_get_root_topic(self):
        _obj = SheetElement()

        self.assertIsNone(_obj.getRootTopic())
        self._assert_init_methods()

    def test_get_title(self):
        _get_first_child_node_by_tag_name = self._init_patch_with_name(
            '_get_first_child_node_by_tag_name', 'xmind.core.sheet.SheetElement.getFirstChildNodeByTagName')

        _obj = SheetElement()

        self.assertIsNone(_obj._get_title())
        _get_first_child_node_by_tag_name.assert_called_once_with(TAG_TITLE)
        self._assert_init_methods()

    def test_getTitle_without_title(self):
        _get_title = self._init_patch_with_name(
            '_get_title', 'xmind.core.sheet.SheetElement._get_title')
        _title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.sheet.TitleElement')

        _obj = SheetElement()

        self.assertIsNone(_obj.getTitle())
        _get_title.assert_called_once()
        _title_element.assert_not_called()
        self._assert_init_methods()

    def test_getTitle_with_title(self):
        _get_title = self._init_patch_with_name(
            '_get_title', 'xmind.core.sheet.SheetElement._get_title', return_value="title")
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')

        _title_element_obj = Mock()
        _title_element_obj.getTextContent.return_value = "TextContext"
        _title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.sheet.TitleElement', return_value=_title_element_obj)

        _obj = SheetElement()

        self.assertEqual(_obj.getTitle(), "TextContext")
        _get_title.assert_called_once()
        _title_element.assert_called_with("title", None)
        _get_owner_workbook.assert_called_once()
        _title_element_obj.getTextContent.assert_called_once()
        self._assert_init_methods()

    def test_set_title_without_title(self):
        _get_title = self._init_patch_with_name(
            '_get_title', 'xmind.core.sheet.SheetElement._get_title')
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')
        _title_element_obj = Mock()
        _title_element_obj.setTextContent.return_value = None
        _title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.sheet.TitleElement', return_value=_title_element_obj)
        _append_child = self._init_patch_with_name(
            '_append_child', 'xmind.core.sheet.SheetElement.appendChild')
        _update_modified_time = self._init_patch_with_name(
            '_update_modified_time', 'xmind.core.sheet.SheetElement.updateModifiedTime')

        _obj = SheetElement()

        self.assertIsNone(_obj.setTitle("TextContent"))
        _get_owner_workbook.assert_called_once()
        _get_title.assert_called_once()
        _title_element.assert_called_with(None, None)
        _title_element_obj.setTextContent.assert_called_with("TextContent")
        _append_child.assert_called_with(_title_element_obj)
        _update_modified_time.assert_called_once()
        self._assert_init_methods()

    def test_set_title_with_title(self):
        _get_title = self._init_patch_with_name(
            '_get_title', 'xmind.core.sheet.SheetElement._get_title', return_value="title")
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')
        _title_element_obj = Mock()
        _title_element_obj.setTextContent.return_value = None
        _title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.sheet.TitleElement', return_value=_title_element_obj)
        _append_child = self._init_patch_with_name(
            '_append_child', 'xmind.core.sheet.SheetElement.appendChild')
        _update_modified_time = self._init_patch_with_name(
            '_update_modified_time', 'xmind.core.sheet.SheetElement.updateModifiedTime')

        _obj = SheetElement()

        self.assertIsNone(_obj.setTitle("TextContent"))
        _get_owner_workbook.assert_called_once()
        _get_title.assert_called_once()
        _title_element.assert_called_with("title", None)
        _title_element_obj.setTextContent.assert_called_with("TextContent")
        _append_child.assert_not_called()
        _update_modified_time.assert_called_once()
        self._assert_init_methods()

    def test_get_parent_without_workbook(self):
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook')
        _get_parent_node = self._init_patch_with_name(
            '_get_parent_node', 'xmind.core.sheet.SheetElement.getParentNode')

        _obj = SheetElement()

        self.assertIsNone(_obj.getParent())
        _get_owner_workbook.assert_called_once()
        _get_parent_node.assert_not_called()
        self._assert_init_methods()

    def test_get_parent_with_workbook_belonging_parent(self):
        _parent = Mock()
        _get_parent_node = self._init_patch_with_name(
            '_get_parent_node', 'xmind.core.sheet.SheetElement.getParentNode', return_value=_parent)
        _workbook_element = Mock()
        _workbook_element.getImplementation.return_value = _parent
        _workbook = Mock()
        _workbook.getWorkbookElement.return_value = _workbook_element
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_workbook)

        _obj = SheetElement()

        self.assertEqual(_obj.getParent(), _workbook)
        _get_owner_workbook.assert_called_once()
        _get_parent_node.assert_called_once()
        _workbook.getWorkbookElement.assert_called_once()
        _workbook_element.getImplementation.assert_called_once()
        self._assert_init_methods()

    def test_get_parent_with_workbook_not_belonging_parent(self):
        _parent = Mock()
        _get_parent_node = self._init_patch_with_name(
            '_get_parent_node', 'xmind.core.sheet.SheetElement.getParentNode', return_value=_parent)
        _workbook_element = Mock()
        _workbook_element.getImplementation.return_value = None
        _workbook = Mock()
        _workbook.getWorkbookElement.return_value = _workbook_element
        _get_owner_workbook = self._init_patch_with_name(
            '_get_owner_workbook', 'xmind.core.sheet.SheetElement.getOwnerWorkbook', return_value=_workbook)

        _obj = SheetElement()

        self.assertIsNone(_obj.getParent())
        _get_owner_workbook.assert_called_once()
        _get_parent_node.assert_called_once()
        _workbook.getWorkbookElement.assert_called_once()
        _workbook_element.getImplementation.assert_called_once()
        self._assert_init_methods()

    def test_update_modified_time_without_workbook(self):
        _update_modified_time_workbook_mixin_element = self._init_patch_with_name(
            '_update_modified_time_workbook_mixin_element', 'xmind.core.sheet.WorkbookMixinElement.updateModifiedTime')
        _get_parent = self._init_patch_with_name(
            '_get_parent', 'xmind.core.sheet.SheetElement.getParent')

        _obj = SheetElement()

        self.assertIsNone(_obj.updateModifiedTime())
        _update_modified_time_workbook_mixin_element.assert_called_once()
        _get_parent.assert_called_once()
        self._assert_init_methods()

    def test_update_modified_time_with_workbook(self):
        _update_modified_time_workbook_mixin_element = self._init_patch_with_name(
            '_update_modified_time_workbook_mixin_element', 'xmind.core.sheet.WorkbookMixinElement.updateModifiedTime')
        _workbook = Mock()
        _workbook.updateModifiedTime.return_value = "ModifiedTime"
        _get_parent = self._init_patch_with_name(
            '_get_parent', 'xmind.core.sheet.SheetElement.getParent', return_value=_workbook)

        _obj = SheetElement()

        self.assertIsNone(_obj.updateModifiedTime())
        _update_modified_time_workbook_mixin_element.assert_called_once()
        _get_parent.assert_called_once()
        _workbook.updateModifiedTime.assert_called_once()
        self._assert_init_methods()
