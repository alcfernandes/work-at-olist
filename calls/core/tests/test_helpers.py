from datetime import datetime

from django.test import TestCase

from freezegun import freeze_time

from calls.core.util.helpers import time_between, current_month_year, last_month_year, valid_phone_number


class TimeBetweenTest(TestCase):
    """
    time_between() should return the elapsed time between two dates and times in the format _h_m_s
    e.g. 0h35m42s
    """

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
    """
    current_month_year() should return a date and time corresponding to the first day of the current month and year
    """
    @freeze_time('2018-11-10')
    def test_current_month_year(self):
        expected_result = datetime(2018, 11, 1)
        result = current_month_year()
        self.assertEqual(expected_result, result)


class LastMonthYearTest(TestCase):
    """
    last_month_year() should return a date and time corresponding to the first day of the last month and year
    """
    @freeze_time('2018-11-10')
    def test_last_month_year(self):
        expected_result = datetime(2018, 10, 1)
        result = last_month_year()
        self.assertEqual(expected_result, result)

    @freeze_time('2018-01-10')
    def test_last_month_year_when_january(self):
        expected_result = datetime(2017, 12, 1)
        result = last_month_year()
        self.assertEqual(expected_result, result)


class ValidPhoneNumberTest(TestCase):
    """
    ValidPhoneNumber(telephone) should return True if telephone has a valid format.
    Only digits. Length: 10-11.
    """
    def test_only_digits_validation(self):
        self.assertFalse(valid_phone_number('XPT1234567'))

    def test_max_digits_validation(self):
        self.assertFalse(valid_phone_number('123456789012'))

    def test_min_digits_validation(self):
        self.assertFalse(valid_phone_number('123456789'))

    def test_valid_phone_validation(self):
        self.assertTrue(valid_phone_number('1234567890'))
