from rest_framework import serializers
from question.models import Question, Comment, Mycomment
from vote.serializers import VoteSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Map the comment model instance into JSON format."""

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        """Map serializer fields to comment model fields."""
        model = Comment
        fields = "__all__"


class CommentSerializerclass(serializers.ModelSerializer):
    class Meta:
        model = Mycomment
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuestionSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ["created_by", "meetup_id", "delete_status"]
