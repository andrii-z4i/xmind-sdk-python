from xmind.tests import logging_configuration as lc
from xmind.tests import base
import xmind
import json
import os


class TestE2EOpen(base.Base):

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('TestE2EOpen')
        return self._logger

    def _check_sheets_number(self, workbook):
        _number = len(workbook.getSheets())
        self.assertEqual(
            _number, 2, 'Number of sheets is {} - expected 2'.format(_number))

    def _check_sheet_title(self, sheet, title):
        self.assertEqual(sheet.getTitle(), title)

    def _check_topic_title(self, topic, title):
        _topic_title_element = topic.getTitle()
        if type(title) is dict:
            self.assertEqual(_topic_title_element, title['#text'],
                             'Topic title is "{}", expected "{}"'.format(_topic_title_element, title['#text']))
        else:
            self.assertEqual(_topic_title_element, title,
                             'Topic title is "{}", expected "{}"'.format(_topic_title_element, title))

    def _check_relationship_title(self, relationship, title):
        _test_title = relationship.getElementsByTagName(
            'title')[0]._get_firstChild()._get_data()
        self.assertEqual(_test_title, title,
                         'Relationship title is "{}", expected "{}"'.format(_test_title, title))

    def _check_notes(self, topic, note):
        if topic.getNotes():
            _note = topic.getNotes().getContent()
            self.assertEqual(
                _note, note, 'Topic note is {}, expected "{}"'.format(_note, note))
        else:
            self.assertIsNone(note, 'Topic note is not None - expected None')

    def _check_tag_attribute(self, tag, attr_name, attr_value):
        _value = tag.getAttribute(attr_name)
        self.assertEqual(
            _value, attr_value, '{} expected to be {} - not {}'.format(attr_name, attr_value, _value))

    def _check_topic_marker_ref_attr(self, _root_test_topic, _root_expected_topic):
        _marker_ref = _root_test_topic._get_markerrefs()._get_firstChild()
        for _key, _value in _root_expected_topic['marker-refs']['marker-ref'].items():
            _ref_attr = _marker_ref.getAttribute(_key[1:])
            self.assertEqual(
                _ref_attr, _value, 'Expected {} value = {} - not {}'.format(_key, _value, _ref_attr))

    def _check_topic_position(self, _root_test_topic, _root_expected_topic):
        _test_position = _root_test_topic.getPosition()
        _expected_position = (
            int(_root_expected_topic['position']['-svg:x']), int(_root_expected_topic['position']['-svg:y']))
        self.assertEqual(_test_position, _expected_position,
                         'Expected position: {} - not {}'.format(_expected_position, _test_position))

    def _check_xmap_content(self, _workbook, _content):
        _xmap_test = _workbook.getChildNodesByTagName('xmap-content')[0]
        _xmap_expected = _content['xmap-content']
        for _key, _value in _xmap_expected.items():
            if _key[0] == '-':
                _test_attr = _xmap_test.getAttribute(_key[1:])
                self.assertEqual(_test_attr, _value,
                                 'Expected xmap {} value is: {} - not {}'.format(_key[1:], _value, _test_attr))

    def _check_element_extension(self, test_element, exp_element):
        if hasattr(test_element, 'getFirstChildNodeByTagName'):
            _test_ext = test_element.getFirstChildNodeByTagName(
                'extensions').getElementsByTagName('extension')[0]
        else:
            _test_ext = test_element.getElementsByTagName(
                'extensions')[0].getElementsByTagName('extension')[0]
        _expected_ext = exp_element['extensions']['extension']
        for _key, _value in _expected_ext.items():
            if _key[0] == '-':
                _test_value = _test_ext.getAttribute(_key[1:])
                self.assertEqual(_test_value, _value,
                                 'Expected extension value with attr {} is: {} - not {}'.format(_key[1:], _value,
                                                                                                _test_value))
            else:
                for _key_exp, _value_exp in _value.items():
                    _test_tag = _test_ext.getElementsByTagName(
                        _key)[0].getElementsByTagName(_key_exp)[0]
                    _test_value = _test_tag._get_firstChild()._get_data()
                self.assertEqual(_test_value, _value_exp,
                                 'Expected extension value for {} tag is: {} - not {}'.format(_key_exp, _value_exp,
                                                                                              _test_value))

    def _check_control_point(self, test_point, exp_point):
        for _key, _value in exp_point.items():
            self._check_tag_attribute(test_point, _key[1:], _value)

    def _check_control_points(self, test_points, exp_points):
        for i in range(0, len(exp_points)):
            self._check_control_point(test_points[i], exp_points[i])

    def _check_relationship(self, test_relationship, exp_relationship):
        self._check_relationship_title(
            test_relationship, exp_relationship['title'])
        for _key, _value in exp_relationship.items():
            if _key[0] == '-':
                self._check_tag_attribute(test_relationship, _key[1:], _value)
        self._check_control_points(test_relationship.getElementsByTagName('control-points')[0]._get_childNodes(),
                                   exp_relationship['control-points']['control-point'])

    def _check_relationships(self, test_sheet, exp_sheet):
        _test_relationships_list = test_sheet.getFirstChildNodeByTagName(
            'relationships')._get_childNodes()
        _exp_relationships_list = exp_sheet['relationships']['relationship']
        for _i in range(0, len(_exp_relationships_list)):
            self._check_relationship(
                _test_relationships_list[_i], _exp_relationships_list[_i])

    def _check_full_topic(self, _root_topic_test, _root_topic_expected):
        self._check_topic_title(
            _root_topic_test, _root_topic_expected['title'])
        for _key, _value in _root_topic_expected.items():
            if _key[0] == '-':
                self._check_tag_attribute(_root_topic_test, _key[1:], _value)
        if 'notes' in _root_topic_expected:
            self._check_notes(_root_topic_test,
                              _root_topic_expected['notes']['plain'])
        if 'marker-refs' in _root_topic_expected:
            self._check_topic_marker_ref_attr(
                _root_topic_test, _root_topic_expected)
        if 'position' in _root_topic_expected:
            self._check_topic_position(_root_topic_test, _root_topic_expected)
        if 'extensions' in _root_topic_expected:
            self._check_element_extension(
                _root_topic_test, _root_topic_expected)

        # Check attached subtopics of root topic
        if 'children' in _root_topic_expected:
            _children = _root_topic_expected['children']['topics']
            if type(_children) is list:
                for element in _root_topic_expected['children']['topics']:
                    _subtopics_list_test = _root_topic_test.getSubTopics(
                        element['-type'])
                    _subtopics_list_expected = element['topic']
                    if type(_subtopics_list_expected) is not list:
                        _subtopics_list_expected = [_subtopics_list_expected]
                    for i in range(0, len(_subtopics_list_expected)):
                        self._check_full_topic(
                            _subtopics_list_test[i], _subtopics_list_expected[i])
            else:
                _subtopics_list_test = _root_topic_test.getSubTopics(
                    _children['-type'])
                _subtopics_list_expected = _children['topic']
                if type(_subtopics_list_expected) is not list:
                    _subtopics_list_expected = [_subtopics_list_expected]
                for i in range(0, len(_subtopics_list_expected)):
                    self._check_full_topic(
                        _subtopics_list_test[i], _subtopics_list_expected[i])

    # This is the test!
    def test_e2e_open(self):
        current_dir = os.path.dirname(__file__)
        content_file_path = os.path.join(current_dir, 'content.json')
        xmind_file_path = os.path.join(current_dir, 'test_file.xmind')
        with open(content_file_path, 'r') as file:
            _content = json.load(file)
        _workbook = xmind.load(xmind_file_path)
        self.assertTrue(_workbook, 'There is no workbook!')
        self._check_sheets_number(_workbook)
        self._check_xmap_content(_workbook, _content)
        self._check_element_extension(_workbook.getChildNodesByTagName(
            'xmap-content')[0], _content['xmap-content'])

        for i in range(0, len(_content['xmap-content']['sheet'])):
            _test_sheet = _workbook.getSheets()[i]
            _expected_sheet = _content['xmap-content']['sheet'][i]
            self._check_sheet_title(_test_sheet, _expected_sheet['title'])
            if _test_sheet.getFirstChildNodeByTagName('relationships'):
                self._check_relationships(_test_sheet, _expected_sheet)

            # Checking sheet attributes
            for _key, _value in _expected_sheet.items():
                if _key[0] == '-':
                    self._check_tag_attribute(_test_sheet, _key[1:], _value)

            # Check root topic title, attributes, notes
            _root_topic_test = _test_sheet.getRootTopic()
            _root_topic_expected = _expected_sheet['topic']
            self._check_full_topic(_root_topic_test, _root_topic_expected)
