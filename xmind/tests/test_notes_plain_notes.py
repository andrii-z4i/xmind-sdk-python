from xmind.tests import logging_configuration as lc
from xmind.core.notes import PlainNotes
from xmind.tests import base
from unittest.mock import Mock, MagicMock, call, PropertyMock


class TestPlainNotes(base.Base):
    """Test class for PlainNotes class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('plainNotes')
        return self._logger

    def test_init(self):
        _note_content_element_init = self._init_patch_with_name(
            '_init_note_content_element', 'xmind.core.notes._NoteContentElement.__init__', autospec=True)
        _set_text_content = self._init_patch_with_name(
            '_set_text_content', 'xmind.core.notes.PlainNotes.setTextContent', autospec=True)

        _obj1 = PlainNotes()
        _note_content_element_init.assert_called_with(_obj1, None, None,)
        _set_text_content.assert_not_called()

        _obj2 = PlainNotes(1)
        _note_content_element_init.assert_called_with(_obj2, None, None)
        _set_text_content.assert_called_with(_obj2, 1)

        _obj3 = PlainNotes(1, 2)
        _note_content_element_init.assert_called_with(_obj3, 2, None)
        _set_text_content.assert_called_with(_obj3, 1)

        _obj4 = PlainNotes(1, 2, 3)
        _note_content_element_init.assert_called_with(_obj4, 2, 3)
        _set_text_content.assert_called_with(_obj4, 1)

        _obj5 = PlainNotes(content=None, node=1, ownerTopic=2)
        _note_content_element_init.assert_called_with(_obj5, 1, 2)

        _obj6 = PlainNotes(content=None, node=None, ownerTopic=2)
        _note_content_element_init.assert_called_with(_obj6, None, 2)

        with self.assertRaises(Exception):
            PlainNotes(1, 2, 3, 4)
        # 6 because for last case we don't get to __init__ of super
        self.assertEqual(_note_content_element_init.call_count, 6)
        # only 3 cases have to get to set text content method
        self.assertEqual(_set_text_content.call_count, 3)

    def test_setContent(self):
        _note_content_element_init = self._init_patch_with_name(
            '_init_note_content_element', 'xmind.core.notes._NoteContentElement.__init__', autospec=True)
        _set_text_content = self._init_patch_with_name(
            '_set_text_content', 'xmind.core.notes.PlainNotes.setTextContent', autospec=True)

        _object = PlainNotes()
        _set_text_content.assert_not_called()
        _object.setContent('test')
        _note_content_element_init.assert_called_once_with(_object, None, None)
        _set_text_content.assert_called_once_with(_object, 'test')

    def test_setContent_excessive_parameters(self):
        _note_content_element_init = self._init_patch_with_name(
            '_init_note_content_element', 'xmind.core.notes._NoteContentElement.__init__', autospec=True)
        _set_text_content = self._init_patch_with_name(
            '_set_text_content', 'xmind.core.notes.PlainNotes.setTextContent', autospec=True)

        _object = PlainNotes()
        _set_text_content.assert_not_called()

        with self.assertRaises(Exception):
            _object.setContent(1, 2)

        _note_content_element_init.assert_called_once_with(_object, None, None)
        _set_text_content.assert_not_called()
