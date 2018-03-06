#-*- coding: utf-8 -*-
import xmind, zipfile, logging, datetime, json
from xmind.core import workbook, saver, const
from xmind.core.topic import TopicElement


class CreateXmindFileFromJson:

    DB_of_topics = {}

    def create_topics(self, topic, father_topic, workbook, topics_type=const.TOPIC_ATTACHED):
        if type(topic) == list:
            for i in topic:
                t = TopicElement(ownerWorkbook=workbook)
                t.setTitle(i["title"])
                self.DB_of_topics.update({i["-id"]: t})
                father_topic.addSubTopic(t, topics_type=topics_type)
                try:
                    if type(i["children"]["topics"]) == list:
                        self.create_topics(i["children"]["topics"][0]["topic"], t, workbook)
                        self.create_topics(i["children"]["topics"][1]["topic"], t, workbook, topics_type="detached")
                    else:
                        self.create_topics(i["children"]["topics"]["topic"], t, workbook)
                except:
                    print("the end of branch")
        elif type(topic) == dict:
            if not father_topic:
                sheet = w.getPrimarySheet()
                sheet.setTitle("test")
                t = sheet.getRootTopic()
                t.setTitle(topic["title"])
                self.DB_of_topics.update({topic["-id"]: t})
            else:
                t = TopicElement(ownerWorkbook=workbook)
                t.setTitle(topic["title"])
                self.DB_of_topics.update({topic["-id"]: t})
                father_topic.addSubTopic(t, topics_type=topics_type)
            try:
                if type(topic["children"]["topics"]) == list:
                    self.create_topics(topic["children"]["topics"][0]["topic"], t, workbook)
                    self.create_topics(topic["children"]["topics"][1]["topic"], t, workbook, topics_type="detached")
                else:
                    self.create_topics(topic["children"]["topics"]["topic"], t, workbook)
            except:
                print("the end of branch")

   #def create_relationships(self):


test = CreateXmindFileFromJson()
json_data = json.load(open('test_file.json'))

w = xmind.load("f.xmind")

test.create_topics(json_data["xmap-content"]["sheet"]["topic"], None, w)
xmind.save(w, "fil1.xmind")
