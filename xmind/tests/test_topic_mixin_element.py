from xmind.core.mixin import TopicMixinElement
from xmind.tests import logging_configuration as lc
from xmind.tests import base
from unittest.mock import patch, MagicMock


class TopicMixinElementTest(base.Base):
    """TopicMixinElementTest"""

    def setUp(self):
        super(TopicMixinElementTest, self).setUp()
        self._init_method = self._init_patch_with_name(
            '_init', 'xmind.core.Element.__init__')
        self._ownerTopic = MagicMock()

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('TopicMixinElementTest')
        return self._logger

    def test_excessive_parameters(self):

        _element = TopicMixinElement(None, None)
        self._init_method.assert_called_once_with(None)

        _parameters = [
            ('getOwnerTopic', 0),
            ('getOwnerSheet', 0),
            ('getOwnerWorkbook', 0)
        ]

        for pair in _parameters:
            with self.subTest(pair=pair):
                self._test_method_by_excessive_parameters(pair, _element)

    def test_init_without_parameters(self):
        self.assertRaises(TypeError, TopicMixinElement)

    def test_get_owner_topic(self):
        _element = TopicMixinElement(None, self._ownerTopic)
        self.assertEqual(_element.getOwnerTopic(), self._ownerTopic)

    def test_get_owner_sheet(self):
        self._ownerTopic.getOwnerSheet.return_value = "owner"
        _element = TopicMixinElement(None, self._ownerTopic)

        self.assertEqual("owner", _element.getOwnerSheet())
        self.assertEqual(self._ownerTopic.getOwnerSheet.call_count, 1)

    def test_get_owner_sheet_without_input_owner(self):
        self._ownerTopic.getOwnerSheet.return_value = "owner"
        _element = TopicMixinElement(None, None)

        self.assertEqual(None, _element.getOwnerSheet())
        self.assertEqual(self._ownerTopic.getOwnerSheet.call_count, 0)

    def test_get_owner_workbook(self):
        self._ownerTopic.getOwnerWorkbook.return_value = "owner"
        _element = TopicMixinElement(None, self._ownerTopic)

        self.assertEqual("owner", _element.getOwnerWorkbook())
        self.assertEqual(self._ownerTopic.getOwnerWorkbook.call_count, 1)

    def test_get_owner_workbook_without_input_owner(self):
        self._ownerTopic.getOwnerWorkbook.return_value = "owner"
        _element = TopicMixinElement(None, None)

        self.assertEqual(None, _element.getOwnerWorkbook())
        self.assertEqual(self._ownerTopic.getOwnerWorkbook.call_count, 0)
