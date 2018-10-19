from decimal import Decimal

from datetime import time

from django.test import TestCase


from calls.core.models import PricingRule


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


class PrincesForTimePeriodMethodTest(TestCase):
    """
    Given an initial start time and end time, the method 'prices_for_time_period' must return
    the tariff corresponding to each period of time registered in the rules of prices.
    """
    def setUp(self):
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

    def test_prices_for_time_period_method_case_1(self):
        """
        Case 1: 21:57:13 to 22:17:53 | Starts on Standard tariff. Ends on Reduced tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'minutes': 2,
                'call_charge': Decimal('0.18'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'minutes': 17,
                'call_charge': Decimal('0.17'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_time_period(time(21, 57, 13), time(22, 17, 53))

        self.assertEqual(expected_result, result)

    def test_prices_for_time_period_method_case_2(self):
        """
        Case 2: 5:58:00 to 06:05:00 | Starts on Reduced tariff. Ends on Standard tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'minutes': 5,
                'call_charge': Decimal('0.45'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'minutes': 2,
                'call_charge': Decimal('0.02'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_time_period(time(5, 58, 00), time(6, 5, 0))

        self.assertEqual(expected_result, result)

    def test_prices_for_time_period_method_case_3(self):
        """
        Case 3: 06:10:05 to 06:20:57 | Starts on Standard tariff. Ends on Standard tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'minutes': 10,
                'call_charge': Decimal('0.90'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_time_period(time(6, 10, 5), time(6, 20, 57))

        self.assertEqual(expected_result, result)

    def test_prices_for_time_period_method_case_4(self):
        """
        Case 4: 22:00:00 to 22:10:33 | Starts on Reduced tariff. Ends on Reduced tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 2,
                'minutes': 10,
                'call_charge': Decimal('0.10'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_time_period(time(22, 0, 0), time(22, 10, 33))

        self.assertEqual(expected_result, result)

    def test_prices_for_time_period_method_case_5(self):
        """
        Case 5: 21:59:59 to 22:00:00 | Test ranges limits and zero tariff.
        """

        expected_result = [
            {
                'pricing_rule_id': 1,
                'minutes': 0,
                'call_charge': Decimal('0.00'),
                'standing_charge': Decimal('0.36')
            },
            {
                'pricing_rule_id': 2,
                'minutes': 0,
                'call_charge': Decimal('0.00'),
                'standing_charge': Decimal('0.36')
            },
        ]

        result = PricingRule.prices_for_time_period(time(21, 59, 59), time(22, 0, 0))

        self.assertEqual(expected_result, result)


class RulesMethodTest(TestCase):
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
                'start': time(6, 0, 0),
                'end': time(22, 0, 0),
                'id': 1,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.09'),
            },
            {
                'start': time(22, 0, 0),
                'end': time(23, 59, 59),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
            {
                'start': time(0, 0, 0),
                'end': time(6, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
        ]

        result = PricingRule.rules()

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
                'start': time(0, 0, 0),
                'end': time(18, 0, 0),
                'id': 1,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.09'),
            },
            {
                'start': time(18, 0, 0),
                'end': time(23, 59, 59),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
            {
                'start': time(0, 0, 0),
                'end': time(0, 0, 0),
                'id': 2,
                'standing_charge': Decimal('0.36'),
                'minute_call_charge': Decimal('0.01'),
            },
        ]

        result = PricingRule.rules()

        self.assertEqual(expected_result, result)

