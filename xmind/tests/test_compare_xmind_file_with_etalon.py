#-*- coding: utf-8 -*-
import xmind, zipfile
from xmind.core import workbook, saver
from xmind.core.topic import TopicElement

from xmlscomparator.xml_diff import create_xml_diff_from_strings
from xmlscomparator.comparators.type_comparator import TypeComparator
from xmlscomparator.comparators.text_comparator import TextComparator
from xmlscomparator.comparators.attr_comparator_policy import AttrComparatorPolicy
from xmlscomparator.comparators.attr_comparator import AttrComparator

w = xmind.load("test.xmind") # load an existing file or create a new workbook if nothing is found
'''
s1 = w.getPrimarySheet() # get the first sheet
s1.setTitle("Source of IcMs") # set its title
r1 = s1.getRootTopic() # get the root topic of this sheet
r1.setTitle("we don't care of this sheet") # set its title
'''
''' Sheet Scenarios '''
#s2 = w.createSheet() # create a new sheet
s2 = w.getPrimarySheet() # get the first sheet
s2.setTitle("Scenarios")

''' Main Topic Scenarios  '''
r2 = s2.getRootTopic()
r2.setTitle("Scenarios")

'''=============================Topic Dialtone============================='''
t1 = TopicElement(ownerWorkbook=w) # create a new element
t1.setTitle("Dialtone") # set its title

''' Topic "behind the jail (80%)" '''
t1_1 = TopicElement(ownerWorkbook=w) # create a new element
t1_1.setTitle("behind the jail (80%)") # set its title

''' Topic "create_one_to_one_call" '''
t1_1_1 = TopicElement(ownerWorkbook=w) # create a new element
t1_1_1.setTitle("create_one_to_one_call") # set its title
t1_1_1.setURLHyperlink("https://domoreexp.visualstudio.com/MSTeams/_queries?id=222450&fullScreen=false&_a=edit")

''' Topic "join_or_create_meetup_from_link" '''
t1_1_2 = TopicElement(ownerWorkbook=w) # create a new element
t1_1_2.setTitle("join_or_create_meetup_from_link") # set its title
t1_1_2.setURLHyperlink("https://domoreexp.visualstudio.com/MSTeams/_workitems/edit/221727")

''' Adding subtopics to "behind the jail (80%)" topic '''
t1_1.addSubTopic(t1_1_1)
t1_1.addSubTopic(t1_1_2)

''' Topic "normal one (90%)" '''
t1_2 = TopicElement(ownerWorkbook=w) # create a new element
t1_2.setTitle("normal one (90%)") # set its title

''' Topic "media_connected" '''
t1_2_1 = TopicElement(ownerWorkbook=w) # create a new element
t1_2_1.setTitle("media_connected") # set its title

''' Topic "create_meetup" '''
t1_2_2 = TopicElement(ownerWorkbook=w) # create a new element
t1_2_2.setTitle("create_meetup") # set its title

''' Topic "join_meetup_reply_chain" '''
t1_2_3 = TopicElement(ownerWorkbook=w) # create a new element
t1_2_3.setTitle("join_meetup_reply_chain") # set its title

''' Topic "join_scheduled_meetup" '''
t1_2_4 = TopicElement(ownerWorkbook=w) # create a new element
t1_2_4.setTitle("join_scheduled_meetup") # set its title

''' Topic "call_accept" '''
t1_2_5 = TopicElement(ownerWorkbook=w) # create a new element
t1_2_5.setTitle("call_accept") # set its title

''' Adding subtopics to "normal one (90%)" topic '''
t1_2.addSubTopic(t1_2_1)
t1_2.addSubTopic(t1_2_2)
t1_2.addSubTopic(t1_2_3)
t1_2.addSubTopic(t1_2_4)
t1_2.addSubTopic(t1_2_5)

''' Adding subtopics to Dialtone topic '''
t1.addSubTopic(t1_1)
t1.addSubTopic(t1_2)

'''=============================Topic Optimal============================='''
t2 = TopicElement(ownerWorkbook=w)
t2.setTitle("Optimal")

''' Topic "get_meeting_info" '''
t2_1 = TopicElement(ownerWorkbook=w)
t2_1.setTitle("get_meeting_info")

''' Topic "get_exchange_meeting_info" '''
t2_2 = TopicElement(ownerWorkbook=w)
t2_2.setTitle("get_exchange_meeting_info")

''' Topic "start_recording" '''
t2_3 = TopicElement(ownerWorkbook=w)
t2_3.setTitle("start_recording")

''' Topic "stop_recording???" '''
t2_4 = TopicElement(ownerWorkbook=w)
t2_4.setTitle("stop_recording???")

''' Adding subtopics to Optimal topic '''
t2.addSubTopic(t2_1)
t2.addSubTopic(t2_2)
t2.addSubTopic(t2_3)
t2.addSubTopic(t2_4)

'''=============================Topic Core============================='''
t3 = TopicElement(ownerWorkbook=w)
t3.setTitle("Core")

''' Topic "behind the jail (85% threshold)" '''
t3_1 = TopicElement(ownerWorkbook=w)
t3_1.setTitle("behind the jail (85% threshold)")

''' Topic "add_participant" '''
t3_1_1 = TopicElement(ownerWorkbook=w)
t3_1_1.setTitle("add_participant")

''' Topic "create_group_call" '''
t3_1_2 = TopicElement(ownerWorkbook=w)
t3_1_2.setTitle("create_group_call")

''' Topic "join_group_call" '''
t3_1_3 = TopicElement(ownerWorkbook=w)
t3_1_3.setTitle("join_group_call")

''' Adding subtopics to "behind the jail (85% threshold)" topic '''
t3_1.addSubTopic(t3_1_1)
t3_1.addSubTopic(t3_1_2)
t3_1.addSubTopic(t3_1_3)

''' Topic "normal one (90% threshold)" '''
t3_2 = TopicElement(ownerWorkbook=w)
t3_2.setTitle("normal one (90% threshold)")

''' Topic "screen_sharing_sender_end" '''
t3_2_1 = TopicElement(ownerWorkbook=w)
t3_2_1.setTitle("screen_sharing_sender_end")

''' Topic "start_video" '''
t3_2_2 = TopicElement(ownerWorkbook=w)
t3_2_2.setTitle("start_video")

''' Topic "stop_video" '''
t3_2_3 = TopicElement(ownerWorkbook=w)
t3_2_3.setTitle("stop_video")

''' Topic "video_stream_rendering" '''
t3_2_4 = TopicElement(ownerWorkbook=w)
t3_2_4.setTitle("video_stream_rendering")

''' Topic "screen_sharing_sender" '''
t3_2_5 = TopicElement(ownerWorkbook=w)
t3_2_5.setTitle("screen_sharing_sender")

''' Topic "join_or_create_call_from_link" '''
t3_2_6 = TopicElement(ownerWorkbook=w)
t3_2_6.setTitle("join_or_create_call_from_link")

''' Topic "calling_service_init" '''
t3_2_7 = TopicElement(ownerWorkbook=w)
t3_2_7.setTitle("calling_service_init")

''' Topic "calling_relay_manager_query_relays_async" '''
t3_2_8 = TopicElement(ownerWorkbook=w)
t3_2_8.setTitle("calling_relay_manager_query_relays_async")

''' Topic "ecs_config_request" '''
t3_2_9 = TopicElement(ownerWorkbook=w)
t3_2_9.setTitle("ecs_config_request")

''' Topic "add_pstn_participant" '''
t3_2_10 = TopicElement(ownerWorkbook=w)
t3_2_10.setTitle("add_pstn_participant")

''' Topic "call_me_back" '''
t3_2_11 = TopicElement(ownerWorkbook=w)
t3_2_11.setTitle("call_me_back")

''' Topic "calling_mute_participant" '''
t3_2_12 = TopicElement(ownerWorkbook=w)
t3_2_12.setTitle("calling_mute_participant")

''' Topic "server_unmute_self" '''
t3_2_13 = TopicElement(ownerWorkbook=w)
t3_2_13.setTitle("server_unmute_self")

''' Topic "calling_mute_all" '''
t3_2_14 = TopicElement(ownerWorkbook=w)
t3_2_14.setTitle("calling_mute_all")

''' Adding subtopics to "normal one (90% threshold)" topic '''
t3_2.addSubTopic(t3_2_1)
t3_2.addSubTopic(t3_2_2)
t3_2.addSubTopic(t3_2_3)
t3_2.addSubTopic(t3_2_4)
t3_2.addSubTopic(t3_2_5)
t3_2.addSubTopic(t3_2_6)
t3_2.addSubTopic(t3_2_7)
t3_2.addSubTopic(t3_2_8)
t3_2.addSubTopic(t3_2_9)
t3_2.addSubTopic(t3_2_10)
t3_2.addSubTopic(t3_2_11)
t3_2.addSubTopic(t3_2_12)
t3_2.addSubTopic(t3_2_13)
t3_2.addSubTopic(t3_2_14)

''' Adding subtopics to Core topic '''
t3.addSubTopic(t3_1)
t3.addSubTopic(t3_2)

''' Adding subtopics to Scenarios main topic '''
r2.addSubTopic(t1)
r2.addSubTopic(t2)
r2.addSubTopic(t3)

w.addSheet(s2) # the second sheet is now added to the workbook

xmind.save(w, "test_file_to_compare.xmind") # and we save

test1 = zipfile.ZipFile('test_file_to_compare.xmind', 'r')
test_file_to_compare = test1.read(test1.namelist()[0])

test2 = zipfile.ZipFile('test_file.xmind', 'r')
test_file = test2.read(test2.namelist()[1])

_comparator = create_xml_diff_from_strings(test_file_to_compare, test_file)
print(_comparator.compare())
