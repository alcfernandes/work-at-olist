from django.db import models

from calls.core.validators import phone_number_validator


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
