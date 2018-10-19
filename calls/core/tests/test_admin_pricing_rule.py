from django.test import TestCase
from django.contrib import admin

from calls.core.models.pricing_rule import PricingRule
from calls.core.admin import PricingRuleModelAdmin


class PricingRuleAdminTest(TestCase):
    """
    It should allow maintenance of the price rule table by Django admin
    """
    def setUp(self):
        self.model_admin = PricingRuleModelAdmin(PricingRule, admin.site)

    def test_pricing_rule_admin_registered(self):
        """ PricingRule class must be registered on admin"""
        # pylint: disable=W0212
        self.assertTrue(admin.site._registry[PricingRule])

    def test_list_display_fields(self):
        """ Django admin should display certain fields of price rule table in the browser."""
        fields_expected = [
            'name',
            'start_time',
            'end_time',
            'standing_charge',
            'minute_call_charge',
        ]

        for field in fields_expected:
            with self.subTest():
                self.assertIn(field, self.model_admin.list_display)

    def test_lts_filter(self):
        """ Must have certain filters"""
        fields_expected = ['name']
        for field in fields_expected:
            with self.subTest():
                self.assertIn(field, self.model_admin.list_filter)



