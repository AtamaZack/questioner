from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Map the comment model instance into JSON format."""

    created_by = serializers.ReadOnlyField(source='created_by.username')
    # question_name = serializers.ReadOnlyField(source='question.title')

    class Meta:
        """Map serializer fields to comment model fields."""
        model = Comment
        fields = "__all__"
        # read_only_fields = ("created_by_name", "question_name", )
