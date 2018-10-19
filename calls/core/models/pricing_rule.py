from decimal import Decimal
from datetime import time

from django.db import models

from calls.core.util.helpers import to_timedelta


class PricingRule(models.Model):

    class Meta:
        verbose_name = "pricing rule"
        verbose_name_plural = "pricing rules"

    name = models.CharField("name", max_length=80, unique=True)
    start_time = models.TimeField("start time")
    end_time = models.TimeField("end time (excluding)")
    standing_charge = models.DecimalField("standing charge", max_digits=6, decimal_places=2)
    minute_call_charge = models.DecimalField("call charge/minute", max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    @staticmethod
    def rules():
        """
        To facilitate the calculation of fares, it returns the charging rules by breaking time bands
        that pass from one day to another (eg 22:00 to 06:00), one for each day
        eg (22:00 to 06:00) => (22:00 to 23:59 and 00:00 to 06:00)
        """
        rules = PricingRule.objects.all()
        result = []

        for rule in rules:
            if rule.start_time > rule.end_time:
                result.append(
                    {
                        'start': rule.start_time,
                        'end': time(23, 59, 59),
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )

                result.append(
                    {
                        'start': time(0, 0, 0),
                        'end': rule.end_time,
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )
            else:
                result.append(
                    {
                        'start': rule.start_time,
                        'end': rule.end_time,
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )
        return result

    @staticmethod
    def prices_for_time_period(case_start, case_end):
        """
        Returns the tariffs for each portion of time according to price rules table

        :param case_start: Time Start
        :param case_end: Time End
        """
        result = []
        rules = PricingRule.rules()

        for rule in rules:

            rule_start, rule_end = rule['start'], rule['end']

            start = None
            end = None

            if case_end < rule_start or case_start >= rule_end:
                # The case is out of rule time box
                continue

            if case_start < rule_start and case_end < rule_end:
                # The case starts before and ends during rule time box
                start = rule_start
                end = case_end

            elif case_start < rule_start and case_end >= rule_end:
                # The case starts before and ends after rule time box
                start = rule_start
                end = rule_end

            elif case_start >= rule_start and case_end < rule_end:
                # The case starts and ends during rule time box
                start = case_start
                end = case_end

            elif case_start >= rule_start and case_end >= rule_end:
                # The case starts during and ends after rule time box
                start = case_start
                end = rule_end

            prices = {
                'pricing_rule_id': rule['id'],
                'minutes': (to_timedelta(end) - to_timedelta(start)).seconds // 60,
                'call_charge': (to_timedelta(end) - to_timedelta(start)).seconds // 60 * rule['minute_call_charge'],
                'standing_charge': rule['standing_charge']
            }

            result.append(prices)

        return result

    @staticmethod
    def price(start_timestamp, end_timestamp):
        prices = PricingRule.prices_for_time_period(start_timestamp.time(), end_timestamp.time())

        call_charge = Decimal('0.00')
        if prices:
            for price in prices:
                call_charge += price['call_charge']

            standing_charge = prices[0]['standing_charge']
            return call_charge + standing_charge
        else:
            return call_charge
