from xmind.tests import logging_configuration as lc
from xmind.core.relationship import RelationshipElement
from xmind.core.title import TitleElement
from xmind.tests import base
from unittest.mock import patch, MagicMock, Mock, PropertyMock
from xmind.core.const import TAG_RELATIONSHIP, ATTR_ID, TAG_TITLE, TAG_TOPIC,  ATTR_END1, ATTR_END2


class TestRelationshipElement(base.Base):
    """Test class for RelationshipsElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('relationshipElement')
        return self._logger

    def setUp(self):
        super(TestRelationshipElement, self).setUp()
        self._wb_mixin_element_init = self._init_patch_with_name(
            '_wb', 'xmind.core.relationship.WorkbookMixinElement.__init__', autospec=True)
        self._add_attribute = self._init_patch_with_name(
            '_attr', 'xmind.core.relationship.RelationshipElement.addIdAttribute', autospec=True)

    def test_init(self):
        _obj1 = RelationshipElement()
        self._wb_mixin_element_init.assert_called_with(_obj1, None, None)
        self.assertEqual(_obj1.TAG_NAME, TAG_RELATIONSHIP)
        self._add_attribute.assert_called_with(_obj1, ATTR_ID)

        _obj2 = RelationshipElement(1)
        self._wb_mixin_element_init.assert_called_with(_obj2, 1, None)
        self.assertEqual(_obj2.TAG_NAME, TAG_RELATIONSHIP)
        self._add_attribute.assert_called_with(_obj2, ATTR_ID)

        _obj3 = RelationshipElement(1, 2)
        self._wb_mixin_element_init.assert_called_with(_obj3, 1, 2)
        self.assertEqual(_obj3.TAG_NAME, TAG_RELATIONSHIP)
        self._add_attribute.assert_called_with(_obj3, ATTR_ID)

        _obj4 = RelationshipElement(node=None, ownerWorkbook=1)
        self._wb_mixin_element_init.assert_called_with(_obj4, None, 1)
        self._add_attribute.assert_called_with(_obj4, ATTR_ID)
        self.assertEqual(_obj4.TAG_NAME, TAG_RELATIONSHIP)

        with self.assertRaises(TypeError) as _ex:
            RelationshipElement(1, 2, 3)

        self.assertTrue(_ex.exception.args[0].find("__init__() takes") != -1)
        # 4 because for last case we don't get to __init__ of super
        self.assertEqual(self._wb_mixin_element_init.call_count, 4)
        self.assertEqual(self._add_attribute.call_count, 4)

    def test_excessive_parameters(self):
        _relationship_element = RelationshipElement(12)

        _parameters = [
            ('_get_title', 0),
            ('_find_end_point', 1),
            ('getEnd1ID', 0),
            ('setEnd1ID', 1),
            ('getEnd2ID', 0),
            ('setEnd2ID', 1),
            ('getEnd1', 1),
            # ('getEnd2', 1),
            ('getTitle', 0),
            ('setTitle', 1),
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(
                    pair, _relationship_element)

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)

    def test_get_title(self):
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getFirstChildNodeByTagName') as _gf:
            _gf.return_value = 'Something'
            self.assertEqual('Something', _relationship_element._get_title())

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _gf.assert_called_once_with(TAG_TITLE)

    def test_find_end_point_owner_workbook_is_none(self):
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getOwnerWorkbook') as _g_wb:
            _g_wb.return_value = None
            self.assertIsNone(_relationship_element._find_end_point('1'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)

    def test_find_end_point_owner_workbook_endpoint_is_none(self):
        _wb_mock = MagicMock()
        _wb_mock.getElementById.return_value = None
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getOwnerWorkbook') as _g_wb:
            _g_wb.return_value = _wb_mock
            self.assertIsNone(_relationship_element._find_end_point('1'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _wb_mock.getElementById.assert_called_once_with('1')

    def test_find_end_point_endpoint_tag_name_is_not_topic(self):
        _wb_mock = MagicMock()
        _end_point = MagicMock()
        _tag_name = PropertyMock(return_value='bla-bla')
        type(_end_point).tagName = _tag_name
        _wb_mock.getElementById.return_value = _end_point
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getOwnerWorkbook') as _g_wb:
            _g_wb.return_value = _wb_mock
            self.assertIsNone(_relationship_element._find_end_point('1'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _wb_mock.getElementById.assert_called_once_with('1')
        _tag_name.assert_called_once()

    def test_find_end_point_endpoint_tag_name_is_topic(self):
        _wb_mock = MagicMock()
        _end_point = MagicMock()
        _tag_name = PropertyMock(return_value=TAG_TOPIC)
        type(_end_point).tagName = _tag_name
        _wb_mock.getElementById.return_value = _end_point
        _relationship_element = RelationshipElement(12)

        _new_topic_element_mock = self._init_patch_with_name(
            '_topic', 'xmind.core.relationship.TopicElement', return_value='super', autospec=True)

        with patch.object(_relationship_element, 'getOwnerWorkbook') as _g_wb:
            _g_wb.return_value = _wb_mock
            self.assertEqual(
                'super', _relationship_element._find_end_point('1'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _wb_mock.getElementById.assert_called_once_with('1')
        _tag_name.assert_called_once()
        _new_topic_element_mock.assert_called_once_with(_end_point, _wb_mock)

    def test_getEnd1ID(self):
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getAttribute') as _get_attribute:
            _get_attribute.return_value = 120
            self.assertEqual(120, _relationship_element.getEnd1ID())

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_attribute.assert_called_once_with(ATTR_END1)

    def test_setEnd1ID(self):
        _relationship_element = RelationshipElement(12)
        _set_attribute = patch.object(
            _relationship_element, 'setAttribute').start()
        _update_modified_time = patch.object(
            _relationship_element, 'updateModifiedTime').start()

        self.assertIsNone(_relationship_element.setEnd1ID(15))

        _set_attribute.assert_called_once_with(ATTR_END1, 15)
        _update_modified_time.assert_called_once()
        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)

    def test_getEnd2ID(self):
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, 'getAttribute') as _get_attribute:
            _get_attribute.return_value = 120
            self.assertEqual(120, _relationship_element.getEnd2ID())

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_attribute.assert_called_once_with(ATTR_END2)

    def test_setEnd2ID(self):
        _relationship_element = RelationshipElement(12)
        _set_attribute = patch.object(
            _relationship_element, 'setAttribute').start()
        _update_modified_time = patch.object(
            _relationship_element, 'updateModifiedTime').start()

        self.assertIsNone(_relationship_element.setEnd2ID(17))

        _set_attribute.assert_called_once_with(ATTR_END2, 17)
        _update_modified_time.assert_called_once()
        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)

    def test_getEnd1(self):
        _relationship_element = RelationshipElement(12)

        with patch.object(_relationship_element, '_find_end_point') as _find_end_point:
            _find_end_point.return_value = 120
            self.assertEqual(120, _relationship_element.getEnd1(111))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _find_end_point.assert_called_once_with(111)

    def test_getTitle_title_is_none(self):
        _relationship_element = RelationshipElement(12)
        _title_element = patch('xmind.core.relationship.TitleElement').start()

        with patch.object(_relationship_element, '_get_title') as _get_title:
            _get_title.return_value = None
            self.assertIsNone(_relationship_element.getTitle())

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_title.assert_called_once()
        _title_element.assert_not_called()

    def test_getTitle(self):
        _relationship_element = RelationshipElement(12)
        _title_mock = Mock()
        _title_mock.getTextContent.return_value = 'it works'
        _title_element = patch('xmind.core.relationship.TitleElement').start()
        _title_element.return_value = _title_mock
        _get_owner_workbook = patch.object(
            _relationship_element, 'getOwnerWorkbook').start()
        _get_owner_workbook.return_value = 'somehow'

        with patch.object(_relationship_element, '_get_title') as _get_title:
            _get_title.return_value = 'test_value'
            self.assertEqual('it works', _relationship_element.getTitle())

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_title.assert_called_once()
        _title_element.assert_called_once_with('test_value', 'somehow')
        _title_mock.getTextContent.assert_called_once()

    def test_setTitle_title_is_none(self):
        _relationship_element = RelationshipElement(12)
        _title_mock = Mock()
        _title_mock.setTextContent.return_value = 'it works'
        _title_element = patch('xmind.core.relationship.TitleElement').start()
        _title_element.return_value = _title_mock
        _get_owner_workbook = patch.object(
            _relationship_element, 'getOwnerWorkbook').start()
        _get_owner_workbook.return_value = 'somehow'
        _append_child = patch.object(
            _relationship_element, 'appendChild').start()
        _update_modified_time = patch.object(
            _relationship_element, 'updateModifiedTime').start()

        with patch.object(_relationship_element, '_get_title') as _get_title:
            _get_title.return_value = None
            self.assertIsNone(_relationship_element.setTitle('Super'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_title.assert_called_once()
        _title_element.assert_called_once_with(None, 'somehow')
        _title_mock.setTextContent.assert_called_once_with('Super')
        _append_child.assert_called_once_with(_title_mock)
        _update_modified_time.assert_called_once()

    def test_setTitle_title(self):
        _relationship_element = RelationshipElement(12)
        _title_mock = Mock()
        _title_mock.setTextContent.return_value = 'it works'
        _title_element = patch('xmind.core.relationship.TitleElement').start()
        _title_element.return_value = _title_mock
        _get_owner_workbook = patch.object(
            _relationship_element, 'getOwnerWorkbook').start()
        _get_owner_workbook.return_value = 'somehow'
        _append_child = patch.object(
            _relationship_element, 'appendChild').start()
        _update_modified_time = patch.object(
            _relationship_element, 'updateModifiedTime').start()

        with patch.object(_relationship_element, '_get_title') as _get_title:
            _get_title.return_value = 'test_value'
            self.assertIsNone(_relationship_element.setTitle('Super'))

        self._wb_mixin_element_init.assert_called_once_with(
            _relationship_element, 12, None)
        self._add_attribute.assert_called_once_with(
            _relationship_element, ATTR_ID)
        _get_title.assert_called_once()
        _title_element.assert_called_once_with('test_value', 'somehow')
        _title_mock.setTextContent.assert_called_once_with('Super')
        _append_child.assert_not_called()
        _update_modified_time.assert_called_once()
