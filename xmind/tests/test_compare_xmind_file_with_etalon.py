#-*- coding: utf-8 -*-
import zipfile
from xmlscomparator.xml_diff import create_xml_diff_from_strings
from xmlscomparator.comparators.type_comparator import TypeComparator
from xmlscomparator.comparators.text_comparator import TextComparator
from xmlscomparator.comparators.attr_comparator_policy import AttrComparatorPolicy
from xmlscomparator.comparators.attr_comparator import AttrComparator
from xmind.tests.create_xmind_file_from_json import CreateXmindFileFromJson


''' comparing block '''
obj = CreateXmindFileFromJson('test.xmind', 'test_file.json')
obj.create_xmind_file()

unarchived = zipfile.ZipFile('test.xmind', 'r')
test_file_to_compare = unarchived.read(unarchived.namelist()[0])

unarchived = zipfile.ZipFile('test_file.xmind', 'r')
test_file = unarchived.read(unarchived.namelist()[1])
print(test_file)
print(test_file_to_compare)


_type_comparator = TypeComparator()
_text_comparator = TextComparator()
_attr_comparator = AttrComparator("")
_attr_policy = AttrComparatorPolicy()
_attr_policy.add_attribute_name_to_skip_compare('extensions')
_attr_comparator.set_attr_comparator_policy(_attr_policy)
_attr_comparator.set_check_values(False)
_text_comparator.set_next_comparator(_attr_comparator)
_type_comparator.set_next_comparator(_text_comparator)
_comparator = create_xml_diff_from_strings(test_file, test_file_to_compare)
_comparator.set_comparator(_type_comparator)
_comparator.compare()

print(_comparator.compare())