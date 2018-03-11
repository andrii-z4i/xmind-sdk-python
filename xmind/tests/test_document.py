from xmind.tests import logging_configuration as lc
from xmind.core import Document
from xmind.tests import base
from unittest.mock import patch, MagicMock


class TestDocument(base.Base):
    """Tests for Document class from __init__"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('document')
        return self._logger

    def test_excessive_parameters(self):
        _document = Document(12)
        _parameters = [
            ('_documentConstructor', 0),
            ('getOwnerDocument', 0),
            ('createElement', 1),
            ('setVersion', 1),
            ('replaceVersion', 1),
            ('getElementById', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _document)

    def test_init_no_node(self):
        """Tests __init__ method without parameter"""
        _dom_document = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Document', return_value='value', autospec=True)
        _document = Document()
        _dom_document.assert_called_once()
        self.assertEqual(_document._node, 'value')

    def test_init_pass_node(self):
        """Tests __init__ method with parameter"""
        _dom_document = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Document', return_value='value', autospec=True)
        _document = Document(1)
        _dom_document.assert_not_called()
        self.assertEqual(_document._node, 1)

    def test_init_pass_more_parameters(self):
        """Tests __init__ method with more parameter"""
        _dom_document = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Document', return_value='value', autospec=True)
        with self.assertRaises(Exception):
            Document(1, 2)

        _dom_document.assert_not_called()

    def test_documentConstructor(self):
        """Tests _documentConstructor method"""
        _dom_document = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Document', return_value='dom', autospec=True)
        _document = Document(121212)  # value has to be taken from parameter
        _dom = _document._documentConstructor()
        _dom_document.assert_called_once()
        self.assertEqual(_document._node, 121212)
        self.assertEqual(_dom, 'dom')

    def test_documentElement_property(self):
        """Tests documentElement property"""
        _node = MagicMock(documentElement='something')
        _dom_document = self._init_patch_with_name(
            '_dm', 'xmind.core.DOM.Document', return_value='dom', autospec=True)
        _document = Document(_node)  # value has to be taken from parameter
        self.assertEqual(_document.documentElement, 'something')
        _dom_document.assert_not_called()

    def test_getOwnerDocument(self):
        """Tests getOwnerDocument method"""
        _node = MagicMock()
        _document = Document(_node)  # value has to be taken from parameter
        self.assertEqual(_document.getOwnerDocument(), _node)

    def test_createElement(self):
        """Tests createElement method"""
        _node = MagicMock()
        _node.createElement.return_value = 'super'
        _document = Document(_node)  # value has to be taken from parameter
        _value = _document.createElement('bla-bla')
        _node.createElement.assert_called_once_with('bla-bla')
        self.assertEqual(_value, 'super')

    def test_setVersion(self):
        """Tests setVersion method"""
        _documentElement = MagicMock()
        _documentElement.hasAttribute.return_value = False
        _node = MagicMock(documentElement=_documentElement)
        _document = Document(_node)  # value has to be taken from parameter
        _document.setVersion('123')
        _documentElement.setAttribute.assert_called_once_with("version", '123')
        _documentElement.hasAttribute.assert_called_once_with("version")

    def test_setVersion_no_element(self):
        """Tests setVersion method documentElement is None, no exception should be"""
        _node = MagicMock(documentElement=None)
        _document = Document(_node)  # value has to be taken from parameter
        _document.setVersion("123")

    def test_setVersion_version_has_been_already_set(self):
        """Tests setVersion method when version has been set before"""
        _documentElement = MagicMock()
        _documentElement.hasAttribute.return_value = True
        _node = MagicMock(documentElement=_documentElement)
        _document = Document(_node)  # value has to be taken from parameter
        _document.setVersion('123')
        _documentElement.setAttribute.assert_not_called()
        _documentElement.hasAttribute.assert_called_once_with("version")

    def test_replaceVersion_no_element(self):
        """Tests replaceVersion method documentElement is None, no exception should be"""
        _node = MagicMock(documentElement=None)
        _document = Document(_node)  # value has to be taken from parameter
        _document.replaceVersion("123")

    def test_replaceVersion(self):
        """Tests replaceVersion method"""
        _documentElement = MagicMock()
        _node = MagicMock(documentElement=_documentElement)
        _document = Document(_node)  # value has to be taken from parameter
        _document.replaceVersion('123')
        _documentElement.setAttribute.assert_called_once_with("version", '123')

    def test_getElementById(self):
        """Tests getElementById method"""
        _node = MagicMock()
        _node.getElementById.return_value = '3333333'
        _document = Document(_node)  # value has to be taken from parameter
        _element = _document.getElementById('222')
        _node.getElementById.assert_called_once_with('222')
        self.assertEqual(_element, '3333333')
