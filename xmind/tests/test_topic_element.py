import logging
from xmind.core.topic import TopicElement
from xmind.tests import base
from unittest.mock import patch, Mock, PropertyMock, call
from xmind.core.const import (
    TAG_TOPIC,
    TAG_TITLE,
    TAG_MARKERREF,
    TAG_MARKERREFS,
    TAG_POSITION,
    TAG_CHILDREN,
    TAG_SHEET,
    ATTR_ID,
    ATTR_HREF,
)


class TestTopicElement(base.Base):
    """Test class for TopicElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = logging.getLogger('TopicElement')
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
