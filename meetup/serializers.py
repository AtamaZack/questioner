from rest_framework import serializers
from .models import Meeting
from tag.models import Tag


class TagsListingField(serializers.RelatedField):
    @classmethod
    def to_representation(cls, value, queryset=Tag.objects.all()):
        return value.title


class MeetingSerializer(serializers.ModelSerializer):
    rest_tags = TagsListingField(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = "__all__"
        read_only_fields = ("created_by",)
