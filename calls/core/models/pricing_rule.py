from decimal import Decimal
from datetime import time, datetime, timedelta
import pytz

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
    def map_day_time_rules():

        rules = PricingRule.objects.all()
        result = []

        for rule in rules:
            if rule.start_time > rule.end_time:
                result.append(
                    {
                        'start_time': rule.start_time,
                        'end_time': time(0, 0, 0),
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )

                result.append(
                    {
                        'start_time': time(0, 0, 0),
                        'end_time': rule.end_time,
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )
            else:
                result.append(
                    {
                        'start_time': rule.start_time,
                        'end_time': rule.end_time,
                        'id': rule.id,
                        'standing_charge': rule.standing_charge,
                        'minute_call_charge': rule.minute_call_charge,
                    }
                )
        return result

    @staticmethod
    def prices_for_period(case_start, case_end):
        prices = []

        rules = PricingRule.map_day_time_rules()

        if not rules:
            return []

        start = case_start

        # Find the rule that mach with start point
        for idx, rule in enumerate(rules):
            if (rule['start_time'] <= start.time() < rule['end_time']) or \
                    (rule['start_time'] <= start.time() and rule['end_time'] == time(0, 0, 0)):
                break

        while True:
            slice_start_datetime = start

            slice_end_date = slice_start_datetime.date()
            if rule['end_time'] == time(0, 0, 0):
                slice_end_date += timedelta(days=1)

            slice_end_datetime = datetime(
                slice_end_date.year,
                slice_end_date.month,
                slice_end_date.day,
                rule['end_time'].hour,
                rule['end_time'].minute,
                rule['end_time'].second,
                tzinfo=pytz.UTC
            )

            if slice_end_datetime > case_end:
                slice_end_datetime = case_end

            slice_time_price = {
                'pricing_rule_id': rule['id'],
                'start_datetime': slice_start_datetime,
                'end_datetime': slice_end_datetime,
                'minutes': (to_timedelta(slice_end_datetime) - to_timedelta(slice_start_datetime)).seconds // 60,
                'call_charge': (to_timedelta(slice_end_datetime) - to_timedelta(slice_start_datetime)).seconds // 60 * rule['minute_call_charge'],
                'standing_charge': rule['standing_charge']
            }

            prices.append(slice_time_price)

            if slice_end_datetime == case_end:
                break

            start = slice_end_datetime

            if idx == len(rules)-1:
                idx = 0
            else:
                idx += 1

            rule = rules[idx]

        return prices

    @staticmethod
    def price(start_timestamp, end_timestamp):
        prices = PricingRule.prices_for_period(start_timestamp, end_timestamp)

        call_charge = Decimal('0.00')
        if prices:
            for price in prices:
                call_charge += price['call_charge']

            standing_charge = prices[0]['standing_charge']
            return call_charge + standing_charge
        else:
            return call_charge
