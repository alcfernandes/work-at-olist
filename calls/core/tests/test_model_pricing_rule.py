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
