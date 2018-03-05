from xmind.tests import logging_configuration as lc
from xmind.core.position import PositionElement
from xmind.tests import base
from unittest.mock import patch
from xmind.core.const import TAG_POSITION, ATTR_X, ATTR_Y


class TestPositionElement(base.Base):
    """Test class for PositionElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('positionElement')
        return self._logger

    def test_init(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__', autospec=True)

        _obj1 = PositionElement()
        _workbook_mixin_element_init.assert_called_with(_obj1, None, None)
        self.assertEqual(TAG_POSITION, _obj1.TAG_NAME)

        _obj2 = PositionElement(1)
        _workbook_mixin_element_init.assert_called_with(_obj2, 1, None)
        self.assertEqual(TAG_POSITION, _obj2.TAG_NAME)

        _obj3 = PositionElement(None, 1)
        _workbook_mixin_element_init.assert_called_with(_obj3, None, 1)
        self.assertEqual(TAG_POSITION, _obj3.TAG_NAME)

        _obj4 = PositionElement(1, 2)
        _workbook_mixin_element_init.assert_called_with(_obj4, 1, 2)
        self.assertEqual(TAG_POSITION, _obj4.TAG_NAME)

        _obj5 = None
        with self.assertRaises(TypeError) as _ex:
            _obj5 = PositionElement(1, 2, 3)

        self.assertEqual(None, _obj5)
        self.assertTrue(_ex.exception.args[0].find(
            "__init__() takes") != -1)
        self.assertEqual(_workbook_mixin_element_init.call_count, 4)

    def test_excessive_parameters(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__')
        _get_attribute = self._init_patch_with_name(
            '_get_attribute', 'xmind.core.position.PositionElement.getAttribute')
        _set_attribute = self._init_patch_with_name(
            '_set_attribute', 'xmind.core.position.PositionElement.setAttribute')

        _element = PositionElement()
        _workbook_mixin_element_init.assert_called_once_with(None, None)

        _parameters = [
            ('getX', 0),
            ('getY', 0),
            ('setX', 1),
            ('setY', 1)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

        _get_attribute.assert_not_called()
        _set_attribute.assert_not_called()

    def test_getX(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__')

        _element = PositionElement()
        with patch.object(_element, 'getAttribute') as _get_attribute:
            _get_attribute.return_value = 10
            self.assertEqual(10, _element.getX())

        _workbook_mixin_element_init.assert_called_once_with(None, None)
        _get_attribute.assert_called_once_with(ATTR_X)

    def test_getY(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__')

        _element = PositionElement()
        with patch.object(_element, 'getAttribute') as _get_attribute:
            _get_attribute.return_value = 11
            self.assertEqual(11, _element.getY())

        _workbook_mixin_element_init.assert_called_once_with(None, None)
        _get_attribute.assert_called_once_with(ATTR_Y)

    def test_setX(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__')

        _element = PositionElement()
        with patch.object(_element, 'setAttribute') as _set_attribute:
            _set_attribute.return_value = 12
            self.assertIsNone(_element.setX(12))

        _workbook_mixin_element_init.assert_called_once_with(None, None)
        _set_attribute.assert_called_once_with(ATTR_X, 12)

    def test_setY(self):
        _workbook_mixin_element_init = self._init_patch_with_name(
            '_mixin_init', 'xmind.core.position.WorkbookMixinElement.__init__')

        _element = PositionElement()
        with patch.object(_element, 'setAttribute') as _set_attribute:
            _set_attribute.return_value = 13
            self.assertIsNone(_element.setY(13))

        _workbook_mixin_element_init.assert_called_once_with(None, None)
        _set_attribute.assert_called_once_with(ATTR_Y, 13)
