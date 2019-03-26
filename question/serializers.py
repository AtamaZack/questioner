from rest_framework import serializers
from question.models import Question, Comment
from vote.serializers import VoteSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Map the comment model instance into JSON format."""
    class Meta:
        """Map serializer fields to comment model fields."""
        model = Comment
        fields = "__all__"
        read_only_fields = ("created_by", "question", )


class QuestionSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("created_by", "meetup_id", "delete_status", )
