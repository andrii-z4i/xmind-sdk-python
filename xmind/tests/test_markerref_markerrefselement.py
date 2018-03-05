from xmind.core.markerref import MarkerRefsElement
from xmind.core.const import TAG_MARKERREFS
from xmind.tests import logging_configuration as lc
from xmind.tests import base
from unittest.mock import patch


class MarkerRefsElementTest(base.Base):
    """MarkerRefsElementTest"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('MarkerRefsElementTest')
        return self._logger

    def test_init_without_parameters(self):
        """test that object of the class could be created with different number of parameters and it has correct static attribute"""
        with patch('xmind.core.mixin.WorkbookMixinElement.__init__') as WorkbookMixinElementMock:
            _test_object = MarkerRefsElement()
            WorkbookMixinElementMock.assert_called_with(None, None)

            MarkerRefsElement('test')
            WorkbookMixinElementMock.assert_called_with('test', None)

            MarkerRefsElement('test', 2)
            WorkbookMixinElementMock.assert_called_with('test', 2)

            MarkerRefsElement(node=None, ownerWorkbook=3)
            WorkbookMixinElementMock.assert_called_with(None, 3)

            with self.assertRaises(Exception):
                MarkerRefsElement('test', 2, 4)

            self.assertEqual(WorkbookMixinElementMock.call_count, 4)
            self.assertEqual(_test_object.TAG_NAME, TAG_MARKERREFS)
