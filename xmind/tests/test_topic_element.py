from xmind.tests import logging_configuration as lc
from xmind.core.topic import TopicElement
from xmind.tests import base
from unittest.mock import patch, Mock, PropertyMock, call
from xmind.core.const import (
    TAG_TOPIC,
    TAG_TOPICS,
    TAG_TITLE,
    TAG_MARKERREF,
    TAG_MARKERREFS,
    TAG_POSITION,
    TAG_CHILDREN,
    TAG_SHEET,
    ATTR_ID,
    ATTR_HREF,
    ATTR_BRANCH,
    VAL_FOLDED,
    TOPIC_ROOT,
    TOPIC_ATTACHED,
    ATTR_TYPE,
    TAG_NOTES)


class TestTopicElement(base.Base):
    """Test class for TopicElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('TopicElement')
        return self._logger

    def setUp(self):
        super(TestTopicElement, self).setUp()
        self._workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.topic.WorkbookMixinElement.__init__')
        self._add_attribute = self._init_patch_with_name(
            '_add_attribute', 'xmind.core.topic.TopicElement.addIdAttribute', return_value=True)

    def _assert_init_methods(self):
        self._workbook_mixin_element_init.assert_called_once_with(None, None)
        self._add_attribute.assert_called_once_with(ATTR_ID)

    def test_excessive_parameters(self):
        _element = TopicElement()
        self.assertEqual(TAG_TOPIC, _element.TAG_NAME)

        _parameters = [
            ('_get_title', 0),
            ('_get_markerrefs', 0),
            ('_get_position', 0),
            ('_get_children', 0),
            ('_set_hyperlink', 1),
            ('getOwnerSheet', 0),
            ('getTitle', 0),
            ('setTitle', 1),
            ('getMarkers', 0),
            ('addMarker', 1),
            ('setFolded', 0),
            ('getPosition', 0),
            ('setPosition', 2),
            ('removePosition', 0),
            ('getType', 0),
            ('getTopics', (1, False)),
            ('getSubTopics', (1, False)),
            ('getSubTopicByIndex', 2),
            ('addSubTopic', (3, False)),
            ('getIndex', 0),
            ('getHyperlink', 0),
            ('setFileHyperlink', 1),
            ('setTopicHyperlink', 1),
            ('setURLHyperlink', 1),
            ('getNotes', 0),
            ('_set_notes', 0),
            ('setPlainNotes', 1),
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

        self._assert_init_methods()

    def test_init_has_no_node_has_no_owner_workbook(self):
        _element = TopicElement()
        self._assert_init_methods()

    def test_init_by_excessive_parameters(self):
        with self.assertRaises(TypeError) as _ex:
            _element = TopicElement(1, 2, 3)
        self.assertEqual(
            '__init__() takes from 1 to 3 positional arguments but 4 were given', _ex.exception.args[0])

    def test_init_has_no_node_has_owner_workbook(self):
        _element = TopicElement(ownerWorkbook=5)
        self._workbook_mixin_element_init.assert_called_once_with(None, 5)
        self._add_attribute.assert_called_once_with(ATTR_ID)

    def test_init_has_node_has_no_owner_workbook(self):
        _element = TopicElement(3)
        self._workbook_mixin_element_init.assert_called_once_with(3, None)
        self._add_attribute.assert_called_once_with(ATTR_ID)

    def test_init_has_node_has_owner_workbook(self):
        _element = TopicElement(3, 5)
        self._workbook_mixin_element_init.assert_called_once_with(3, 5)
        self._add_attribute.assert_called_once_with(ATTR_ID)

    def test_get_title(self):
        _element = TopicElement()
        with patch.object(_element, 'getFirstChildNodeByTagName') as _mock:
            _mock.return_value = 10
            self.assertEqual(10, _element._get_title())
        _mock.assert_called_once_with(TAG_TITLE)
        self._assert_init_methods()

    def test_get_markerrefs(self):
        _element = TopicElement()
        with patch.object(_element, 'getFirstChildNodeByTagName') as _mock:
            _mock.return_value = 10
            self.assertEqual(10, _element._get_markerrefs())
        _mock.assert_called_once_with(TAG_MARKERREFS)
        self._assert_init_methods()

    def test_get_position(self):
        _element = TopicElement()
        with patch.object(_element, 'getFirstChildNodeByTagName') as _mock:
            _mock.return_value = 10
            self.assertEqual(10, _element._get_position())
        _mock.assert_called_once_with(TAG_POSITION)
        self._assert_init_methods()

    def test_get_children(self):
        _element = TopicElement()
        with patch.object(_element, 'getFirstChildNodeByTagName') as _mock:
            _mock.return_value = 10
            self.assertEqual(10, _element._get_children())
        _mock.assert_called_once_with(TAG_CHILDREN)
        self._assert_init_methods()

    def test_set_hyperlink(self):
        _element = TopicElement()
        with patch.object(_element, 'setAttribute') as _mock:
            _mock.return_value = 10
            self.assertIsNone(_element._set_hyperlink('url'))
        _mock.assert_called_once_with(ATTR_HREF, 'url')
        self._assert_init_methods()

    def test_getOwnerSheet_has_no_parent(self):
        _element = TopicElement()
        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_parent_node_mock.return_value = None

        self.assertIsNone(_element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_not_called()
        self._assert_init_methods()

    def test_getOwnerSheet_has_parent_no_parent_of_parent(self):
        _element = TopicElement()
        _parent = Mock(tagName=TAG_MARKERREFS)
        _parent_node = PropertyMock(return_value=None)
        type(_parent).parentNode = _parent_node

        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_parent_node_mock.return_value = _parent

        self.assertIsNone(_element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_not_called()
        _parent_node.assert_called_once()
        self._assert_init_methods()

    def test_getOwnerSheet_has_parent_has_no_owner_workbook(self):
        _element = TopicElement()
        _parent_of_parent = Mock(tagName=TAG_SHEET)
        _parent = Mock(tagName=TAG_MARKERREFS)
        _parent_node = PropertyMock(return_value=_parent_of_parent)
        type(_parent).parentNode = _parent_node

        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_owner_workbook_mock.return_value = None
        _get_parent_node_mock.return_value = _parent

        self.assertIsNone(_element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_called_once_with()
        _parent_node.assert_called_once()
        self._assert_init_methods()

    def test_getOwnerSheet_has_parent_has_owner_workbook_has_no_sheets(self):
        _element = TopicElement()
        _parent_of_parent = Mock(tagName=TAG_SHEET)
        _parent = Mock(tagName=TAG_MARKERREFS)
        _parent_node = PropertyMock(return_value=_parent_of_parent)
        type(_parent).parentNode = _parent_node

        _owner_workbook = Mock()
        _owner_workbook.getSheets.return_value = []
        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_owner_workbook_mock.return_value = _owner_workbook
        _get_parent_node_mock.return_value = _parent

        self.assertIsNone(_element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_called_once_with()
        _parent_node.assert_called_once()
        _owner_workbook.getSheets.assert_called_once()
        self._assert_init_methods()

    def test_getOwnerSheet_has_parent_has_owner_workbook_has_sheets_parent_is_no_sheet_impl(self):
        #  see https://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is-in-python to understand what is it 'is'
        _element = TopicElement()
        _parent_of_parent = Mock(tagName=TAG_SHEET)
        _parent = Mock(tagName=TAG_MARKERREFS)
        _parent_node = PropertyMock(return_value=_parent_of_parent)
        type(_parent).parentNode = _parent_node

        _sheet = Mock()
        _sheet.getImplementation.return_value = 10  # << parent is NOT 10 in our test
        _owner_workbook = Mock()
        _owner_workbook.getSheets.return_value = [_sheet]
        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_owner_workbook_mock.return_value = _owner_workbook
        _get_parent_node_mock.return_value = _parent

        self.assertIsNone(_element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_called_once_with()
        _parent_node.assert_called_once()
        _owner_workbook.getSheets.assert_called_once()
        _sheet.getImplementation.assert_called_once()
        self._assert_init_methods()

    def test_getOwnerSheet_has_parent_has_owner_workbook_has_sheets_parent_is_sheet_impl(self):
        #  see https://stackoverflow.com/questions/132988/is-there-a-difference-between-and-is-in-python to understand what is it 'is'
        _element = TopicElement()
        _parent_of_parent = Mock(tagName=TAG_SHEET)
        _parent = Mock(tagName=TAG_MARKERREFS)
        _parent_node = PropertyMock(return_value=_parent_of_parent)
        type(_parent).parentNode = _parent_node

        _sheet = Mock()
        # << parent is _parent_of_parent in our test
        _sheet.getImplementation.return_value = _parent_of_parent
        _owner_workbook = Mock()
        _owner_workbook.getSheets.return_value = [_sheet]
        _get_parent_node_mock = patch.object(_element, 'getParentNode').start()
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()

        _get_owner_workbook_mock.return_value = _owner_workbook
        _get_parent_node_mock.return_value = _parent

        self.assertEqual(_sheet, _element.getOwnerSheet())

        _get_parent_node_mock.assert_called_once_with()
        _get_owner_workbook_mock.assert_called_once_with()
        _parent_node.assert_called_once()
        _owner_workbook.getSheets.assert_called_once()
        _sheet.getImplementation.assert_called_once()
        self._assert_init_methods()

    def test_getTitle_has_no_title(self):
        _element = TopicElement()
        _create_title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.topic.TitleElement')
        with patch.object(_element, '_get_title') as _mock:
            _mock.return_value = None
            self.assertIsNone(_element.getTitle())

        _create_title_element.assert_not_called()
        _mock.assert_called_once_with()
        self._assert_init_methods()

    def test_getTitle_has_title(self):
        _element = TopicElement()
        _title = Mock()
        _title.getTextContent.return_value = 'NewValue'
        _create_title_element = self._init_patch_with_name(
            '_title_element', 'xmind.core.topic.TitleElement',
            return_value=_title)
        _wb_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _wb_mock.return_value = 'SomeWorkbook'
        _get_title_mock = patch.object(_element, '_get_title').start()
        _get_title_mock.return_value = 'SomeValue'

        self.assertEqual('NewValue', _element.getTitle())

        _create_title_element.assert_called_once_with(
            'SomeValue', 'SomeWorkbook')
        _wb_mock.assert_called_once_with()
        _get_title_mock.assert_called_once_with()
        _title.getTextContent.assert_called_once_with()
        self._assert_init_methods()

    def test_setTitle_title_is_None(self):
        _element = TopicElement()

        _title = Mock()
        _title.setTextContent.return_value = None

        _get_title_mock = self._init_patch_with_name('_get_title',
                                                     'xmind.core.topic.TopicElement._get_title',
                                                     return_value=None)
        _title_element_mock = self._init_patch_with_name('_title_element',
                                                         'xmind.core.topic.TitleElement',
                                                         return_value=_title)
        _append_child_mock = self._init_patch_with_name('_append_child',
                                                        'xmind.core.topic.TopicElement.appendChild')
        _get_owner_workbook_mock = self._init_patch_with_name('_get_owner_wb',
                                                              'xmind.core.topic.TopicElement.getOwnerWorkbook',
                                                              return_value='owner')

        _element.setTitle('someTitle')

        _get_title_mock.assert_called_once()
        _title_element_mock.assert_called_once_with(None, 'owner')
        _title.setTextContent.assert_called_once_with('someTitle')
        _get_owner_workbook_mock.assert_called_once()
        _append_child_mock.assert_called_once_with(_title)

    def test_setTitle_title_is_not_None(self):
        _element = TopicElement()

        _title = Mock()
        _title.setTextContent.return_value = None

        _get_title_mock = self._init_patch_with_name('_get_title',
                                                     'xmind.core.topic.TopicElement._get_title',
                                                     return_value='NiceTitle')
        _title_element_mock = self._init_patch_with_name('_title_element',
                                                         'xmind.core.topic.TitleElement',
                                                         return_value=_title)
        _append_child_mock = self._init_patch_with_name('_append_child',
                                                        'xmind.core.topic.TopicElement.appendChild')
        _get_owner_workbook_mock = self._init_patch_with_name('_get_owner_wb',
                                                              'xmind.core.topic.TopicElement.getOwnerWorkbook',
                                                              return_value='owner')

        _element.setTitle('someTitle')

        _get_title_mock.assert_called_once()
        _title_element_mock.assert_called_once_with('NiceTitle', 'owner')
        _title.setTextContent.assert_called_once_with('someTitle')
        _get_owner_workbook_mock.assert_called_once()
        _append_child_mock.assert_not_called()

    def test_getMarkers_refs_are_None(self):
        _element = TopicElement()

        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement'
        )

        with patch.object(_element, '_get_markerrefs') as _mock:
            _mock.return_value = None
            self.assertIsNone(_element.getMarkers())

        _mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_not_called()

        self._assert_init_methods()

    def test_getMarkers_markers_are_None(self):
        _element = TopicElement()

        _marker_fefs_element = Mock()
        _marker_fefs_element.getChildNodesByTagName.return_value = None
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_fefs_element,
            autospec=True
        )
        _refs_mock = Mock()
        _get_wb_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_wb_mock.return_value = 'OwnerWorkbook'

        _get_markerrefs_mock = patch.object(
            _element, '_get_markerrefs').start()
        _get_markerrefs_mock.return_value = _refs_mock

        self.assertListEqual([], _element.getMarkers())

        _get_markerrefs_mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_called_once_with(
            _refs_mock,
            'OwnerWorkbook')
        _get_wb_mock.assert_called_once()
        _marker_fefs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        self._assert_init_methods()

    def test_getMarkers_markers_are_not_list(self):
        _element = TopicElement()

        _marker_fefs_element = Mock()
        _marker_fefs_element.getChildNodesByTagName.return_value = 12
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_fefs_element,
            autospec=True
        )
        _refs_mock = Mock()
        _get_wb_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_wb_mock.return_value = 'OwnerWorkbook'

        _get_markerrefs_mock = patch.object(
            _element, '_get_markerrefs').start()
        _get_markerrefs_mock.return_value = _refs_mock

        with self.assertRaises(TypeError) as _ex:
            _element.getMarkers()

        _get_markerrefs_mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_called_once_with(
            _refs_mock,
            'OwnerWorkbook')
        self.assertEqual("'int' object is not iterable", _ex.exception.args[0])
        _get_wb_mock.assert_called_once()
        _marker_fefs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        self._assert_init_methods()

    def test_getMarkers(self):
        _element = TopicElement()

        _marker_fefs_element = Mock()
        _marker_fefs_element.getChildNodesByTagName.return_value = [11, 12, 13]
        _marker_refs_element_constructor_mock = patch(
            'xmind.core.topic.MarkerRefsElement').start()
        _marker_refs_element_constructor_mock.return_value = _marker_fefs_element

        _marker_ref_element_constructor_mock = patch(
            'xmind.core.topic.MarkerRefElement').start()
        _marker_ref_element_constructor_mock.side_effect = [
            111,
            112,
            113
        ]

        _refs_mock = Mock()
        _get_wb_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_wb_mock.return_value = 'OwnerWorkbook'
        _get_markerrefs_mock = patch.object(
            _element, '_get_markerrefs').start()
        _get_markerrefs_mock.return_value = _refs_mock

        self.assertListEqual(
            [111, 112, 113], _element.getMarkers())

        _get_markerrefs_mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_called_once_with(
            _refs_mock,
            'OwnerWorkbook')
        self.assertEqual(3, _marker_ref_element_constructor_mock.call_count)
        self.assertListEqual([
            call(11, 'OwnerWorkbook'),
            call(12, 'OwnerWorkbook'),
            call(13, 'OwnerWorkbook')], _marker_ref_element_constructor_mock.call_args_list)
        self.assertEqual(4, _get_wb_mock.call_count)
        _marker_fefs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        self._assert_init_methods()

    def test_addMarker_markerId_is_none(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()

        self.assertIsNone(_element.addMarker(None))
        _get_markerrefs.assert_not_called()
        self._assert_init_methods()

    def test_addMarker_markerId_is_str(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.side_effect = Exception('test exception')

        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement'
        )

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker('marker_test')

        self.assertTrue(_ex_mock.exception.args[0].find(
            "test exception") != -1)

        _get_markerrefs.assert_called_once()
        _marker_refs_element_constructor_mock.assert_not_called()
        _marker_id_constructor.assert_called_once_with('marker_test')
        self._assert_init_methods()

    def test_addMarker_markerId_is_object(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.side_effect = Exception('test exception')

        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement'
        )

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker(Mock())

        self.assertTrue(_ex_mock.exception.args[0].find(
            "test exception") != -1)
        _get_markerrefs.assert_called_once()
        _marker_refs_element_constructor_mock.assert_not_called()
        _marker_id_constructor.assert_not_called()
        self._assert_init_methods()

    def test_addMarker_markerrefs_are_none(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = None

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.side_effect = Exception(
            'test exception')
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker('marker_test')

        self.assertTrue(_ex_mock.exception.args[0].find(
            "test exception") != -1)
        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        _get_owner_workbook_mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_called_once_with(
            None, 'ownerWorkbook')
        _append_child_mock.assert_called_once_with(_marker_refs_element)
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)

        self._assert_init_methods()

    def test_addMarker_markerrefs_are_object(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = 'refs_value'

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.side_effect = Exception(
            'test exception')
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker('marker_test')

        self.assertTrue(_ex_mock.exception.args[0].find(
            "test exception") != -1)
        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        _get_owner_workbook_mock.assert_called_once()
        _marker_refs_element_constructor_mock.assert_called_once_with(
            'refs_value', 'ownerWorkbook')
        _append_child_mock.assert_not_called()
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)

        self._assert_init_methods()

    def test_addMarker_markers_are_none(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = 'refs_value'

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.return_value = None
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )
        _marker_ref_element = Mock()
        _marker_ref_element.setMarkerId.side_effect = Exception(
            'test exception')
        _marker_ref_element.appendChild.side_effect = Exception
        _marker_ref_element_constructor_mock = self._init_patch_with_name(
            '_marker_ref_element_constructor_mock',
            'xmind.core.topic.MarkerRefElement',
            return_value=_marker_ref_element
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker('marker_test')

        self.assertTrue(_ex_mock.exception.args[0].find(
            "test exception") != -1)
        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        self.assertEqual(2, _get_owner_workbook_mock.call_count)
        _marker_refs_element_constructor_mock.assert_called_once_with(
            'refs_value', 'ownerWorkbook')
        _append_child_mock.assert_not_called()
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        _marker_ref_element_constructor_mock.assert_called_once_with(
            None, 'ownerWorkbook')
        _marker_ref_element.setMarkerId.assert_called_once_with(
            'new_marker_id')
        _marker_ref_element.appendChild.assert_not_called()

        self._assert_init_methods()

    def test_addMarker_markers_are_not_list(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = 'refs_value'

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.return_value = 12
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value='new_marker_id'
        )
        _marker_ref_element = Mock()
        _marker_ref_element.setMarkerId.side_effect = Exception("exception1")
        _marker_ref_element.appendChild.side_effect = Exception("exception2")
        _marker_ref_element_constructor_mock = self._init_patch_with_name(
            '_marker_ref_element_constructor_mock',
            'xmind.core.topic.MarkerRefElement',
            return_value=_marker_ref_element
        )

        with self.assertRaises(Exception) as _ex_mock:
            _element.addMarker('marker_test')

        self.assertTrue(_ex_mock.exception.args[0].find(
            "'int' object is not iterable") != -1, _ex_mock.exception.args[0])
        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        self.assertEqual(1, _get_owner_workbook_mock.call_count)
        _marker_refs_element_constructor_mock.assert_called_once_with(
            'refs_value', 'ownerWorkbook')
        _append_child_mock.assert_not_called()
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        _marker_ref_element_constructor_mock.assert_not_called()
        _marker_ref_element.setMarkerId.assert_not_called()
        _marker_ref_element.appendChild.assert_not_called()

        self._assert_init_methods()

    def test_addMarker_mre_family_equals_to_markerid(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = 'refs_value'

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.return_value = ['m1', 'm2']
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_element = Mock()
        _marker_id_element.getFamilly.return_value = 15

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value=_marker_id_element
        )
        _marker_ref_element = Mock()
        _marker_ref_element.setMarkerId.side_effect = Exception
        _marker_ref_element.appendChild.side_effect = Exception
        _marker_ref_element_constructor_mock = patch(
            'xmind.core.topic.MarkerRefElement'
        ).start()

        _marker_with_family = Mock()
        _marker_with_family.getFamilly.side_effect = [5, 15]

        _element_not_equal = Mock()
        _element_not_equal.getMarkerId.return_value = _marker_with_family
        _element_equal = Mock()
        _element_equal.getMarkerId.return_value = _marker_with_family
        _element_equal.setMarkerId.return_value = None

        _marker_ref_element_constructor_mock.side_effect = [
            _element_not_equal,
            _element_equal
        ]

        self.assertEqual(_element_equal, _element.addMarker('marker_test'))

        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        self.assertEqual(3, _get_owner_workbook_mock.call_count)
        _marker_refs_element_constructor_mock.assert_called_once_with(
            'refs_value', 'ownerWorkbook')
        _append_child_mock.assert_not_called()
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        self.assertEqual(2, _marker_ref_element_constructor_mock.call_count)
        self.assertListEqual(
            [call('m1', 'ownerWorkbook'), call('m2', 'ownerWorkbook')],
            _marker_ref_element_constructor_mock.call_args_list
        )
        _marker_ref_element.setMarkerId.assert_not_called()
        _marker_ref_element.appendChild.assert_not_called()
        self.assertEqual(2, _marker_id_element.getFamilly.call_count)
        self.assertEqual(2, _marker_with_family.getFamilly.call_count)
        _element_equal.setMarkerId.assert_called_once_with(_marker_id_element)

        self._assert_init_methods()

    def test_addMarker_mre_family_does_not_equal_to_markerid(self):
        _element = TopicElement()

        _get_markerrefs = patch.object(_element, '_get_markerrefs').start()
        _get_markerrefs.return_value = 'refs_value'

        _marker_refs_element = Mock()
        _marker_refs_element.getChildNodesByTagName.return_value = ['m1', 'm2']
        _marker_refs_element_constructor_mock = self._init_patch_with_name(
            '_marker_refs_element_constructor_mock',
            'xmind.core.topic.MarkerRefsElement',
            return_value=_marker_refs_element
        )
        _get_owner_workbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _marker_id_element = Mock()
        _marker_id_element.getFamilly.return_value = 15

        _marker_id_constructor = self._init_patch_with_name(
            '_marker_id_constructor',
            'xmind.core.topic.MarkerId',
            return_value=_marker_id_element
        )
        _marker_ref_element = Mock()
        _marker_ref_element_constructor_mock = patch(
            'xmind.core.topic.MarkerRefElement'
        ).start()

        _marker_with_family = Mock()
        _marker_with_family.getFamilly.side_effect = [5, 6]

        _element_not_equal = Mock()
        _element_not_equal.getMarkerId.return_value = _marker_with_family

        _marker_ref_element_constructor_mock.side_effect = [
            _element_not_equal,
            _element_not_equal,
            _marker_ref_element
        ]

        self.assertEqual(_marker_ref_element,
                         _element.addMarker('marker_test'))

        _marker_id_constructor.assert_called_once_with('marker_test')
        _get_markerrefs.assert_called_once()
        self.assertEqual(4, _get_owner_workbook_mock.call_count)
        _marker_refs_element_constructor_mock.assert_called_once_with(
            'refs_value', 'ownerWorkbook')
        _append_child_mock.assert_not_called()
        _marker_refs_element.getChildNodesByTagName.assert_called_once_with(
            TAG_MARKERREF)
        self.assertEqual(3, _marker_ref_element_constructor_mock.call_count)
        self.assertListEqual(
            [
                call('m1', 'ownerWorkbook'),
                call('m2', 'ownerWorkbook'),
                call(None, 'ownerWorkbook')
            ],
            _marker_ref_element_constructor_mock.call_args_list
        )
        _marker_ref_element.setMarkerId.assert_called_once_with(
            _marker_id_element)
        _marker_refs_element.appendChild.assert_called_once_with(
            _marker_ref_element)
        self.assertEqual(2, _marker_id_element.getFamilly.call_count)
        self.assertEqual(2, _marker_with_family.getFamilly.call_count)

        self._assert_init_methods()

    def test_setFolded(self):
        _element = TopicElement()

        with patch.object(_element, 'setAttribute') as _mock:
            self.assertIsNone(_element.setFolded())

        _mock.assert_called_once_with(ATTR_BRANCH, VAL_FOLDED)
        self._assert_init_methods()

    def test_getPosition_position_is_none(self):
        _element = TopicElement()
        _position_element_construction_mock = self._init_patch_with_name(
            '_position_element',
            'xmind.core.topic.PositionElement',
            thrown_exception=Exception,
            autospec=True)

        with patch.object(_element, '_get_position') as _mock:
            _mock.return_value = None
            self.assertIsNone(_element.getPosition())

        _mock.assert_called_once()
        _position_element_construction_mock.assert_not_called()

        self._assert_init_methods()

    def test_getPosition_x_is_none_and_y_is_none(self):
        # import ipdb; ipdb.set_trace()
        _element = TopicElement()
        _position_element_mock = Mock()
        _position_element_mock.getX.return_value = None
        _position_element_mock.getY.return_value = None
        _position_element_construction_mock = self._init_patch_with_name(
            '_position_element',
            'xmind.core.topic.PositionElement',
            return_value=_position_element_mock,
            autospec=True)

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = 'position'

        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertIsNone(_element.getPosition())

        _get_owner_workbook_mock.assert_called_once()
        _get_position_mock.assert_called_once()
        _position_element_construction_mock.assert_called_once_with(
            'position', 
            'ownerWorkbook'
        )
        _position_element_mock.getX.assert_called_once()
        _position_element_mock.getY.assert_called_once()

        self._assert_init_methods()

    def test_getPosition_position_x_is_none(self):
        _element = TopicElement()
        _position_element_mock = Mock()
        _position_element_mock.getX.return_value = None
        _position_element_mock.getY.return_value = 5
        _position_element_construction_mock = self._init_patch_with_name(
            '_position_element',
            'xmind.core.topic.PositionElement',
            return_value=_position_element_mock,
            autospec=True)

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = 'position'

        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertEqual((0, 5), _element.getPosition())

        _get_owner_workbook_mock.assert_called_once()
        _get_position_mock.assert_called_once()
        _position_element_construction_mock.assert_called_once_with(
            'position', 
            'ownerWorkbook'
        )
        _position_element_mock.getX.assert_called_once()
        _position_element_mock.getY.assert_called_once()

        self._assert_init_methods()
    
    def test_setPosition_position_is_none(self):
        _element = TopicElement()
        _position_element_mock = Mock()
        _position_element_mock.setX.return_value = None
        _position_element_mock.setY.return_value = None
        _position_element_construction_mock = self._init_patch_with_name(
            '_position_element',
            'xmind.core.topic.PositionElement',
            return_value=_position_element_mock,
            autospec=True)
        
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = None

        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertIsNone(_element.setPosition(0, 6))

        _get_owner_workbook_mock.assert_called_once()
        _get_position_mock.assert_called_once()
        _position_element_construction_mock.assert_called_once_with(
            ownerWorkbook='ownerWorkbook'
        )
        _append_child_mock.assert_called_once_with(_position_element_mock)
        _position_element_mock.setX.assert_called_once_with(0)
        _position_element_mock.setY.assert_called_once_with(6)

        self._assert_init_methods()
    
    def test_setPosition_position_is_not_none(self):
        _element = TopicElement()
        _position_element_mock = Mock()
        _position_element_mock.setX.return_value = None
        _position_element_mock.setY.return_value = None
        _position_element_construction_mock = self._init_patch_with_name(
            '_position_element',
            'xmind.core.topic.PositionElement',
            return_value=_position_element_mock,
            autospec=True)
        
        _append_child_mock = patch.object(_element, 'appendChild').start()

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = 'newPosition'

        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertIsNone(_element.setPosition(0, 6))

        _get_owner_workbook_mock.assert_called_once()
        _get_position_mock.assert_called_once()
        _position_element_construction_mock.assert_called_once_with(
            'newPosition',
            'ownerWorkbook'
        )
        _append_child_mock.assert_not_called()
        _position_element_mock.setX.assert_called_once_with(0)
        _position_element_mock.setY.assert_called_once_with(6)

        self._assert_init_methods()

    def test_removePosition_position_is_none(self):
        _element = TopicElement()
        _impl_mock = Mock()
        _impl_mock.removeChild.side_effect = Exception

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = None

        _get_impl_mock = patch.object(_element, 'getImplementation').start()
        _get_impl_mock.return_value = _impl_mock
        self.assertIsNone(_element.removePosition())
        _get_position_mock.assert_called_once()
        _get_impl_mock.assert_not_called()
        _impl_mock.removeChild.assert_not_called()
        self._assert_init_methods()
    
    def test_removePosition_position_is_not_none(self):
        _element = TopicElement()
        _impl_mock = Mock()

        _get_position_mock = patch.object(_element, '_get_position').start()
        _get_position_mock.return_value = 'newPosition'

        _get_impl_mock = patch.object(_element, 'getImplementation').start()
        _get_impl_mock.return_value = _impl_mock
        self.assertIsNone(_element.removePosition())
        _get_position_mock.assert_called_once()
        _get_impl_mock.assert_called_once()
        _impl_mock.removeChild.assert_called_once_with('newPosition')
        self._assert_init_methods()
    
    def test_getType_parent_is_none(self):
        _element = TopicElement()
        _topics_element_constructor_mock = self._init_patch_with_name(
            '_topics_element_contructor',
            'xmind.core.topic.TopicsElement',
            thrown_exception=Exception
        )

        with patch.object(_element, 'getParentNode') as _mock:
            _mock.return_value = None
            self.assertIsNone(_element.getType())
        
        _mock.assert_called_once()
        _topics_element_constructor_mock.assert_not_called()

        self._assert_init_methods()
    
    def test_getType_parent_tagName_is_tag_sheet(self):
        _element = TopicElement()
        _topics_element_constructor_mock = self._init_patch_with_name(
            '_topics_element_contructor',
            'xmind.core.topic.TopicsElement',
            thrown_exception=Exception
        )

        _parent_mock = Mock(tagName = TAG_SHEET)

        with patch.object(_element, 'getParentNode') as _mock:
            _mock.return_value = _parent_mock
            self.assertEqual(TOPIC_ROOT, _element.getType())
        
        _mock.assert_called_once()
        _topics_element_constructor_mock.assert_not_called()

        self._assert_init_methods()
    
    def test_getType_parent_tagName_is_tag_topics(self):
        _element = TopicElement()

        _topics_mock = Mock()
        _topics_mock.getType.return_value = 'newType'

        _topics_element_constructor_mock = self._init_patch_with_name(
            '_topics_element_contructor',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_mock
        )

        _parent_mock = Mock(tagName = TAG_TOPICS)
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = _parent_mock
        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertEqual('newType', _element.getType())
        
        _getParentNode_mock.assert_called_once()
        _get_owner_workbook_mock.assert_called_once()
        _topics_element_constructor_mock.assert_called_once_with(_parent_mock, 'ownerWorkbook')
        _topics_mock.getType.assert_called_once()
        self._assert_init_methods()
    
    def test_getTopics_topic_children_is_none(self):
        _element = TopicElement()

        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = None

        _children_element_constructor_mock = self._init_patch_with_name(
            '_children_element_constructor',
            'xmind.core.topic.ChildrenElement',
            thrown_exception=Exception
        )
        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.side_effect = Exception

        self.assertIsNone(_element.getTopics('newType'))

        _get_children_mock.assert_called_once()
        _children_element_constructor_mock.assert_not_called()
        _get_owner_workbook_mock.assert_not_called()

        self._assert_init_methods()
    
    def test_getTopics_topic_children_is_not_none(self):
        _element = TopicElement()

        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = 'some_topic_children'

        _topic_children_mock = Mock()
        _topic_children_mock.getTopics.return_value = 'newTopics'

        _children_element_constructor_mock = self._init_patch_with_name(
            '_children_element_constructor',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_mock
        )
        _get_owner_workbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _get_owner_workbook_mock.return_value = 'ownerWorkbook'

        self.assertEqual('newTopics', _element.getTopics('newType'))

        _get_children_mock.assert_called_once()
        _get_owner_workbook_mock.assert_called_once()
        _children_element_constructor_mock.assert_called_once_with(
            'some_topic_children',
            'ownerWorkbook'
        )
        _topic_children_mock.getTopics.assert_called_once_with('newType')

        self._assert_init_methods()

    def test_getSubTopics_topics_are_none(self):
        _element = TopicElement()
        with patch.object(_element, 'getTopics') as _getTopics_mock:
            _getTopics_mock.return_value = None
            self.assertIsNone(_element.getSubTopics())
        _getTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()
    
    def test_getSubTopics_topics_are_not_none(self):
        _element = TopicElement()
        _topics_mock = Mock()
        _topics_mock.getSubTopics.return_value = 12
        with patch.object(_element, 'getTopics') as _getTopics_mock:
            _getTopics_mock.return_value = _topics_mock
            self.assertEqual(12, _element.getSubTopics())
        _getTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        _topics_mock.getSubTopics.assert_called_once()
        self._assert_init_methods()
    
    def test_getSubTopicByIndex_sub_topics_are_none(self):
        _element = TopicElement()

        with patch.object(_element, 'getSubTopics') as _getSubTopics_mock:
            _getSubTopics_mock.return_value = None
            self.assertIsNone(_element.getSubTopicByIndex(0))
        
        _getSubTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()
    
    def test_getSubTopicByIndex_index_less_than_zero(self):
        _element = TopicElement()

        with patch.object(_element, 'getSubTopics') as _getSubTopics_mock:
            _getSubTopics_mock.return_value = [1, 2]
            self.assertListEqual([1, 2], _element.getSubTopicByIndex(-1))
        
        _getSubTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()
    
    def test_getSubTopicByIndex_index_greater_than_list_len(self):
        _element = TopicElement()

        with patch.object(_element, 'getSubTopics') as _getSubTopics_mock:
            _getSubTopics_mock.return_value = [1, 2]
            self.assertListEqual([1, 2], _element.getSubTopicByIndex(4))
        
        _getSubTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()
    
    def test_getSubTopicByIndex_returns_sub_topic_by_index(self):
        _element = TopicElement()

        with patch.object(_element, 'getSubTopics') as _getSubTopics_mock:
            _getSubTopics_mock.return_value = [1, 2]
            self.assertEqual(1, _element.getSubTopicByIndex(0))
        
        _getSubTopics_mock.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()

    def test_addSubTopic_topic_is_none_get_children_throws(self):
        _element = TopicElement()
        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.side_effect = Exception('our exception')
        __class__mock = self._init_patch_with_name('_class_mock', 'xmind.core.topic.TopicElement.__init__')

        with self.assertRaises(Exception) as _ex:
            _element.addSubTopic()
        
        self.assertEqual("our exception", _ex.exception.args[0])

        _getOwnerWorkbook_mock.assert_called_once()
        __class__mock.assert_called_once_with(None, 'owner')
        _get_children_mock.assert_called_once()
        self._assert_init_methods()

    def test_addSubTopic_topic_is_not_none_get_children_throws(self):
        _element = TopicElement()
        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.side_effect = Exception('our exception')
        __class__mock = self._init_patch_with_name('_class_mock', 'xmind.core.topic.TopicElement.__init__')

        with self.assertRaises(Exception) as _ex:
            _element.addSubTopic('value')

        self.assertEqual("our exception", _ex.exception.args[0])

        _getOwnerWorkbook_mock.assert_called_once()
        __class__mock.assert_not_called()
        _get_children_mock.assert_called_once()
        self._assert_init_methods()

    def test_addSubTopic_get_children_returns_none_append_child_throws(self):
        _element = TopicElement()
        _topic_children_element = Mock()

        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = None
        _ChildrenElement_mock = self._init_patch_with_name(
            '_ChildrenElement_mock',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_element
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()
        _appendChild_mock.side_effect = Exception("appendChildException")
        _topic_children_element.getTopics.side_effect = Exception('getTopicsException')

        with self.assertRaises(Exception) as _ex:
            _element.addSubTopic('value')
        
        self.assertEqual('appendChildException', _ex.exception.args[0])

        _getOwnerWorkbook_mock.assert_called_once()
        _get_children_mock.assert_called_once()
        _ChildrenElement_mock.assert_called_once_with(ownerWorkbook='owner')
        _appendChild_mock.assert_called_once_with(_topic_children_element)
        _topic_children_element.getTopics.assert_not_called()
        self._assert_init_methods()

    def test_addSubTopic_get_children_returns_value_getTopics_throws(self):
        _element = TopicElement()
        _topic_children_element = Mock()

        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = 'topic_children_value'
        _ChildrenElement_mock = self._init_patch_with_name(
            '_ChildrenElement_mock',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_element
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()
        _appendChild_mock.side_effect = Exception('appendChildException')
        _topic_children_element.getTopics.side_effect = Exception('getTopicsException')

        with self.assertRaises(Exception) as _ex:
            _element.addSubTopic('value')
        
        self.assertEqual('getTopicsException', _ex.exception.args[0])

        _getOwnerWorkbook_mock.assert_called_once()
        _get_children_mock.assert_called_once()
        _ChildrenElement_mock.assert_called_once_with('topic_children_value', 'owner')
        _appendChild_mock.assert_not_called()
        _topic_children_element.getTopics.assert_called_once_with(TOPIC_ATTACHED)
        self._assert_init_methods()

    def test_addSubTopic_getTopics_returns_none_appendChild_throws(self):
        _element = TopicElement()
        _topic_children_element = Mock()
        _topic_children_element.getTopics.return_value = None
        _topic_children_element.appendChild.side_effect = Exception('appendChildExceptionTopic')

        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = 'topic_children_value'
        _ChildrenElement_mock = self._init_patch_with_name(
            '_ChildrenElement_mock',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_element
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()
        _appendChild_mock.side_effect = Exception('appendChildException')
        _topics_element = Mock()
        _TopicsElement_mock = self._init_patch_with_name(
            '_TopicsElement_mock',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_element
        )

        with self.assertRaises(Exception) as _ex:
            _element.addSubTopic('value')
        
        self.assertEqual('appendChildExceptionTopic', _ex.exception.args[0])

        _getOwnerWorkbook_mock.assert_called_once()
        _get_children_mock.assert_called_once()
        _ChildrenElement_mock.assert_called_once_with('topic_children_value', 'owner')
        _appendChild_mock.assert_not_called()
        _topic_children_element.getTopics.assert_called_once_with(TOPIC_ATTACHED)
        _TopicsElement_mock.assert_called_once_with(ownerWorkbook='owner')
        _topics_element.setAttribute.assert_called_once_with(ATTR_TYPE, TOPIC_ATTACHED)
        _topic_children_element.appendChild.assert_called_once_with(_topics_element)
        self._assert_init_methods()


    def test_addSubTopic_getTopics_returns_value_topics_appendChild_called(self):
        _element = TopicElement()
        _topics_element = Mock()
        _topics_element.getChildNodesByTagName.return_value = []
        _topic_children_element = Mock()
        _topic_children_element.getTopics.return_value = _topics_element

        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = 'topic_children_value'
        _ChildrenElement_mock = self._init_patch_with_name(
            '_ChildrenElement_mock',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_element
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()
        _appendChild_mock.side_effect = Exception
        _TopicsElement_mock = self._init_patch_with_name(
            '_TopicsElement_mock',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_element
        )

        self.assertEqual('value', _element.addSubTopic('value'))

        _getOwnerWorkbook_mock.assert_called_once()
        _get_children_mock.assert_called_once()
        _ChildrenElement_mock.assert_called_once_with('topic_children_value', 'owner')
        _appendChild_mock.assert_not_called()
        _topic_children_element.getTopics.assert_called_once_with(TOPIC_ATTACHED)
        _TopicsElement_mock.assert_not_called()
        _topics_element.setAttribute.assert_not_called()
        _topic_children_element.appendChild.assert_not_called()
        _topics_element.getChildNodesByTagName.assert_called_once_with(TAG_TOPIC)
        _topics_element.appendChild.assert_called_once_with('value')
        self._assert_init_methods()

    def test_addSubTopic_getTopics_returns_value_insertBefore_called(self):
        _element = TopicElement()
        _topics_element = Mock()
        _topics_element.getChildNodesByTagName.return_value = [311, 322]
        _topic_children_element = Mock()
        _topic_children_element.getTopics.return_value = _topics_element

        _getOwnerWorkbook_mock = patch.object(_element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'
        _get_children_mock = patch.object(_element, '_get_children').start()
        _get_children_mock.return_value = 'topic_children_value'
        _ChildrenElement_mock = self._init_patch_with_name(
            '_ChildrenElement_mock',
            'xmind.core.topic.ChildrenElement',
            return_value=_topic_children_element
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()
        _appendChild_mock.side_effect = Exception
        _TopicsElement_mock = self._init_patch_with_name(
            '_TopicsElement_mock',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_element
        )

        with patch('xmind.core.topic.TopicElement') as _TopicElement_mock:
            _TopicElement_mock.side_effect = [66, 77]
            self.assertEqual('value', _element.addSubTopic('value', 0))

        _getOwnerWorkbook_mock.assert_called_once()
        _get_children_mock.assert_called_once()
        _ChildrenElement_mock.assert_called_once_with('topic_children_value', 'owner')
        _appendChild_mock.assert_not_called()
        _topic_children_element.getTopics.assert_called_once_with(TOPIC_ATTACHED)
        _TopicsElement_mock.assert_not_called()
        _topics_element.setAttribute.assert_not_called()
        _topic_children_element.appendChild.assert_not_called()
        self.assertEqual(2, _TopicElement_mock.call_count)
        self.assertListEqual([call(311, 'owner'), call(322, 'owner')], _TopicElement_mock.call_args_list)
        _topics_element.getChildNodesByTagName.assert_called_once_with(TAG_TOPIC)
        _topics_element.appendChild.assert_not_called()
        _topics_element.insertBefore.assert_called_once_with('value', 66)
        self._assert_init_methods()

    def test_getIndex_parent_is_none(self):
        _element = TopicElement()
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = None

        self.assertEqual(-1, _element.getIndex())
        _getParentNode_mock.assert_called_once()
        self._assert_init_methods()

    def test_getIndex_parent_tagName_is_not_topic(self):
        _element = TopicElement()
        _tagName_mock = PropertyMock(return_value=TAG_CHILDREN)
        _parent = Mock()
        type(_parent).tagName = _tagName_mock
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = _parent

        self.assertEqual(-1, _element.getIndex())
        _getParentNode_mock.assert_called_once()
        _tagName_mock.assert_called_once()
        self._assert_init_methods()

    def test_getIndex_parent_childNodes_is_empty_list(self):
        _element = TopicElement()
        _tagName_mock = PropertyMock(return_value=TAG_TOPICS)
        _childNodes_mock = PropertyMock(return_value=[])
        _parent = Mock()
        type(_parent).tagName = _tagName_mock
        type(_parent).childNodes = _childNodes_mock
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = _parent

        self.assertEqual(-1, _element.getIndex())
        _getParentNode_mock.assert_called_once()
        _tagName_mock.assert_called_once()
        _childNodes_mock.assert_called_once()
        self._assert_init_methods()

    def test_getIndex_none_of_childs_in_childNodes_equals_by_implementation(self):
        _element = TopicElement()
        _tagName_mock = PropertyMock(return_value=TAG_TOPICS)
        _childNodes_mock = PropertyMock(return_value=['a', 'b', 'c'])
        _parent = Mock()
        type(_parent).tagName = _tagName_mock
        type(_parent).childNodes = _childNodes_mock
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = _parent
        _getImplementation_mock = patch.object(_element, 'getImplementation').start()
        _getImplementation_mock.return_value = 'd'

        self.assertEqual(-1, _element.getIndex())
        _getParentNode_mock.assert_called_once()
        _tagName_mock.assert_called_once()
        _childNodes_mock.assert_called_once()
        self.assertEqual(3, _getImplementation_mock.call_count)
        self._assert_init_methods()

    def test_getIndex_third_child_in_childNodes_equals_by_implementation(self):
        _element = TopicElement()
        _tagName_mock = PropertyMock(return_value=TAG_TOPICS)
        _childNodes_mock = PropertyMock(return_value=['a', 'b', 'c', 'd', 'e'])
        _parent = Mock()
        type(_parent).tagName = _tagName_mock
        type(_parent).childNodes = _childNodes_mock
        _getParentNode_mock = patch.object(_element, 'getParentNode').start()
        _getParentNode_mock.return_value = _parent
        _getImplementation_mock = patch.object(_element, 'getImplementation').start()
        _getImplementation_mock.return_value = 'c'

        self.assertEqual(2, _element.getIndex())
        _getParentNode_mock.assert_called_once()
        _tagName_mock.assert_called_once()
        _childNodes_mock.assert_called_once()
        self.assertEqual(3, _getImplementation_mock.call_count)
        self._assert_init_methods()

    def test_getHyperlink(self):
        _element = TopicElement()
        with patch.object(_element, 'getAttribute') as _mock:
            _mock.return_value = 'http://go.here/'
            self.assertEqual('http://go.here/', _element.getHyperlink())
        _mock.assert_called_once_with(ATTR_HREF)
        self._assert_init_methods()

    def test_setFileHyperlink_protocol_is_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=(None, 'someContent')
        )
        _get_abs_path_mock = self._init_patch_with_name(
            '_get_abs_path_mock',
            'xmind.core.topic.utils.get_abs_path',
            return_value='/some/file/here'
        )

        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setFileHyperlink('here'))

        _split_hyperlink_mock.assert_called_once_with('here')
        _get_abs_path_mock.assert_called_once_with('here')
        _set_hyperlink_mock.assert_called_once_with('file:///some/file/here')
        self._assert_init_methods()

    def test_setFileHyperlink_protocol_is_not_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=('http://', 'someContent')
        )
        _get_abs_path_mock = self._init_patch_with_name(
            '_get_abs_path_mock',
            'xmind.core.topic.utils.get_abs_path',
            return_value='/some/file/here'
        )

        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setFileHyperlink('http://here'))

        _split_hyperlink_mock.assert_called_once_with('http://here')
        _get_abs_path_mock.assert_not_called()
        _set_hyperlink_mock.assert_called_once_with('http://here')
        self._assert_init_methods()

    def test_setTopicHyperlink_protocol_is_not_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=('http://', 'someContent')
        )
        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setTopicHyperlink('http://here'))

        _split_hyperlink_mock.assert_called_once_with('http://here')
        _set_hyperlink_mock.assert_called_once_with('http://here')
        self._assert_init_methods()

    def test_setTopicHyperlink_protocol_is_none_tid_starts_with_sharp(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=(None, 'someContent')
        )
        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setTopicHyperlink('#TheBest'))

        _split_hyperlink_mock.assert_called_once_with('#TheBest')
        _set_hyperlink_mock.assert_called_once_with('xmind:#TheBest')
        self._assert_init_methods()

    def test_setTopicHyperlink_protocol_is_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=(None, 'someContent')
        )
        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setTopicHyperlink('TheBest'))

        _split_hyperlink_mock.assert_called_once_with('TheBest')
        _set_hyperlink_mock.assert_called_once_with('xmind:#TheBest')
        self._assert_init_methods()

    def test_setURLHyperlink_protocol_is_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=(None, 'TheBest')
        )
        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setURLHyperlink('TheBest'))

        _split_hyperlink_mock.assert_called_once_with('TheBest')
        _set_hyperlink_mock.assert_called_once_with('http://TheBest')
        self._assert_init_methods()

    def test_setURLHyperlink_protocol_is_not_none(self):
        _element = TopicElement()
        _split_hyperlink_mock = self._init_patch_with_name(
            '_split_hyperlink_mock',
            'xmind.core.topic.split_hyperlink',
            return_value=('someProtocol://', 'TheBest')
        )
        _set_hyperlink_mock = patch.object(_element, '_set_hyperlink').start()

        self.assertIsNone(_element.setURLHyperlink('someProtocol://TheBest'))

        _split_hyperlink_mock.assert_called_once_with('someProtocol://TheBest')
        _set_hyperlink_mock.assert_called_once_with('someProtocol://TheBest')
        self._assert_init_methods()

    def test_getNotes_notes_are_none(self):
        _element = TopicElement()
        _NotesElement_mock = self._init_patch_with_name(
            '_NotesElement_mock',
            'xmind.core.topic.NotesElement',
            return_value='notes'
        )
        _getFirstChildNodeByTagName_mock = patch.object(_element, 'getFirstChildNodeByTagName').start()
        _getFirstChildNodeByTagName_mock.return_value = None

        self.assertIsNone(_element.getNotes())

        _NotesElement_mock.assert_not_called()
        _getFirstChildNodeByTagName_mock.assert_called_once_with(TAG_NOTES)
        self._assert_init_methods()

    def test_getNotes_notes_are_not_none(self):
        _element = TopicElement()
        _NotesElement_mock = self._init_patch_with_name(
            '_NotesElement_mock',
            'xmind.core.topic.NotesElement',
            return_value='notes'
        )
        _getFirstChildNodeByTagName_mock = patch.object(_element, 'getFirstChildNodeByTagName').start()
        _getFirstChildNodeByTagName_mock.return_value = 'someNotes'

        self.assertEqual('notes', _element.getNotes())

        _NotesElement_mock.assert_called_once_with('someNotes', _element)
        _getFirstChildNodeByTagName_mock.assert_called_once_with(TAG_NOTES)
        self._assert_init_methods()

    def test__set_notes_notes_are_none(self):
        _element = TopicElement()
        _getNotes_mock = patch.object(_element, 'getNotes').start()
        _getNotes_mock.return_value = None

        _NotesElement_mock = self._init_patch_with_name(
            '_NotesElement_mock',
            'xmind.core.topic.NotesElement',
            return_value='notes'
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()

        self.assertEqual('notes', _element._set_notes())

        _getNotes_mock.assert_called_once()
        _NotesElement_mock.assert_called_once_with(ownerTopic=_element)
        _appendChild_mock.assert_called_once_with('notes')
        self._assert_init_methods()

    def test__set_notes_notes_are_not_none(self):
        _element = TopicElement()
        _getNotes_mock = patch.object(_element, 'getNotes').start()
        _getNotes_mock.return_value = 'someNotes'

        _NotesElement_mock = self._init_patch_with_name(
            '_NotesElement_mock',
            'xmind.core.topic.NotesElement',
            return_value='notes'
        )
        _appendChild_mock = patch.object(_element, 'appendChild').start()

        self.assertEqual('someNotes', _element._set_notes())

        _getNotes_mock.assert_called_once()
        _NotesElement_mock.assert_not_called()
        _appendChild_mock.assert_not_called()
        self._assert_init_methods()

    def test_setPlainNotes_old_is_not_none(self):
        _element = TopicElement()
        _notes_elemet = Mock()
        _notes_elemet.getFirstChildNodeByTagName.return_value = 'value'
        _getImplementation_mock = Mock()
        _notes_elemet.getImplementation.return_value = _getImplementation_mock

        _set_notes_mock = patch.object(_element, '_set_notes').start()
        _set_notes_mock.return_value = _notes_elemet

        _plain_notes_element = Mock()
        _plain_notes_element.getFormat.return_value = 'format'

        _PlainNotes_mock = self._init_patch_with_name(
            '_PlainNotes_mock',
            'xmind.core.topic.PlainNotes',
            return_value=_plain_notes_element
        )
        self.assertIsNone(_element.setPlainNotes('notesContent'))
        _set_notes_mock.assert_called_once()
        _PlainNotes_mock.assert_called_once_with('notesContent', None, _element)
        _notes_elemet.getFirstChildNodeByTagName.assert_called_once_with('format')
        _getImplementation_mock.removeChild.assert_called_once_with('value')
        _notes_elemet.appendChild.assert_called_once_with(_plain_notes_element)
        self._assert_init_methods()

    def test_setPlainNotes_old_is_none(self):
        _element = TopicElement()
        _notes_elemet = Mock()
        _notes_elemet.getFirstChildNodeByTagName.return_value = None
        _getImplementation_mock = Mock()
        _notes_elemet.getImplementation.return_value = _getImplementation_mock

        _set_notes_mock = patch.object(_element, '_set_notes').start()
        _set_notes_mock.return_value = _notes_elemet

        _plain_notes_element = Mock()
        _plain_notes_element.getFormat.return_value = 'format'

        _PlainNotes_mock = self._init_patch_with_name(
            '_PlainNotes_mock',
            'xmind.core.topic.PlainNotes',
            return_value=_plain_notes_element
        )
        self.assertIsNone(_element.setPlainNotes('notesContent'))
        _set_notes_mock.assert_called_once()
        _PlainNotes_mock.assert_called_once_with('notesContent', None, _element)
        _notes_elemet.getFirstChildNodeByTagName.assert_called_once_with('format')
        _getImplementation_mock.removeChild.assert_not_called()
        _notes_elemet.appendChild.assert_called_once_with(_plain_notes_element)
        self._assert_init_methods()

