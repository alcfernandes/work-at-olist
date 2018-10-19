from django.contrib import admin

from .models import PricingRule


@admin.register(PricingRule)
class PricingRuleModelAdmin(admin.ModelAdmin):

    save_on_top = True

    list_display = [
        'name',
        'start_time',
        'end_time',
        'standing_charge',
        'minute_call_charge',
    ]

    list_display_links = ["name"]

    list_filter = ["name"]

    search_fields = ["name"]

