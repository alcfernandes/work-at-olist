from datetime import datetime

from django.test import TestCase

from freezegun import freeze_time

from calls.core.util.helpers import time_between, current_month_year


class TimeBetweenTest(TestCase):
    def test_delta_hours_minutes_seconds(self):
        expected = '1h5m5s'
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 11, 15, 25))
        self.assertEqual(expected, result)

    def test_delta_minutes_seconds(self):
        expected = '0h5m5s'
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 10, 15, 25))
        self.assertEqual(expected, result)

    def test_delta_seconds(self):
        expected = '0h0m5s'
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 1, 10, 10, 25))
        self.assertEqual(expected, result)

    def test_delta_days(self):
        expected = '24h0m5s'
        result = time_between(datetime(2018, 1, 1, 10, 10, 20), datetime(2018, 1, 2, 10, 10, 25))
        self.assertEqual(expected, result, msg="Delta days must be add on hours value.")


class CurrentMonthYearTest(TestCase):
    @freeze_time('2018-11-10')
    def test_current_month_year(self):
        expected_result = datetime(2018, 11, 1)
        result = current_month_year()
        self.assertEqual(expected_result, result)

