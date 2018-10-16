from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save, pre_save

from calls.core.validators import phone_number_validator
from calls.core.util.helpers import time_between


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
    def price(start_timestamp, end_timestamp):
        return Decimal('0.54')


def call_detail_post_save_receiver(instance, *_args, **_kwargs):
    call_detail = instance

    if not Call.objects.filter(id=call_detail.call_id).exists():
        Call.objects.create(
            id=call_detail.call_id,
            detail_start=instance if instance.type == CallDetail.START else None,
            detail_end=instance if instance.type == CallDetail.END else None,
        )
    else:
        call = Call.objects.get(id=call_detail.call_id)
        if instance.type == CallDetail.START:
            call.detail_start = instance
        else:
            call.detail_end = instance
        call.save()


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

    def duration(self):
        if not (self.detail_start and self.detail_end):
            return {'hours': 0, 'minutes': 0, 'seconds': 0}

        return time_between(self.detail_start.timestamp, self.detail_end.timestamp)

    def calculate_price(self):
        if not (self.detail_start and self.detail_end):
            self.price = Decimal('0.00')
            return

        self.price = PricingRule.price(self.detail_start.timestamp, self.detail_end.timestamp)


pre_save.connect(call_pre_save_receiver, sender=Call)
