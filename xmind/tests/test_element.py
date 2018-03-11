from xmind.tests import logging_configuration as lc
from xmind.core import Element
from xmind.tests import base
from unittest.mock import patch, MagicMock, call, PropertyMock


class InnerElement(object):
    prefix = ''
    localName = ''


class InnerNode(object):
    nodeType = 0
    data = ''

    def __init__(self, nodeType, data):
        self.nodeType = nodeType
        self.data = data


class TestElement(base.Base):
    """Tests for Element class from __init__"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('element')
        return self._logger

    def test_excessive_parameters(self):
        _element = Element(12)
        _parameters = [
            ('getOwnerDocument', 0),
            ('setOwnerDocument', 1),
            ('getOwnerDocument', 0),
            ('setOwnerDocument', 1),
            ('setAttributeNS', 2),
            ('getAttribute', 1),
            ('setAttribute', 2),
            ('createElement', 1),
            ('addIdAttribute', 1),
            ('getIndex', 0),
            ('getTextContent', 0),
            ('setTextContent', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_init_with_node(self):
        """Tests __init__ method with node parameter"""
        _element_constructor = self._init_patch_with_name(
            '_el_constructor', 'xmind.core.Element._elementConstructor', autospec=None)
        _element = Element(1)
        _element_constructor.assert_not_called()
        self.assertEqual(_element._node, 1)

    def test_init_without_node(self):
        """Tests __init__ method without node parameter"""
        _element_constructor = self._init_patch_with_name(
            '_el_constructor', 'xmind.core.Element._elementConstructor', return_value=12, autospec=None)
        _element = Element()
        _element_constructor.assert_called_once_with("")
        self.assertEqual(_element._node, 12)

    def test_init_more_parameters(self):
        """Tests __init__ method with more parameters, extects exception"""
        _element_constructor = self._init_patch_with_name(
            '_el_constructor', 'xmind.core.Element._elementConstructor', return_value=12, autospec=None)
        with self.assertRaises(Exception):
            Element(1, 2)
        _element_constructor.assert_not_called()

    def test_elementConstructor(self):
        """Tests _elementConstructor method"""
        _inner_element = InnerElement()
        _dom_element = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Element', return_value=_inner_element, autospec=True)
        _element_get_prefix = self._init_patch_with_name(
            '_get_prefix', 'xmind.core.Element.getPrefix', return_value='aaa', autospec=True)
        _element_get_local_name = self._init_patch_with_name(
            '_get_local_name', 'xmind.core.Element.getLocalName', return_value='local', autospec=True)
        _element = Element(1)
        _created_element = _element._elementConstructor('a')
        self.assertEqual(_created_element, _inner_element)
        self.assertEqual(_inner_element.prefix, 'aaa')
        _dom_element.assert_called_once_with('a', None, None, 'local')
        _element_get_prefix.assert_called_once_with(_element, 'a')
        _element_get_local_name.assert_called_once_with(_element, 'a')

    def test_getOwnerDocument(self):
        """Tests getOwnerDocument method"""
        _node = MagicMock(ownerDocument='me')
        _element = Element(_node)
        self.assertEqual(_element.getOwnerDocument(), 'me')

    def test_setOwnerDocument(self):
        """Tests setOwnerDocument method"""
        _node = MagicMock(ownerDocument='me')
        _element = Element(_node)
        _element.setOwnerDocument('you')
        self.assertEqual(_node.ownerDocument, 'you')

    def test_setAttributeNS_has_attribute_and_attributeNs(self):
        """Tests setAttributeNS method (no attributeNS, no attribute)"""
        _node = MagicMock()
        _node.hasAttribute.return_value = True
        _node.hasAttributeNS.return_value = True
        _namespace = ('a', 'a1')
        _attr = ('b', 'local', '12')
        _element = Element(_node)
        _element.setAttributeNS(_namespace, _attr)
        _node.hasAttribute.assert_called_once_with('a')
        _node.hasAttributeNS.assert_called_once_with('b', 'local')
        _node.setAttribute.assert_not_called()
        _node.setAttributeNS.assert_not_called()

    def test_setAttributeNS_has_no_attributeNS_but_has_attribute(self):
        """Tests setAttributeNS method (has attribute, no attributeNS"""
        _node = MagicMock()
        _node.hasAttribute.return_value = True
        _node.hasAttributeNS.return_value = False
        _namespace = ('a', 'a1')
        _attr = ('b', 'local', '12')
        _element = Element(_node)
        _element.setAttributeNS(_namespace, _attr)
        _node.hasAttribute.assert_called_once_with('a')
        _node.hasAttributeNS.assert_called_once_with('b', 'local')
        _node.setAttribute.assert_not_called()
        _node.setAttributeNS.assert_called_once_with("b", "a:local", "12")

    def test_setAttributeNS_has_no_attribute_but_has_attributeNS(self):
        """Tests setAttributeNS method (no attribute, has attributeNS"""
        _node = MagicMock()
        _node.hasAttribute.return_value = False
        _node.hasAttributeNS.return_value = True
        _namespace = ('a', 'a1')
        _attr = ('b', 'local', '12')
        _element = Element(_node)
        _element.setAttributeNS(_namespace, _attr)
        _node.hasAttribute.assert_called_once_with('a')
        _node.hasAttributeNS.assert_called_once_with('b', 'local')
        _node.setAttribute.assert_called_once_with('a', 'a1')
        _node.setAttributeNS.assert_not_called()

    def test_setAttributeNS_has_no_attribute_and_has_no_attributeNS(self):
        """Tests setAttributeNS method (no attribute, no attributeNS"""
        _node = MagicMock()
        _node.hasAttribute.return_value = False
        _node.hasAttributeNS.return_value = False
        _namespace = ('a', 'a1')
        _attr = ('b', 'local', '12')
        _element = Element(_node)
        _element.setAttributeNS(_namespace, _attr)
        _node.hasAttribute.assert_called_once_with('a')
        _node.hasAttributeNS.assert_called_once_with('b', 'local')
        _node.setAttribute.assert_called_once_with('a', 'a1')
        _node.setAttributeNS.assert_called_once_with("b", "a:local", "12")

    def test_getAttribute_node_hasAttribute(self):
        """Tests getAttribute method"""
        _node = MagicMock()
        _node.getAttribute.return_value = 12
        _node.hasAttribute.return_value = True
        _element = Element(_node)
        self.assertEqual(_element.getAttribute('t1'), 12)
        _node.getAttribute.assert_called_once_with('t1')
        _node.hasAttribute.assert_called_once_with('t1')

    def test_getAttribute_node_hasNoAttribute(self):
        """Tests getAttribute method when node has attribute"""
        _get_local_name = self._init_patch_with_name(
            "_get_local_name", "xmind.core.Element.getLocalName", return_value='t1', autospec=True)
        _node = MagicMock()
        _node.getAttribute.return_value = 12
        _node.hasAttribute.return_value = False
        _element = Element(_node)
        self.assertEqual(_element.getAttribute('t1'), None)
        _node.getAttribute.assert_not_called()
        _node.hasAttribute.assert_called_once_with('t1')
        _get_local_name.assert_called_once_with(_element, 't1')

    def test_getAttribute_node_hasNoAttribute_localName_differs(self):
        """Tests getAttribute method when node has no attribute and localName differs from attribute name"""
        _get_local_name = self._init_patch_with_name(
            "_get_local_name", "xmind.core.Element.getLocalName", return_value='t2', autospec=True)
        _node = MagicMock()
        _node.getAttribute.return_value = 12
        _node.hasAttribute.side_effect = [False, True]
        _element = Element(_node)
        with patch.object(Element, 'getAttribute', wraps=_element.getAttribute) as _mock:
            self.assertEqual(_element.getAttribute('t1'), 12)

        self.assertEqual(_mock.call_count, 2)
        self.assertListEqual(_mock.call_args_list, [call('t1'), call('t2')])
        _node.getAttribute.assert_called_once_with('t2')
        self.assertEqual(_node.hasAttribute.call_count, 2)
        self.assertListEqual(_node.hasAttribute.call_args_list, [
                             call('t1'), call('t2')])
        _get_local_name.assert_called_once_with(_element, 't1')

    def test_setAttribute_attr_value_None(self):
        """Tests setAttribute when attr_value is None"""
        _node = MagicMock()
        _node.hasAttribute.return_value = False
        _element = Element(_node)
        _result = _element.setAttribute('some')
        self.assertIsNone(_result)
        _node.setAttribute.assert_not_called()
        _node.removeAttribute.assert_not_called()
        _node.hasAttribute.assert_called_once_with('some')

    def test_setAttribute_attr_value_is_not_None(self):
        """Tests setAttribute when attr_value is not None"""
        _node = MagicMock()
        _element = Element(_node)
        _result = _element.setAttribute('some', 2)
        self.assertIsNone(_result)
        _node.setAttribute.assert_called_once_with('some', '2')
        _node.removeAttribute.assert_not_called()
        _node.hasAttribute.assert_not_called()

    def test_setAttribute_attr_value_is_None_remove_attribute(self):
        """Tests setAttribute when attr_value is None, removeAttribute called"""
        _node = MagicMock()
        _node.hasAttribute.return_value = True
        _element = Element(_node)
        _result = _element.setAttribute('some')
        self.assertIsNone(_result)
        _node.setAttribute.assert_not_called()
        _node.removeAttribute.assert_called_once_with('some')
        _node.hasAttribute.assert_called_once_with('some')

    def test_createElement(self):
        """Tests createElement method, returns nothing"""
        _node = MagicMock()
        _element = Element(_node)
        _result = _element.createElement('some')
        self.assertIsNone(_result)

    def test_addIdAttribute_no_op(self):
        """Tests addIdAttribute when node has attribute already"""
        _node = MagicMock()
        _node.hasAttribute.return_value = True
        _element = Element(_node)
        _result = _element.addIdAttribute('some')
        self.assertIsNone(_result)
        _node.hasAttribute.assert_called_once_with('some')
        _node.setAttribute.assert_not_called()
        _node.setIdAttribute.assert_not_called()

    def test_addIdAttribute_no_document_owner(self):
        """Tests addIdAttribute when node has no attribute already and no owner of document"""
        _node = MagicMock()
        _node.hasAttribute.return_value = False
        _generate_id_mock = self._init_patch_with_name(
            '_generate_id', 'xmind.core.utils.generate_id', return_value=2, autospec=True)
        _get_owner_document = self._init_patch_with_name(
            '_getOwnerDocument', 'xmind.core.Element.getOwnerDocument', return_value=False, autospec=True)
        _element = Element(_node)
        _result = _element.addIdAttribute('some')
        self.assertIsNone(_result)
        _generate_id_mock.assert_called_once()
        _node.hasAttribute.assert_called_once_with('some')
        _node.setAttribute.assert_called_once_with('some', 2)
        _node.setIdAttribute.assert_not_called()
        _get_owner_document.assert_called_once()

    def test_addIdAttribute_has_document_owner(self):
        """Tests addIdAttribute when node has attribute already and has owner of document"""
        _node = MagicMock()
        _node.hasAttribute.return_value = False
        _generate_id_mock = self._init_patch_with_name(
            '_generate_id', 'xmind.core.utils.generate_id', return_value=2, autospec=True)
        _get_owner_document = self._init_patch_with_name(
            '_getOwnerDocument', 'xmind.core.Element.getOwnerDocument', return_value=True, autospec=True)
        _element = Element(_node)
        _result = _element.addIdAttribute('some')
        self.assertIsNone(_result)
        _generate_id_mock.assert_called_once()
        _node.hasAttribute.assert_called_once_with('some')
        _node.setAttribute.assert_called_once_with('some', 2)
        _node.setIdAttribute.assert_called_once_with('some')
        _get_owner_document.assert_called_once()

    def test_getIndex_no_parent_node(self):
        """Tests getIndex when no parent index"""
        _node = MagicMock()
        _getParentIndex = self._init_patch_with_name(
            '_getParentIndex', 'xmind.core.Element.getParentNode', return_value=False, autospec=True)
        _element = Element(_node)
        _result = _element.getIndex()
        self.assertEqual(_result, -1)
        _getParentIndex.assert_called_once()

    def test_getIndex_has_parent_node_with_no_childNodes(self):
        """Tests getIndex when it has parent but no childNodes"""
        _node = MagicMock()
        _parent = MagicMock()
        _childNodes = PropertyMock(return_value=iter([]))
        type(_parent).childNodes = _childNodes
        _getParentIndex = self._init_patch_with_name(
            '_getParentIndex', 'xmind.core.Element.getParentNode', return_value=_parent, autospec=True)
        _element = Element(_node)
        _result = _element.getIndex()
        self.assertEqual(_result, -1)
        _getParentIndex.assert_called_once()
        _childNodes.assert_called_once()

    def test_getIndex_has_parent_node_with_childNodes(self):
        """Tests getIndex when it has parent with childNodes"""
        _node = MagicMock()
        _parent = MagicMock()
        _childNodes = PropertyMock(return_value=iter([1, 2, 3, _node, 5, 6]))
        type(_parent).childNodes = _childNodes
        _getParentIndex = self._init_patch_with_name(
            '_getParentIndex', 'xmind.core.Element.getParentNode', return_value=_parent, autospec=True)
        _element = Element(_node)
        _result = _element.getIndex()
        self.assertEqual(_result, 3)
        _getParentIndex.assert_called_once()
        _childNodes.assert_called_once()

    def test_getTextContent_no_childNodes(self):
        """Tests getTextContent when it has no childNodes"""
        _node = MagicMock()
        _childNodes = PropertyMock(return_value=iter([]))
        type(_node).childNodes = _childNodes
        _element = Element(_node)
        _result = _element.getTextContent()
        self.assertIsNone(_result)
        _childNodes.assert_called_once()

    def test_getTextContent_has_childNodes_but_without_expected_nodeType(self):
        """Tests getTextContent whith childNodes"""
        _node = MagicMock()
        _childNodes = PropertyMock(return_value=iter(
            [InnerNode(0, '0'), InnerNode(1, '1')]))
        type(_node).childNodes = _childNodes
        _element = Element(_node)
        _result = _element.getTextContent()
        self.assertIsNone(_result)
        _childNodes.assert_called_once()

    def test_getTextContent_returns_text(self):
        """Tests getTextContent when it has proper data"""
        _node = MagicMock()
        _childNodes = PropertyMock(return_value=iter([InnerNode(0, '0'), InnerNode(
            3, '3'), InnerNode(3, '16'), InnerNode(1, '1')]))
        type(_node).childNodes = _childNodes
        _element = Element(_node)
        _result = _element.getTextContent()
        self.assertEqual(_result, '3\n16')
        _childNodes.assert_called_once()

    def test_setTextContent_no_childNodes(self):
        """Tests setTextContent when it has childNodes"""
        _node = MagicMock(childNodes=[])
        _childNodes = PropertyMock(return_value=iter([]))
        type(_node).childNodes = _childNodes
        _text_object = MagicMock()
        _dom_text = self._init_patch_with_name(
            '_dom_text', 'xmind.core.DOM.Text', return_value=_text_object, autospec=True)
        _element = Element(_node)
        _element.setTextContent('data2')
        _node.appendChild.assert_called_once_with(_text_object)
        _dom_text.assert_called_once()
        _node.removeChild.assert_not_called()
        _text_object.data = 'data2'
        _childNodes.assert_called_once()

    def test_setTextContent_has_childNodes(self):
        """Tests setTextContent when it has childNodes"""
        _childNodesValues = [
            InnerNode(0, '0'),
            InnerNode(3, '3'),
            InnerNode(3, '16'),
            InnerNode(1, '1')
        ]
        _node = MagicMock()
        _childNodes = PropertyMock(return_value=iter(_childNodesValues))
        type(_node).childNodes = _childNodes
        _text_object = MagicMock()
        _dom_text = self._init_patch_with_name(
            '_dom_text', 'xmind.core.DOM.Text', return_value=_text_object, autospec=True)
        _element = Element(_node)
        _element.setTextContent('data2')
        _node.appendChild.assert_called_once_with(_text_object)
        self.assertEqual(_node.removeChild.call_count, 2)
        self.assertListEqual(_node.removeChild.call_args_list, [
                             call(_childNodesValues[1]), call(_childNodesValues[2])])
        _dom_text.assert_called_once()
        _text_object.data = 'data2'
        _childNodes.assert_called_once()
