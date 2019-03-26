from rest_framework import serializers
from question.models import Question
from vote.serializers import VoteSerializer
from comment.serializers import CommentSerializer


class QuestionSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("created_by", "meetup_id", "delete_status", )
