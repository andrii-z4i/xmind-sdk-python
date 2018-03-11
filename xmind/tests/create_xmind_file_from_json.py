#-*- coding: utf-8 -*-
import xmind, json
from xmind.core import const
from xmind.core.topic import TopicElement
from xmind.tests import logging_configuration as lc

class CreateXmindFileFromJson():

    def getLogger(self):
        if not getattr(self, '_logger', None):
            self._logger = lc.get_logger('CreateXmindFileFromJson')
        return self._logger

    def __init__(self, xmind_filename, json_filename):
        self.DB_of_topics = {}
        self.workbook = xmind.load("1.xmind")
        self.xmind_filename = xmind_filename
        self.json_data = json.load(open(json_filename))

    def create_topics(self, topic, parent_topic, sheet, topics_type=const.TOPIC_ATTACHED):
        if type(topic) == list:
            for i in topic:
                t = TopicElement(ownerWorkbook=self.workbook)
                self.add_title(t, i)
                self.add_markers(t, i)
                self.add_position(t, i)
                self.add_attr_branch_folded(t, i)
                parent_topic.addSubTopic(t, topics_type=topics_type)
                try:
                    if type(i["children"]["topics"]) == list:
                        self.create_topics(i["children"]["topics"][0]["topic"], t, sheet)
                        self.create_topics(i["children"]["topics"][1]["topic"], t, sheet, topics_type="detached")
                    else:
                        self.create_topics(i["children"]["topics"]["topic"], t, sheet)
                except:
                    self.getLogger().debug("the end of branch")
                finally:
                    self.add_plain_notes(t, i)
                    self.DB_of_topics.update({i["-id"]: t})
        elif type(topic) == dict:
            if not parent_topic:
                t = sheet.getRootTopic()
            else:
                t = TopicElement(ownerWorkbook=self.workbook)
                parent_topic.addSubTopic(t, topics_type=topics_type)
            self.add_title(t, topic)
            self.add_markers(t, topic)
            self.add_position(t, topic)
            self.add_attr_branch_folded(t, topic)
            try:
                if type(topic["children"]["topics"]) == list:
                    self.create_topics(topic["children"]["topics"][0]["topic"], t, sheet)
                    self.create_topics(topic["children"]["topics"][1]["topic"], t, sheet, topics_type="detached")
                else:
                    self.create_topics(topic["children"]["topics"]["topic"], t, sheet)
            except:
                self.getLogger().debug("the end of branch")
            finally:
                self.add_plain_notes(t, topic)
                self.DB_of_topics.update({topic["-id"]: t})

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
            self.getLogger().debug("No relationships")

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
            self.getLogger().debug("No markers")

    def add_plain_notes(self, created_topic, topic_from_json):
        try:
            created_topic.setPlainNotes(topic_from_json["notes"]["plain"])
        except:
            self.getLogger().debug("No plain notes")

    def add_position(self, created_topic, topic_from_json):
        try:
            created_topic.setPosition(topic_from_json["position"]["-svg:x"], topic_from_json["position"]["-svg:y"])
        except:
            self.getLogger().debug("No position")

    def add_attr_branch_folded(self, created_topic, topic_from_json):
        try:
            if type(topic_from_json["-branch"]):
                created_topic.setFolded()
        except:
            self.getLogger().debug("No attribute branch")

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
