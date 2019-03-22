from rest_framework import serializers
from .models import MeetingTag
from .models import Tag


class MeetingTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTag

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('tag', 'meetup'),
                message=("Tag already exists on meet up.")
            )
        ]

        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["created_by", "active"]


class MeetingTagSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = MeetingTag

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('tag', 'meetup'),
                message=("Tag already exists on meet up.")
            )
        ]

        fields = "__all__"
        read_only_fields = ["created_by"]
