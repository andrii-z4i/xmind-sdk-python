#-*- coding: utf-8 -*-
import xmind, zipfile, logging, datetime, json
from xmind.core import workbook, saver, const
from xmind.core.topic import TopicElement


class CreateXmindFileFromJson:

    def create_topic(self, topic, father_topic, workbook, topics_type=const.TOPIC_ATTACHED):
        if type(topic) == list:
            for i in topic:
                t = TopicElement(ownerWorkbook=workbook)
                t.setTitle(i["title"])
                father_topic.addSubTopic(t, topics_type=topics_type)
                xmind.save(w, "fil1.xmind")
                try:
                    if type(i["children"]["topics"]) == list:
                        self.create_topic(i["children"]["topics"][0]["topic"], t, workbook)
                        self.create_topic(i["children"]["topics"][1]["topic"], t, workbook, topics_type="detached")
                    else:
                        self.create_topic(i["children"]["topics"]["topic"], t, workbook)
                except:
                    print("the end of tree")
        elif type(topic) == dict:
            t = TopicElement(ownerWorkbook=workbook)
            t.setTitle(topic["title"])
            father_topic.addSubTopic(t)
            xmind.save(w, "fil1.xmind")
            try:
                if type(topic["children"]["topics"]) == list:
                    self.create_topic(topic["children"]["topics"][0]["topic"], t, workbook)
                    self.create_topic(topic["children"]["topics"][1]["topic"], t, workbook, topics_type="detached")
                else:
                    self.create_topic(topic["children"]["topics"]["topic"], t, workbook)
            except:
                print("the end of tree")

test = CreateXmindFileFromJson()
json_data = json.load(open('test_file.json'))

w = xmind.load("f.xmind")
sheet = w.getPrimarySheet()
sheet.setTitle("test")
root_topic = sheet.getRootTopic()
root_topic.setTitle(json_data["xmap-content"]["sheet"]["topic"]["title"])

test.create_topic(json_data["xmap-content"]["sheet"]["topic"], root_topic, w)

xmind.save(w, "fil1.xmind")
