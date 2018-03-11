from xmind.tests import logging_configuration as lc
from xmind.core.title import TitleElement
from xmind.tests import base
from unittest.mock import call
from xmind.core.const import *


class TestTitleElement(base.Base):
    """Test class for TitleElement class"""

    def setUp(self):
        super(TestTitleElement, self).setUp()
        self._workbook_mixin_element_mock = self._init_patch_with_name(
            '_wb_mixin_mock', 'xmind.core.topic.WorkbookMixinElement.__init__', autospec=True)

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('titleElement')
        return self._logger

    def test_excessive_parameters(self):
        _title_element = TitleElement()

        self._test_method_by_excessive_parameters(
            ('__init__', (2, False)), _title_element)

        self.assertEqual(_title_element.TAG_NAME, TAG_TITLE)
        self._workbook_mixin_element_mock.assert_called_once_with(
            _title_element, None, None)

    def test_init(self):
        _element1 = TitleElement(node='a1')
        _element2 = TitleElement(ownerWorkbook='b2')
        _element3 = TitleElement(node='a3', ownerWorkbook='b3')
        self.assertEqual(3, self._workbook_mixin_element_mock.call_count)
        self.assertListEqual(
            [
                call(_element1, 'a1', None),
                call(_element2, None, 'b2'),
                call(_element3, 'a3', 'b3')
            ],
            self._workbook_mixin_element_mock.call_args_list
        )
        for _element in (_element1, _element2, _element3):
            self.assertEqual(_element.TAG_NAME, TAG_TITLE)
