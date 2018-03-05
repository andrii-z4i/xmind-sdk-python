from xmind.tests import logging_configuration as lc
from xmind.core.topic import TopicsElement
from xmind.tests import base
from unittest.mock import patch, Mock, PropertyMock, call
from xmind.core.const import TAG_TOPICS, ATTR_TYPE, TAG_TOPIC


class TestTopicsElement(base.Base):
    """Test class for TopicsElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('TopicsElement')
        return self._logger

    def setUp(self):
        super(TestTopicsElement, self).setUp()
        self._workbook_mixin_element_mock = self._init_patch_with_name(
            '_mixin_init',
            'xmind.core.topic.WorkbookMixinElement.__init__',
            autospec=True
        )

    def test_excessive_parameters(self):
        _element = TopicsElement()
        self.assertEqual(TAG_TOPICS, _element.TAG_NAME)

        _parameters = [
            ('getType', 0),
            ('getSubTopics', 0),
            ('getSubTopicByIndex', 1),
            ('__init__', (2, False)),
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_init(self):
        _element1 = TopicsElement(node='node1')
        _element2 = TopicsElement(ownerWorkbook='owner2')
        _element3 = TopicsElement('node3', 'owner3')
        self.assertEqual(3, self._workbook_mixin_element_mock.call_count)
        self.assertListEqual(
            [
                call(_element1, 'node1', None),
                call(_element2, None, 'owner2'),
                call(_element3, 'node3', 'owner3')
            ],
            self._workbook_mixin_element_mock.call_args_list
        )

    def test_getType(self):
        _element = TopicsElement()
        with patch.object(_element, 'getAttribute') as _mock:
            _mock.return_value = 45
            self.assertEqual(45, _element.getType())

        _mock.assert_called_once_with(ATTR_TYPE)
        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_getSubTopics_no_childs(self):
        _element = TopicsElement()
        _getOwnerWorkbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'

        _getChildNodesByTagName_mock = patch.object(
            _element, 'getChildNodesByTagName').start()
        _getChildNodesByTagName_mock.return_value = []

        _TopicElement_mock = patch('xmind.core.topic.TopicElement').start()

        self.assertListEqual([], _element.getSubTopics())

        _getOwnerWorkbook_mock.assert_called_once()
        _getChildNodesByTagName_mock.assert_called_once()
        _TopicElement_mock.assert_not_called()

        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_getSubTopics(self):
        _element = TopicsElement()
        _getOwnerWorkbook_mock = patch.object(
            _element, 'getOwnerWorkbook').start()
        _getOwnerWorkbook_mock.return_value = 'owner'

        _getChildNodesByTagName_mock = patch.object(
            _element, 'getChildNodesByTagName').start()
        _getChildNodesByTagName_mock.return_value = [11, 13, 15]

        _topic_element_list = [
            Mock(),
            Mock(),
            Mock()
        ]

        _TopicElement_mock = patch('xmind.core.topic.TopicElement').start()
        _TopicElement_mock.side_effect = _topic_element_list

        self.assertListEqual(_topic_element_list, _element.getSubTopics())

        _getOwnerWorkbook_mock.assert_called_once()
        _getChildNodesByTagName_mock.assert_called_once()
        self.assertEqual(3, _TopicElement_mock.call_count)
        self.assertListEqual(
            [
                call(11, 'owner'),
                call(13, 'owner'),
                call(15, 'owner'),
            ],
            _TopicElement_mock.call_args_list
        )

        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_getSubTopicByIndex_index_out_of_range(self):
        _element = TopicsElement()

        with patch.object(_element, 'getSubTopics') as _mock:
            _mock.return_value = [1, 2]
            self.assertEqual([1, 2], _element.getSubTopicByIndex(3))

        _mock.assert_called_once()
        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)

    def test_getSubTopicByIndex_index_in_range_of_topics(self):
        _element = TopicsElement()

        with patch.object(_element, 'getSubTopics') as _mock:
            _mock.return_value = [11, 22]
            self.assertEqual(22, _element.getSubTopicByIndex(1))

        _mock.assert_called_once()
        self._workbook_mixin_element_mock.assert_called_once_with(
            _element, None, None)
