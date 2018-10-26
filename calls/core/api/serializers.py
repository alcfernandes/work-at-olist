from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from calls.core.models.call import CallDetail, Call
from calls.core.models.pricing_rule import PricingRule


class CallDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    def validate(self, data):

        if data['type'] == CallDetail.START and 'source' not in data:
            raise serializers.ValidationError("A start-type call detail record must have a source telephone number.")

        if data['type'] == CallDetail.START and 'destination' not in data:
            raise serializers.ValidationError("A start-type call detail record must have a destination telephone "
                                              "number.")

        if data['type'] == CallDetail.END and 'source' in data \
                and data['source'] is not None and data['source'] != "":
            raise serializers.ValidationError("A end-type call detail record should not have a source telephone number.")

        if data['type'] == CallDetail.END and 'destination' in data \
                and data['destination'] is not None and data['destination'] != "":
            raise serializers.ValidationError("A end-type call detail record should not have a destination telephone "
                                              "number.")

        if data['type'] == CallDetail.START and data['destination'] == data['source']:
            raise serializers.ValidationError("Source and destination telephone number must be different.")

        return data

    class Meta:
        model = CallDetail
        fields = (
            'url',
            'id',
            'type',
            'timestamp',
            'source',
            'destination',
            'call_id'
        )

        validators = [
            UniqueTogetherValidator(
                queryset=CallDetail.objects.all(),
                fields=('type', 'call_id'),
                message='A detail record with this type and call id has already been sent. Delete it before resend it.',
            )
        ]


class CallSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Call
        fields = (
            'url',
            'id',
            'detail_start',
            'detail_end',
            'duration',
            'price',

        )


class BillSerializer(serializers.ModelSerializer):
    destination = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    def get_destination(self, obj):
        return obj.detail_start.destination

    def get_start_date(self, obj):
        return obj.detail_start.timestamp.date()

    def get_start_time(self, obj):
        return obj.detail_start.timestamp.time()

    def get_duration(self, obj):
        return obj.duration

    class Meta:
        model = Call
        fields = [
            "destination",
            "start_date",
            "start_time",
            "duration",
            "price"
        ]


class PricingRuleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PricingRule
        fields = (
            'url',
            'id',
            'name',
            'start_time',
            'end_time',
            'standing_charge',
            'minute_call_charge'
        )
