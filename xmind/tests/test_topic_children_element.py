from xmind.tests import logging_configuration as lc
from xmind.core.topic import ChildrenElement, split_hyperlink
from xmind.tests import base
from unittest.mock import patch, Mock, PropertyMock, call
from xmind.core.const import TAG_CHILDREN, TAG_TOPICS


class TestChildrenElement(base.Base):
    """Test class for ChildrenElement class"""

    def setUp(self):
        super(TestChildrenElement, self).setUp()
        self._workbook_mixin_element_mock = self._init_patch_with_name(
            '_wb_mixin_mock',
            'xmind.core.topic.WorkbookMixinElement.__init__',
            autospec=True
        )

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('ChildrenElement')
        return self._logger

    def test_excessive_parameters(self):
        _element = ChildrenElement()

        _parameters = [
            ('getTopics', 1),
            ('__init__', (2, False))
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

        self.assertEqual(TAG_CHILDREN, _element.TAG_NAME)
        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_init(self):
        _element1 = ChildrenElement(node='a1')
        _element2 = ChildrenElement(ownerWorkbook='b2')
        _element3 = ChildrenElement(node='a3', ownerWorkbook='b3')
        self.assertEqual(3, self._workbook_mixin_element_mock.call_count)
        self.assertListEqual(
            [
                call(_element1, 'a1', None),
                call(_element2, None, 'b2'),
                call(_element3, 'a3', 'b3')
            ],
            self._workbook_mixin_element_mock.call_args_list
        )
        self.assertEqual(TAG_CHILDREN, _element1.TAG_NAME)
        self.assertEqual(TAG_CHILDREN, _element2.TAG_NAME)
        self.assertEqual(TAG_CHILDREN, _element3.TAG_NAME)

    def test_getTopics_no_topics(self):
        _element = ChildrenElement()
        _iterChildNodesByTagName_mock = patch.object(
            _element, 'iterChildNodesByTagName').start()
        _iterChildNodesByTagName_mock.return_value = []

        self.assertIsNone(_element.getTopics(1))

        _iterChildNodesByTagName_mock.assert_called_once_with(TAG_TOPICS)
        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)
        self.assertEqual(TAG_CHILDREN, _element.TAG_NAME)

    def test_getTopics_topics_type_differs(self):
        _element = ChildrenElement()
        _iterChildNodesByTagName_mock = patch.object(
            _element, 'iterChildNodesByTagName').start()
        _iterChildNodesByTagName_mock.return_value = [1, 2, 3]

        _topics_element_list = [
            Mock(**{'getType.return_value': 2}),
            Mock(**{'getType.return_value': 2}),
            Mock(**{'getType.return_value': 2}),
        ]
        _TopicsElement_mock = self._init_patch_with_name(
            '_TopicsElement_mock',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_element_list,
            return_value_as_side_effect=True
        )

        _getOwnerWorkbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'

        self.assertIsNone(_element.getTopics(1))

        _iterChildNodesByTagName_mock.assert_called_once_with(TAG_TOPICS)
        self.assertEqual(3, _getOwnerWorkbook_mock.call_count)
        self.assertEqual(3, _TopicsElement_mock.call_count)
        self.assertListEqual(
            [
                call(1, 'owner'),
                call(2, 'owner'),
                call(3, 'owner')
            ],
            _TopicsElement_mock.call_args_list
        )
        for _mock in _topics_element_list:
            _mock.getType.assert_called_once_with()

        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_getTopics(self):
        _element = ChildrenElement()
        _iterChildNodesByTagName_mock = patch.object(
            _element, 'iterChildNodesByTagName').start()
        _iterChildNodesByTagName_mock.return_value = [1, 2, 3]

        _topics_element_list = [
            Mock(**{'getType.return_value': 2}),
            Mock(**{'getType.return_value': 1}),
            Mock(**{'getType.return_value': 2}),
        ]
        _TopicsElement_mock = self._init_patch_with_name(
            '_TopicsElement_mock',
            'xmind.core.topic.TopicsElement',
            return_value=_topics_element_list,
            return_value_as_side_effect=True
        )

        _getOwnerWorkbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'

        self.assertEqual(_topics_element_list[1], _element.getTopics(1))

        _iterChildNodesByTagName_mock.assert_called_once_with(TAG_TOPICS)
        self.assertEqual(2, _getOwnerWorkbook_mock.call_count)
        self.assertEqual(2, _TopicsElement_mock.call_count)
        self.assertListEqual(
            [
                call(1, 'owner'),
                call(2, 'owner')
            ],
            _TopicsElement_mock.call_args_list
        )

        _topics_element_list[0].getType.assert_called_once_with()
        _topics_element_list[1].getType.assert_called_once_with()
        _topics_element_list[2].getType.assert_not_called()

        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_global_split_hyperlink_colon_not_found(self):
        (protocol, hyperlink) = split_hyperlink('some.link')
        self.assertIsNone(protocol)
        self.assertEqual('some.link', hyperlink)

    def test_global_split_hyperlink_colon_found(self):
        (protocol, hyperlink) = split_hyperlink('http:some.link')
        self.assertEqual('http', protocol)
        self.assertEqual('some.link', hyperlink)

    def test_global_split_hyperlink_starts_with_slash(self):
        (protocol, hyperlink) = split_hyperlink('//some.link')
        self.assertIsNone(protocol)
        self.assertEqual('some.link', hyperlink)

    def test_global_split_hyperlink(self):
        (protocol, hyperlink) = split_hyperlink('http://some.link/url')
        self.assertEqual('http', protocol)
        self.assertEqual('some.link/url', hyperlink)
