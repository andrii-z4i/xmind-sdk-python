import unittest
from unittest.mock import patch, Mock, MagicMock
from xmind.core.markerref import MarkerId
import logging
from . import base


class MarkerrefTest(base.Base):
    """Markerref test"""
    LOGGER = logging.getLogger('MarkerefTest')

    def test_init_set_name(self, name='test-name'):
        """test that object of the class could be created and will has correct name attribute"""
        el = MarkerId(name)
        self.assertEqual(el.name, name)

    def test_init_throws_missing_argument_exception(self):
        """test case when exception comes because the argument is missing"""
        with self.assertRaises(Exception) as ex:
            MarkerId()  # trying to create MarketId objectand waits for Exception

        self.LOGGER.warning("Exception: %s", ex.exception)

    def test_init_throws_excessive_argument_exception(self, name='test-name', second_arg = 'arg'):
        """test case when exception comes because of the excessive arguments"""
        with self.assertRaises(Exception) as ex:
            MarkerId(name, second_arg)  # trying to create MarketId objectand waits for Exception

        self.LOGGER.warning("Exception: %s", ex.exception)

    def test_str_method(self, name='test-name'):
        """test that __str__ method exists and returns correct representation"""
        el = MarkerId(name)
        self.assertEqual(el.__str__(), name)

    def test_repr_method(self, name='test-name'):
        """test that __repr__ method exists and returns correct representation"""
        el = MarkerId(name)
        self.assertEqual(el.__repr__(), "<MarkerId: %s>" % name)

    def test_get_family_method(self, name='test-name', exp_output = 'test'):
        """test that getFamily method exists and returns correct value"""
        el = MarkerId(name)
        self.assertEqual(el.getFamilly(), exp_output)

    def test_static_atributes(self):
        """test all static atributes of MfrkerId class"""
        m_id = MarkerId('a')
        parameters = [
            ('starRed', 'star-red'),
            ('starOrange', 'star-orange'),
            ('starYellow', 'star-yellow'),
            ('starBlue', 'star-blue'),
            ('starGreen', 'star-green'),
            ('starPurple', 'star-purple'),
            ('priority1', 'priority-1'),
            ('priority2', 'priority-2'),
            ('priority3', 'priority-3'),
            ('priority4', 'priority-4'),
            ('priority5', 'priority-5'),
            ('priority6', 'priority-6'),
            ('priority7', 'priority-7'),
            ('priority8', 'priority-8'),
            ('priority9', 'priority-9'),
            ('smileySmile', 'smiley-smile'),
            ('smileyLaugh', 'smiley-laugh'),
            ('smileyAngry', 'smiley-angry'),
            ('smileyCry', 'smiley-cry'),
            ('smileySurprise', 'smiley-surprise'),
            ('smileyBoring', 'smiley-boring'),
            ('task0_8', 'task-start'),
            ('task1_8', 'task-oct'),
            ('task2_8', 'task-quarter'),
            ('task3_8', 'task-3oct'),
            ('task4_8', 'task-half'),
            ('task5_8', 'task-5oct'),
            ('task6_8', 'task-3quar'),
            ('task7_8', 'task-7oct'),
            ('task8_8', 'task-done'),
            ('flagRed', 'flag-red'),
            ('flagOrange', 'flag-orange'),
            ('flagYellow', 'flag-yellow'),
            ('flagBlue', 'flag-blue'),
            ('flagGreen', 'flag-green'),
            ('flagPurple', 'flag-purple'),
            ('peopleRed', 'people-red'),
            ('peopleOrange', 'people-orange'),
            ('peopleYellow', 'people-yellow'),
            ('peopleBlue', 'people-blue'),
            ('peopleGreen', 'people-green'),
            ('peoplePurple', 'people-purple'),
            ('arrowUp', 'arrow-up'),
            ('arrowUpRight', 'arrow-up-right'),
            ('arrowRight', 'arrow-right'),
            ('arrowDownRight', 'arrow-down-right'),
            ('arrowDown', 'arrow-down'),
            ('arrowDownLeft', 'arrow-down-left'),
            ('arrowLeft', 'arrow-left'),
            ('arrowUpLeft', 'arrow-up-left'),
            ('arrowRefresh', 'arrow-refresh'),
            ('symbolPlus', 'symbol-plus'),
            ('symbolMinus', 'symbol-minus'),
            ('symbolQuestion', 'symbol-question'),
            ('symbolExclam', 'symbol-exclam'),
            ('symbolInfo', 'symbol-info'),
            ('symbolWrong', 'symbol-wrong'),
            ('symbolRight', 'symbol-right'),
            ('monthJan', 'month-jan'),
            ('monthFeb', 'month-feb'),
            ('monthMar', 'month-mar'),
            ('monthApr', 'month-apr'),
            ('monthMay', 'month-may'),
            ('monthJun', 'month-jun'),
            ('monthJul', 'month-jul'),
            ('monthAug', 'month-aug'),
            ('monthSep', 'month-sep'),
            ('monthOct', 'month-oct'),
            ('monthNov', 'month-nov'),
            ('monthDec', 'month-dec'),
            ('weekSun', 'week-sun'),
            ('weekMon', 'week-mon'),
            ('weekTue', 'week-tue'),
            ('weekWed', 'week-wed'),
            ('weekThu', 'week-thu'),
            ('weekFri', 'week-fri'),
            ('weekSat', 'week-sat')
        ]

        for pair in parameters:
            with self.subTest(pair=pair):
                self.LOGGER.info('Next pair %s', pair)
                property = getattr(m_id, pair[0], None)
                self.assertEqual(property, pair[1])
