from rest_framework import serializers

from calls.core.models import CallDetail


class CallDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

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
