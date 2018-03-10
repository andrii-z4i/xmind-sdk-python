#-*- coding: utf-8 -*-
import xmind, zipfile, json
from xmind.core import const
from xmind.core.topic import TopicElement
from xmlscomparator.xml_diff import create_xml_diff_from_strings
from xmlscomparator.comparators.type_comparator import TypeComparator
from xmlscomparator.comparators.text_comparator import TextComparator
from xmlscomparator.comparators.attr_comparator_policy import AttrComparatorPolicy
from xmlscomparator.comparators.attr_comparator import AttrComparator

class CreateXmindFileFromJson:

    def __init__(self, xmind_filename, json_filename):
        self.DB_of_topics = {}
        self.workbook = xmind.load("1.xmind")
        self.xmind_filename = xmind_filename
        self.json_data = json.load(open(json_filename))

    def create_topics(self, topic, father_topic, sheet, topics_type=const.TOPIC_ATTACHED):
        if type(topic) == list:
            for i in topic:
                t = TopicElement(ownerWorkbook=self.workbook)
                self.add_title(t, i)
                self.add_markers(t, i)
                self.add_plain_notes(t, i)
                self.add_position(t, i)
                self.add_attr_branch_folded(t, i)
                self.DB_of_topics.update({i["-id"]: t})
                father_topic.addSubTopic(t, topics_type=topics_type)
                try:
                    if type(i["children"]["topics"]) == list:
                        self.create_topics(i["children"]["topics"][0]["topic"], t, sheet)
                        self.create_topics(i["children"]["topics"][1]["topic"], t, sheet, topics_type="detached")
                    else:
                        self.create_topics(i["children"]["topics"]["topic"], t, sheet)
                except:
                    print("the end of branch")
        elif type(topic) == dict:
            if not father_topic:
                t = sheet.getRootTopic()
            else:
                t = TopicElement(ownerWorkbook=self.workbook)
                father_topic.addSubTopic(t, topics_type=topics_type)
            self.add_title(t, topic)
            self.add_markers(t, topic)
            self.add_plain_notes(t, topic)
            self.add_position(t, topic)
            self.add_attr_branch_folded(t, topic)
            self.DB_of_topics.update({topic["-id"]: t})
            try:
                if type(topic["children"]["topics"]) == list:
                    self.create_topics(topic["children"]["topics"][0]["topic"], t, sheet)
                    self.create_topics(topic["children"]["topics"][1]["topic"], t, sheet, topics_type="detached")
                else:
                    self.create_topics(topic["children"]["topics"]["topic"], t, sheet)
            except:
                print("the end of branch")

    def create_relationships(self, sheet, sheet_number=-1):
        try:
            if sheet_number != -1:
                for relationship in self.json_data["xmap-content"]["sheet"][sheet_number]["relationships"]["relationship"]:
                    rel = sheet.createRelationship(self.DB_of_topics[relationship["-end1"]].getID(), self.DB_of_topics[relationship["-end2"]].getID(), relationship["title"])
                    sheet.addRelationship(rel)
            else:
                for relationship in self.json_data["xmap-content"]["sheet"]["relationships"]["relationship"]:
                    rel = sheet.createRelationship(self.DB_of_topics[relationship["-end1"]].getID(), self.DB_of_topics[relationship["-end2"]].getID(), relationship["title"])
                    sheet.addRelationship(rel)
        except:
            print("No relationships")

    def add_title(self, created_topic, topic_from_json):
        if type(topic_from_json["title"]) == dict:
            created_topic.setTitle(topic_from_json["title"]["#text"])
        else:
            created_topic.setTitle(topic_from_json["title"])

    def add_markers(self, created_topic, topic_from_json):
        try:
            if type(topic_from_json["marker-refs"]["marker-ref"]) == list:
                for marker in topic_from_json["marker-refs"]["marker-ref"]:
                    created_topic.addMarker(marker["-marker-id"])
            else:
                created_topic.addMarker(topic_from_json["marker-refs"]["marker-ref"]["-marker-id"])
        except:
            print("No markers")

    def add_plain_notes(self, created_topic, topic_from_json):
        try:
            created_topic.setPlainNotes(topic_from_json["notes"]["plain"])
        except:
            print("No plain notes")

    def add_position(self, created_topic, topic_from_json):
        try:
            created_topic.setPosition(topic_from_json["position"]["-svg:x"], topic_from_json["position"]["-svg:y"])
        except:
            print("No position")

    def add_attr_branch_folded(self, created_topic, topic_from_json):
        try:
            if type(topic_from_json["-branch"]):
                created_topic.setFolded()
        except:
            print("No attribute branch")

    def create_xmind_file(self):
        sheet = self.workbook.getPrimarySheet()
        if type(self.json_data["xmap-content"]["sheet"]) == list:
            sheet.setTitle(self.json_data["xmap-content"]["sheet"][0]["title"])
            self.create_topics(self.json_data["xmap-content"]["sheet"][0]["topic"], None, sheet)
            self.create_relationships(sheet, 0)
            for i in range(1, len(self.json_data["xmap-content"]["sheet"])):
                sheet = self.workbook.createSheet()
                sheet.setTitle(self.json_data["xmap-content"]["sheet"][i]["title"])
                self.create_topics(self.json_data["xmap-content"]["sheet"][i]["topic"], None, sheet)
                self.create_relationships(sheet, i)
                self.workbook.addSheet(sheet)
        else:
            sheet.setTitle(self.json_data["xmap-content"]["sheet"]["title"])
            self.create_topics(self.json_data["xmap-content"]["sheet"]["topic"], None, sheet)
            self.create_relationships(sheet)

        xmind.save(self.workbook, self.xmind_filename)


test = CreateXmindFileFromJson('test.xmind', 'test_file.json')
test.create_xmind_file()


''' comparing block '''
test1 = zipfile.ZipFile('test.xmind', 'r')
test_file_to_compare = test1.read(test1.namelist()[0])

test2 = zipfile.ZipFile('test_file.xmind', 'r')
test_file = test2.read(test2.namelist()[1])
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