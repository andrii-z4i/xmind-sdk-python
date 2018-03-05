from xmind.tests import logging_configuration as lc
from xmind.core.notes import _NoteContentElement
from xmind.tests import base
from unittest.mock import Mock, MagicMock, call, PropertyMock


class TestNoteContentElement(base.Base):
    """Test class for _NoteContentElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('noteContentElement')
        return self._logger

    def test_init(self):
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)

        _obj1 = _NoteContentElement()
        _topic_mixin_element_init.assert_called_with(_obj1, None, None)

        _obj2 = _NoteContentElement(1)
        _topic_mixin_element_init.assert_called_with(_obj2, 1, None)

        _obj3 = _NoteContentElement(1, 2)
        _topic_mixin_element_init.assert_called_with(_obj3, 1, 2)

        _obj4 = _NoteContentElement(node=None, ownerTopic=1)
        _topic_mixin_element_init.assert_called_with(_obj4, None, 1)

        with self.assertRaises(Exception):
            _NoteContentElement(1, 2, 3)
        # 4 because for last case we don't get to __init__ of super
        self.assertEqual(_topic_mixin_element_init.call_count, 4)

    def test_getFormat(self):
        _implementation = MagicMock(tagName='super')
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _get_implementation = self._init_patch_with_name(
            '_get_implementation', 'xmind.core.notes._NoteContentElement.getImplementation', return_value=_implementation, autospec=True)

        _object = _NoteContentElement(1, 2)
        _return_value = _object.getFormat()
        self.assertEqual(_return_value, 'super')

        _topic_mixin_element_init.assert_called_with(_object, 1, 2)
        _get_implementation.assert_called_with(_object)

    def test_getFormat_excessive_parameters(self):
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _get_implementation = self._init_patch_with_name(
            '_get_implementation', 'xmind.core.notes._NoteContentElement.getImplementation', autospec=True)

        _object = _NoteContentElement(1, 2)
        with self.assertRaises(Exception):
            _object.getFormat(12)

        _topic_mixin_element_init.assert_called_with(_object, 1, 2)
        _get_implementation.assert_not_called()
