from decimal import Decimal
from datetime import time

from django.db import models
from django.db.models.signals import post_save, pre_save

from calls.core.validators import phone_number_validator
from calls.core.util.helpers import time_between, to_timedelta


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


def call_detail_post_save_receiver(instance, *_args, **_kwargs):
    Call.update(instance)


class CallDetail(models.Model):

    class Meta:
        verbose_name = "call detail"
        verbose_name_plural = "calls details"

    # Record Type
    START = 'start'
    END = 'end'
    TYPES_CHOICES = (
        (START, "Call Start"),
        (END, "Call End"),
    )

    type = models.CharField("record type", max_length=5, choices=TYPES_CHOICES)
    timestamp = models.DateTimeField()
    call_id = models.PositiveIntegerField()
    source = models.CharField(
        "source phone number",
        max_length=11,
        validators=[phone_number_validator],
        null=True,
        blank=True,
    )
    destination = models.CharField(
        "destination phone number",
        max_length=11,
        validators=[phone_number_validator],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Call id:{self.call_id} - Detail id:{self.id} - {self.type} on {self.timestamp} ' \
               f'from {self.source} to {self.destination}.'


post_save.connect(call_detail_post_save_receiver, sender=CallDetail)


def call_pre_save_receiver(instance, *_args, **_kwargs):
    instance.calculate_price()


class Call(models.Model):

    detail_start = models.ForeignKey(
        CallDetail,
        on_delete=models.CASCADE,
        related_name="call_start",
        blank=True,
        null=True
    )
    detail_end = models.ForeignKey(
        CallDetail,
        on_delete=models.CASCADE,
        related_name="call_end",
        blank=True,
        null=True
    )

    price = models.DecimalField("standing charge", max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'Call {self.id}'

    @property
    def duration(self):
        if not (self.detail_start and self.detail_end):
            return {'hours': 0, 'minutes': 0, 'seconds': 0}

        return time_between(self.detail_start.timestamp, self.detail_end.timestamp)

    def calculate_price(self):
        if not (self.detail_start and self.detail_end):
            self.price = Decimal('0.00')
            return

        self.price = PricingRule.price(self.detail_start.timestamp, self.detail_end.timestamp)

    @staticmethod
    def update(call_detail):
        """
        Creates or updates the call record based on the call detail record
        """

        if not Call.objects.filter(id=call_detail.call_id).exists():
            Call.objects.create(
                id=call_detail.call_id,
                detail_start=call_detail if call_detail.type == CallDetail.START else None,
                detail_end=call_detail if call_detail.type == CallDetail.END else None,
            )
        else:
            call = Call.objects.get(id=call_detail.call_id)
            if call_detail.type == CallDetail.START:
                call.detail_start = call_detail
            else:
                call.detail_end = call_detail
            call.save()


pre_save.connect(call_pre_save_receiver, sender=Call)
