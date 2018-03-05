from xmind.core.markerref import MarkerRefElement
from xmind.core.const import TAG_MARKERREF, ATTR_MARKERID
from xmind.tests import logging_configuration as lc
from xmind.tests import base
from unittest.mock import patch


class MarkerRefElementTest(base.Base):
    """MarkerRefElementTest"""

    def setUp(self):
        super(MarkerRefElementTest, self).setUp()
        self._WorkbookMixinElementMock = self._init_patch_with_name(
            '_init', 'xmind.core.mixin.WorkbookMixinElement.__init__')

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('MarkerRefElementTest')
        return self._logger

    def test_excessive_parameters(self):
        _element = MarkerRefElement(12)
        _parameters = [
            ('getMarkerId', 0),
            ('setMarkerId', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_init_without_parameters(self):
        """test that object of the class could be created with different number of parameters and it has correct static attribute"""
        _test_object = MarkerRefElement()
        self._WorkbookMixinElementMock.assert_called_with(None, None)

        MarkerRefElement('test')
        self._WorkbookMixinElementMock.assert_called_with('test', None)

        MarkerRefElement('test', 2)
        self._WorkbookMixinElementMock.assert_called_with('test', 2)

        MarkerRefElement(node=None, ownerWorkbook=3)
        self._WorkbookMixinElementMock.assert_called_with(None, 3)

        with self.assertRaises(Exception):
            MarkerRefElement('test', 2, 4)

        self.assertEqual(self._WorkbookMixinElementMock.call_count, 4)
        self.assertEqual(_test_object.TAG_NAME, TAG_MARKERREF)

    def test_getMarkerID(self):
        with patch('xmind.core.markerref.MarkerId') as _MarkerIdMock:
            _MarkerIdMock.return_value = 1

            with patch('xmind.core.Element.getAttribute') as _getAttributeMock:
                _getAttributeMock.return_value = 'attribute'

                _test_object = MarkerRefElement()
                _res = _test_object.getMarkerId()

                _getAttributeMock.assert_called_once_with(ATTR_MARKERID)
                _MarkerIdMock.assert_called_once_with('attribute')
                self.assertEqual(_res, 1)

    def test_setMarkerId(self):
        with patch('xmind.core.Element.setAttribute') as _setAttributeMock:
            _test_object = MarkerRefElement()
            _val = _test_object.setMarkerId(7)
            _setAttributeMock.assert_called_once_with(ATTR_MARKERID, '7')
            self.assertEqual(_val, None)
