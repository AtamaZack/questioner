from rest_framework import serializers

from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ["created_by"]
