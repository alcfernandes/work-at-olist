from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.core.validators import ValidationError, MinLengthValidator

from calls.core.validators import phone_number_validator
from calls.core.util.helpers import time_between
from calls.core.models.pricing_rule import PricingRule


def call_detail_post_save_receiver(instance, *_args, **_kwargs):
    Call.update_detail(instance)


def call_detail_pre_delete_receiver(instance, *_args, **_kwargs):
    Call.delete_detail(instance)


class CallDetail(models.Model):

    class Meta:
        verbose_name = "call detail"
        verbose_name_plural = "calls details"
        unique_together = ("type", "call_id")

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
        validators=[phone_number_validator, MinLengthValidator(10)],
        null=True,
        blank=True,
    )
    destination = models.CharField(
        "destination phone number",
        max_length=11,
        validators=[phone_number_validator, MinLengthValidator(10)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Call id:{self.call_id} - Detail id:{self.id} - {self.type} on {self.timestamp} ' \
               f'from {self.source} to {self.destination}.'

    def save(self, *args, **kwargs):
        call = Call.objects.filter(id=self.call_id)

        if call and self.type == CallDetail.START \
                and call[0].detail_end \
                and call[0].detail_end.timestamp < self.timestamp:
            msg = "The Start Call Detail record must be before than the End Call Detail record"
            raise ValidationError(msg)

        if call and self.type == CallDetail.END \
                and call[0].detail_start \
                and call[0].detail_start.timestamp > self.timestamp:
            msg = "The End Call Detail record must be after than the Start Call Detail record"
            raise ValidationError(msg)

        super().save(*args, **kwargs)


post_save.connect(call_detail_post_save_receiver, sender=CallDetail)
pre_delete.connect(call_detail_pre_delete_receiver, sender=CallDetail)


def call_pre_save_receiver(instance, *_args, **_kwargs):
    instance.calculate_price()


class Call(models.Model):

    detail_start = models.ForeignKey(
        CallDetail,
        on_delete=models.SET_NULL,
        related_name="call_start",
        blank=True,
        null=True
    )
    detail_end = models.ForeignKey(
        CallDetail,
        on_delete=models.SET_NULL,
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
            return '0h0m0s'

        return time_between(self.detail_start.timestamp, self.detail_end.timestamp)

    def calculate_price(self):

        if not (self.detail_start and self.detail_end):
            self.price = Decimal('0.00')
            return

        self.price = PricingRule.price(self.detail_start.timestamp, self.detail_end.timestamp)

    @staticmethod
    def update_detail(call_detail):
        """
        Creates, updates the call record based on the call detail record
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

    @staticmethod
    def delete_detail(call_detail):
        """
        Delete/Update the call record based on the call detail record
        """
        if Call.objects.filter(id=call_detail.call_id).exists():
            call = Call.objects.get(id=call_detail.call_id)
            if ((call_detail.type == CallDetail.START) and call.detail_end is None) or ((call_detail.type == CallDetail.END) and call.detail_start is None):
                call.delete()
            else:
                if call_detail.type == CallDetail.START:
                    call.detail_start = None
                else:
                    call.detail_end = None

                call.save()


pre_save.connect(call_pre_save_receiver, sender=Call)
