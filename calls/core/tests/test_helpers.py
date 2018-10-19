from datetime import datetime

from django.test import TestCase

from calls.core.util.helpers import time_between


class TimeBetweenTest(TestCase):
    def test_delta_hours_minutes_seconds(self):
        expected = {'hours': 1, 'minutes': 5, 'seconds': 5}
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 11, 15, 25))
        self.assertEqual(expected, result)

    def test_delta_minutes_seconds(self):
        expected = {'hours': 0, 'minutes': 5, 'seconds': 5}
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 10, 15, 25))
        self.assertEqual(expected, result)

    def test_delta_seconds(self):
        expected = {'hours': 0, 'minutes': 0, 'seconds': 5}
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 10, 10, 25))
        self.assertEqual(expected, result)

    def test_delta_days(self):
        expected = {'hours': 24, 'minutes': 0, 'seconds': 5}
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 2, 10, 10, 25))
        self.assertEqual(expected, result, msg="Delta days must be add on hours value.")

