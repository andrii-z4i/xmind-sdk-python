from xmind.tests import logging_configuration as lc
from xmind.core.notes import NotesElement
from xmind.tests import base
from unittest.mock import Mock, MagicMock, call, PropertyMock


class TestNotesElement(base.Base):
    """Test class for NotesElement class"""

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('notesElement')
        return self._logger

    def test_init(self):
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)

        _obj1 = NotesElement()
        _topic_mixin_element_init.assert_called_with(_obj1, None, None)
        self.assertEqual(_obj1.TAG_NAME, "notes")

        _obj2 = NotesElement(1)
        _topic_mixin_element_init.assert_called_with(_obj2, 1, None)
        self.assertEqual(_obj2.TAG_NAME, "notes")

        _obj3 = NotesElement(1, 2)
        _topic_mixin_element_init.assert_called_with(_obj3, 1, 2)
        self.assertEqual(_obj3.TAG_NAME, "notes")

        _obj4 = NotesElement(node=None, ownerTopic=1)
        _topic_mixin_element_init.assert_called_with(_obj4, None, 1)
        self.assertEqual(_obj4.TAG_NAME, "notes")

        with self.assertRaises(TypeError) as _ex:
            NotesElement(1, 2, 3)

        self.assertTrue(_ex.exception.args[0].find("__init__() takes") != -1)
        # 4 because for last case we don't get to __init__ of super
        self.assertEqual(_topic_mixin_element_init.call_count, 4)

    def test_getContent_no_content(self):
        _getFirstChildNodeByTagName = self._init_patch_with_name(
            '_getFirstChildNodeByTagName', 'xmind.core.notes.NotesElement.getFirstChildNodeByTagName', return_value=False, autospec=True)
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _plain_notest_init = self._init_patch_with_name(
            '_init_plain_notes', 'xmind.core.notes.PlainNotes.__init__', autospec=True)
        _get_owner_topic = self._init_patch_with_name(
            '_get_owner_topic', 'xmind.core.notes.NotesElement.getOwnerTopic', return_value='owner_topic', autospec=True)

        _object = NotesElement()
        _return_value = _object.getContent()
        self.assertEqual(_return_value, None)
        _getFirstChildNodeByTagName.assert_called_once_with(_object, "plain")
        _topic_mixin_element_init.assert_called_once_with(_object, None, None)
        _plain_notest_init.assert_not_called()
        _get_owner_topic.assert_not_called()

    def test_getContent_format_is_wrong_exception(self):
        _content = MagicMock()
        _getFirstChildNodeByTagName = self._init_patch_with_name(
            '_getFirstChildNodeByTagName', 'xmind.core.notes.NotesElement.getFirstChildNodeByTagName', return_value=_content, autospec=True)
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _plain_notest_init = self._init_patch_with_name(
            '_init_plain_notes', 'xmind.core.notes.PlainNotes.__init__', autospec=True)
        _get_owner_topic = self._init_patch_with_name(
            '_get_owner_topic', 'xmind.core.notes.NotesElement.getOwnerTopic', return_value='owner_topic', autospec=True)

        _object = NotesElement()
        with self.assertRaises(Exception) as _ex:
            _object.getContent("plain2")

        self.assertTrue(_ex.exception.args[0].find(
            "Only support plain text notes right now") != -1)
        _getFirstChildNodeByTagName.assert_called_once_with(_object, "plain2")
        _topic_mixin_element_init.assert_called_once_with(_object, None, None)
        _plain_notest_init.assert_not_called()
        _get_owner_topic.assert_not_called()

    def test_getContent_getTextContent_on_content(self):
        _content = MagicMock()
        _content.getTextContent.return_value = 5
        _getFirstChildNodeByTagName = self._init_patch_with_name(
            '_getFirstChildNodeByTagName', 'xmind.core.notes.NotesElement.getFirstChildNodeByTagName', return_value=_content, autospec=True)
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _plain_notes_init = self._init_patch_with_name(
            '_init_plain_notes', 'xmind.core.notes.PlainNotes', return_value=_content, autospec=True)
        _get_owner_topic = self._init_patch_with_name(
            '_get_owner_topic', 'xmind.core.notes.NotesElement.getOwnerTopic', return_value='owner_topic', autospec=True)

        _object = NotesElement()
        _return_value = _object.getContent()
        self.assertEqual(_return_value, 5)

        _getFirstChildNodeByTagName.assert_called_once_with(_object, "plain")
        _topic_mixin_element_init.assert_called_once_with(_object, None, None)
        _plain_notes_init.assert_called_once_with(
            node=_content, ownerTopic='owner_topic')

    def test_getContent_excessive_parameters(self):
        _getFirstChildNodeByTagName = self._init_patch_with_name(
            '_getFirstChildNodeByTagName', 'xmind.core.notes.NotesElement.getFirstChildNodeByTagName', return_value=False, autospec=True)
        _topic_mixin_element_init = self._init_patch_with_name(
            '_init_mixin', 'xmind.core.notes.TopicMixinElement.__init__', autospec=True)
        _plain_notest_init = self._init_patch_with_name(
            '_init_plain_notes', 'xmind.core.notes.PlainNotes.__init__', autospec=True)
        _get_owner_topic = self._init_patch_with_name(
            '_get_owner_topic', 'xmind.core.notes.NotesElement.getOwnerTopic', return_value='owner_topic', autospec=True)

        _object = NotesElement()
        with self.assertRaises(TypeError) as _ex:
            _object.getContent("plain", 33)

        self.assertTrue(_ex.exception.args[0].find("getContent() takes") != -1)
        _getFirstChildNodeByTagName.assert_not_called()
        _topic_mixin_element_init.assert_called_once_with(_object, None, None)
        _plain_notest_init.assert_not_called()
        _get_owner_topic.assert_not_called()
