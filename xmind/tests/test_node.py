from xmind.tests import logging_configuration as lc
import xml
from unittest.mock import MagicMock, patch, Mock, PropertyMock, call

from xmind.core import Node, create_document, create_element
from xmind.tests import base


class TestNode(base.Base):
    """Tests for Node class from core module"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('node')
        return self._logger

    def test_excessive_parameters(self):
        _node = Node(12)
        _parameters = [
            ('getImplementation', 0),
            ('getOwnerDocument', 0),
            ('setOwnerDocument', 1),
            ('getLocalName', 1),
            ('getPrefix', 1),
            ('appendChild', 1),
            ('insertBefore', 2),
            ('getChildNodesByTagName', 1),
            ('getFirstChildNodeByTagName', 1),
            ('getParentNode', 0),
            ('_isOrphanNode', 1),
            ('isOrphanNode', 0),
            ('iterChildNodesByTagName', 1),
            ('removeChild', 1),
            ('output', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _node)

    def test_equals(self):
        """Complex test for _equals method"""
        parameters = [
            (1, 'a', False),
            (1, None, False),
            (1, 2, False),
            (1, 1, True)
        ]
        for pair in parameters:
            with self.subTest(pair=pair):
                self.getLogger().info('Next pair %s', pair)
                _obj1 = Node(pair[0])
                _obj2 = None if not pair[1] else Node(pair[1])
                self.assertEqual(_obj1._equals(_obj2), pair[2])
        _objSelf = Node(1)
        self.assertTrue(_objSelf._equals(_objSelf))

    def test_getImplementation(self):
        """Checks if getImplementation returns self"""
        _obj = Node('check me')
        self.assertEqual(_obj.getImplementation(), 'check me')

    def test_getOwnerDocument(self):
        """Checks if getOwnerDocument throws exception"""
        _obj = Node('check me')
        with self.assertRaises(NotImplementedError) as ex:
            _obj.getOwnerDocument()
        self.assertEqual(str(ex.exception),
                         "This method requires an implementation!")

    def test_setOwnerDocument(self):
        """Checks if setOwnerDocument throws exception"""
        _obj = Node('check me')
        with self.assertRaises(NotImplementedError) as ex:
            _obj.setOwnerDocument(None)  # put here None as doc
        self.assertEqual(str(ex.exception),
                         "This method requires an implementation!")

    def test_getLocalName(self):
        """Checks getLocalName implementation"""
        parameters = [
            (':', ''),
            ('qq:', ''),
            ('qq:1', '1'),
            ('', ''),
            ('fake', 'fake')
        ]

        for pair in parameters:
            with self.subTest(pair=pair):
                self.getLogger().info('Next pair %s', pair)
                _obj = Node(pair[0])
                self.assertEqual(_obj.getLocalName(pair[0]), pair[1])

    def test_getPrefix(self):
        """Checks getPrefix implementation"""
        parameters = [
            (':', ':'),
            ('qq:', 'qq:'),
            ('qq:1', 'qq:'),
            ('', None),
            ('fake', None)
        ]

        for pair in parameters:
            with self.subTest(pair=pair):
                self.getLogger().info('Next pair %s', pair)
                _obj = Node(0)
                self.assertEqual(_obj.getPrefix(pair[0]), pair[1])

    def test_appendChild(self):
        """Tests appendChild method"""
        _mock_object = MagicMock()
        _object_to_append = MagicMock()
        _get_implementation = Mock()
        _object_to_append.getImplementation.return_value = _get_implementation

        _get_owner_document_mock = Mock()

        with patch('xmind.core.Node.getOwnerDocument') as getOwnerDocumentMock:
            getOwnerDocumentMock.return_value = _get_owner_document_mock
            _test_object = Node(_mock_object)
            _test_object.appendChild(_object_to_append)

        getOwnerDocumentMock.assert_called()
        _mock_object.appendChild.assert_called_once_with(_get_implementation)
        _object_to_append.setOwnerDocument.assert_called_once_with(
            _get_owner_document_mock)
        _object_to_append.getImplementation.assert_called_once()

    def test_insertBefore(self):
        """Tests insertBefore method"""
        _mock_object = MagicMock()
        _new_node_object = MagicMock()
        _ref_node_object = MagicMock()
        _get_implementation = Mock()
        _new_node_object.getImplementation.return_value = _get_implementation
        _ref_node_object.getImplementation.return_value = _get_implementation

        _get_owner_document_mock = Mock()

        with patch('xmind.core.Node.getOwnerDocument') as getOwnerDocumentMock:
            getOwnerDocumentMock.return_value = _get_owner_document_mock
            _test_object = Node(_mock_object)
            _test_object.insertBefore(_new_node_object, _ref_node_object)

        getOwnerDocumentMock.assert_called()
        _mock_object.insertBefore.assert_called_once_with(
            _get_implementation, _get_implementation)
        _new_node_object.setOwnerDocument.assert_called_once_with(
            _get_owner_document_mock)
        _new_node_object.getImplementation.assert_called_once()
        _ref_node_object.getImplementation.assert_called_once()

    def test_getChildNodesByTagName(self):
        """Tests getChildNodesByTagName"""
        _node = MagicMock()
        _node.childNodes = self._createNodeList([
            (1, 'abba'),
            (2, 'trara'),
            (3, 'child'),
            (4, 'child'),
            (3, 'child3')
        ])
        _test_object = Node(_node)
        values = _test_object.getChildNodesByTagName('child')
        self.assertListEqual(values, [_node.childNodes[3]])

    def test_getFirstChildNodeByTagName(self):
        """Tests getFirstChildNodeByTagName method"""
        _testParameters = [
            ([(1, 'abba'), (2, 'trara'), (3, 'child'), (4, 'child'), (3, 'child3')], 3),
            ([(1, 'abba'), (2, 'trara'), (4, 'child'), (4, 'child'), (3, 'child3')], 2),
            ([(1, 'abba'), (2, 'trara'), (3, 'child'),
              (4, 'child4'), (3, 'child3')], None),
        ]

        for parameter in _testParameters:
            with self.subTest(parameter=parameter):
                _node = MagicMock()
                _node.childNodes = self._createNodeList(parameter[0])
                _test_object = Node(_node)
                value = _test_object.getFirstChildNodeByTagName('child')
                if parameter[1]:
                    self.assertEqual(value, _node.childNodes[parameter[1]])
                else:
                    self.assertEqual(value, None)

    def test_getParentNode(self):
        """Tests getParentNode method"""
        _node = MagicMock()
        _node.parentNode = Mock()
        _test_object = Node(_node)
        _parentNode = _test_object.getParentNode()
        self.assertEqual(_node.parentNode, _parentNode)

    def test_isOrphanNode_None(self):
        """Tests _isOrphanNode method"""
        _node = Node(None)
        _result = _node._isOrphanNode(None)
        self.assertTrue(_result)

    def test_isOrphanNode_Document_Node(self):
        """Tests _isOrphanNode method"""
        _node = Node(None)
        _node_to_check = self._createNode(9, 'something')
        _result = _node._isOrphanNode(_node_to_check)
        self.assertFalse(_result)

    def test_isOrphanNode_check_parent(self):
        """Tests _isOrphanNode method"""
        _node = Node(None)
        _node_to_check = self._createNode(4, 'something')
        setattr(_node_to_check, 'parentNode', None)
        with patch.object(Node, '_isOrphanNode', wraps=_node._isOrphanNode) as _mock:
            _result = _node._isOrphanNode(_node_to_check)
            self.assertTrue(_result)

        self.assertListEqual(_mock.call_args_list, [
                             call(_node_to_check), call(None)])
        self.assertEqual(_mock.call_count, 2)

    def test_isOrphanNode_self(self):
        """Tests isOrphanNode method"""
        _node = Node(None)
        with patch.object(Node, '_isOrphanNode', wraps=_node._isOrphanNode) as _mock:
            _result = _node.isOrphanNode()
            self.assertTrue(_result)
        self.assertListEqual(_mock.call_args_list, [call(None)])
        self.assertEqual(_mock.call_count, 1)

    def test_iterChildNodesByTagName(self):
        """Tests iterChildNodesByTagName method (yield)"""
        _node = MagicMock()
        _node.childNodes = self._createNodeList([
            (1, 'abba'),
            (2, 'trara'),
            (4, 'child'),
            (3, 'child'),
            (4, 'child')
        ])
        _test_object = Node(_node)
        values = list(_test_object.iterChildNodesByTagName('child'))
        self.assertListEqual(
            values, [_node.childNodes[2], _node.childNodes[4]])

    def test_removeChild(self):
        """Tests removeChild method"""
        _node = MagicMock()
        _node.removeChild = MagicMock()
        _test_object = Node(_node)
        _child_node = MagicMock()
        _child_node.getImplementation.return_value = 5

        _test_object.removeChild(_child_node)
        _node.removeChild.assert_called_with(5)
        _child_node.getImplementation.assert_called_once()

    def test_output(self):
        """Tests output method"""
        _output_stream = Mock()
        _node = MagicMock()
        _node.writexml = MagicMock(return_value='Bla')
        _test_object = Node(_node)
        _return = _test_object.output(_output_stream)
        self.assertEqual(_return, 'Bla')
        _node.writexml.assert_called_with(
            _output_stream, addindent="", newl="", encoding="utf-8")

    def _createNodeList(self, listOfTuples):
        _returnNodes = []
        for item in listOfTuples:
            _returnNodes.append(self._createNode(item[0], item[1]))

        return _returnNodes

    def _createNode(self, nodeType, tagName):
        class InnerNode(xml.dom.Node):

            def __init__(self, nodeType, tagName):
                super(InnerNode, self).__init__()
                self.nodeType = nodeType
                self.tagName = tagName

            def __eq__(self, other):
                return self.nodeType == other.nodeType and self.tagName == other.tagName

        return InnerNode(nodeType, tagName)

    def test_global_create_document(self):
        _dom_document_mock = self._init_patch_with_name(
            '_dom_document_mock',
            'xmind.core.DOM.Document',
            return_value='new_document'
        )
        self.assertEqual('new_document', create_document())
        _dom_document_mock.assert_called_once_with()

    def test_global_create_element_complex(self):

        with patch('xmind.core.DOM.Element') as _dom_element_mock:
            _dom_element_mock.side_effect = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g'
            ]
            self.assertEqual('a', create_element('tag_a'))
            self.assertEqual('b', create_element('tag_b', 'uri'))
            self.assertEqual('c', create_element('tag_c', None, 'prefix'))
            self.assertEqual('d', create_element(
                'tag_d', None, None, 'localName'))
            self.assertEqual('e', create_element(
                'tag_e', localName='localName2'))
            self.assertEqual('f', create_element('tag_f', prefix='prefix2'))
            self.assertEqual('g', create_element('tag_g', namespaceURI='uri2'))

        self.assertEqual(7, _dom_element_mock.call_count)
        self.assertListEqual(
            [
                call('tag_a', None, None, None),
                call('tag_b', 'uri', None, None),
                call('tag_c', None, 'prefix', None),
                call('tag_d', None, None, 'localName'),
                call('tag_e', None, None, 'localName2'),
                call('tag_f', None, 'prefix2', None),
                call('tag_g', 'uri2', None, None),

            ],
            _dom_element_mock.call_args_list
        )
