import pytz

from decimal import Decimal

from datetime import time, datetime

from django.test import TestCase

from calls.core.models.pricing_rule import PricingRule


def create_default_pricing_rules(self):

    self.standard_tariff = PricingRule.objects.create(
        id=1,
        name="Standard time call",
        start_time=time(6, 0, 0),
        end_time=time(22, 0, 0),
        standing_charge=Decimal(0.36),
        minute_call_charge=Decimal(0.09),
    )

    PricingRule.objects.create(
        id=2,
        name="Reduced tariff time call",
        start_time=time(22, 0, 0),
        end_time=time(6, 0, 0),
        standing_charge=Decimal(0.36),
        minute_call_charge=Decimal(0.01),
    )


class PricingRuleModelTest(TestCase):
    def setUp(self):
        self.rule = PricingRule(
            id=1,
            name="Standard time call",
            start_time=time(6, 0, 0),
            end_time=time(22, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )
        self.rule.save()

    def test_create(self):
        self.assertTrue(PricingRule.objects.exists())

    def test_str(self):
        self.assertEqual("Standard time call", str(self.rule))


class MapDayTimeRulesMethodTest(TestCase):
    """
    Should returns the pricing rules, breaking time bands
    that pass from one day to another (eg 22:00 to 06:00), one for each day
    eg (22:00 to 06:00) => (22:00 to 23:59 and 00:00 to 06:00)
    """
    def test_rules_method_case_1(self):
        """
        Case 1: 22:00 to 06:00
        """
        PricingRule.objects.create(
            id=1,
            name="Standard time call",
            start_time=time(6, 0, 0),
            end_time=time(22, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )

        PricingRule.objects.create(
            id=2,
            name="Reduced tariff time call",
            start_time=time(22, 0, 0),
            end_time=time(6, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.01),
        )

        expected_result = [
            {
                'start_time': time(6, 0, 0),
                'end_time': time(22, 0, 0),
                'id': 1,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.09'),
            },
            {
                'start_time': time(22, 0, 0),
                'end_time': time(0, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
            {
                'start_time': time(0, 0, 0),
                'end_time': time(6, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
        ]

        result = PricingRule.map_day_time_rules()

        self.assertEqual(expected_result, result)

    def test_rules_method_case_2(self):
        """
        Case 2: 18:00 to 00:00
        """
        PricingRule.objects.create(
            id=1,
            name="Standard time call",
            start_time=time(0, 0, 0),
            end_time=time(18, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )

        PricingRule.objects.create(
            id=2,
            name="Reduced tariff time call",
            start_time=time(18, 0, 0),
            end_time=time(0, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.01),
        )

        expected_result = [
            {
                'start_time': time(0, 0, 0),
                'end_time': time(18, 0, 0),
                'id': 1,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.09'),
            },
            {
                'start_time': time(18, 0, 0),
                'end_time': time(0, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
            {
                'start_time': time(0, 0, 0),
                'end_time': time(0, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
        ]

        result = PricingRule.map_day_time_rules()

        self.assertEqual(expected_result, result)


class PrincesForPeriodMethodTest(TestCase):
    """
    Given an initial start time and end time, the method 'prices_for_time_period' must return
    the tariff corresponding to each period of time registered in the rules of prices.
    """
    def setUp(self):
        create_default_pricing_rules(self)

    def test_prices_for_period_method_case_1(self):
        """
        Case 1: 2017-12-12 21:57:13 to 2017-12-12 22:17:53
        Same day - Starts on Standard tariff. Ends on Reduced tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'start_datetime': datetime(2017, 12, 12, 21, 57, 13, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 12, 22, 00, 00, tzinfo=pytz.UTC),
                'minutes': 2,
                'call_charge': Decimal('0.18'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'start_datetime': datetime(2017, 12, 12, 22, 00, 00, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 12, 22, 17, 53, tzinfo=pytz.UTC),
                'minutes': 17,
                'call_charge': Decimal('0.17'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_period(
            datetime(2017, 12, 12, 21, 57, 13, tzinfo=pytz.UTC),
            datetime(2017, 12, 12, 22, 17, 53, tzinfo=pytz.UTC)
        )

        self.assertEqual(expected_result, result)

    def test_prices_for_period_method_case_2(self):
        """
        Case 2: 2017-12-12 21:57:13 to 2017-12-13 22:10:56
        Different days.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'start_datetime': datetime(2017, 12, 12, 21, 57, 13, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 12, 22, 00, 00, tzinfo=pytz.UTC),
                'minutes': 2,
                'call_charge': Decimal('0.18'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'start_datetime': datetime(2017, 12, 12, 22, 00, 00, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 13, 00, 00, 00, tzinfo=pytz.UTC),
                'minutes': 120,
                'call_charge': Decimal('1.20'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'start_datetime': datetime(2017, 12, 13, 00, 00, 00, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 13, 6, 00, 00, tzinfo=pytz.UTC),
                'minutes': 360,
                'call_charge': Decimal('3.60'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 1,
                'start_datetime': datetime(2017, 12, 13, 6, 00, 00, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 13, 22, 00, 00, tzinfo=pytz.UTC),
                'minutes': 960,
                'call_charge': Decimal('86.40'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'start_datetime': datetime(2017, 12, 13, 22, 00, 00, tzinfo=pytz.UTC),
                'end_datetime': datetime(2017, 12, 13, 22, 10, 56, tzinfo=pytz.UTC),
                'minutes': 10,
                'call_charge': Decimal('0.10'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_period(
            datetime(2017, 12, 12, 21, 57, 13, tzinfo=pytz.UTC),
            datetime(2017, 12, 13, 22, 10, 56, tzinfo=pytz.UTC)
        )

        self.maxDiff = None
        self.assertEqual(expected_result, result)