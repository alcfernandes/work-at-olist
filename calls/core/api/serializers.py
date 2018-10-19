from rest_framework import serializers

from calls.core.models.call import CallDetail


class CallDetailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    def validate(self, data):
        if data['type'] == CallDetail.START and 'source' not in data:
            raise serializers.ValidationError("A start-type call detail record must have a source telephone number.")

        if data['type'] == CallDetail.START and 'destination' not in data:
            raise serializers.ValidationError("A start-type call detail record must have a destination telephone "
                                              "number.")

        if data['type'] == CallDetail.END and 'source' in data:
            raise serializers.ValidationError("A end-type call detail record should not have a source telephone number.")

        if data['type'] == CallDetail.END and 'destination' in data:
            raise serializers.ValidationError("A end-type call detail record should not have a destination telephone "
                                              "number.")
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
