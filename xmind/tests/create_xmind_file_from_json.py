#-*- coding: utf-8 -*-
import xmind, zipfile, logging, datetime, json
from xmind.core import workbook, saver, const
from xmind.core.topic import TopicElement


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
                t.setTitle(i["title"])
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
                t.setTitle(topic["title"])
                self.DB_of_topics.update({topic["-id"]: t})
            else:
                t = TopicElement(ownerWorkbook=self.workbook)
                t.setTitle(topic["title"])
                self.DB_of_topics.update({topic["-id"]: t})
                father_topic.addSubTopic(t, topics_type=topics_type)
            try:
                if type(topic["children"]["topics"]) == list:
                    self.create_topics(topic["children"]["topics"][0]["topic"], t, sheet)
                    self.create_topics(topic["children"]["topics"][1]["topic"], t, sheet, topics_type="detached")
                else:
                    self.create_topics(topic["children"]["topics"]["topic"], t, sheet)
            except:
                print("the end of branch")

    def create_relationships(self, sheet):
        for relationship in self.json_data["xmap-content"]["sheet"]["relationships"]["relationship"]:
            rel = sheet.createRelationship(self.DB_of_topics[relationship["-end1"]].getID(), self.DB_of_topics[relationship["-end2"]].getID(), relationship["title"])
            sheet.addRelationship(rel)

    def create_xmind_file(self):
        sheet = self.workbook.getPrimarySheet()
        sheet.setTitle("test")
        self.create_topics(self.json_data["xmap-content"]["sheet"]["topic"], None, sheet)
        self.create_relationships(sheet)
        xmind.save(self.workbook, self.xmind_filename)


test = CreateXmindFileFromJson('test.xmind', 'test_file.json')
test.create_xmind_file()



