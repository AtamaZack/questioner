from rest_framework import serializers

from .models import Answers


class AnswerSerializer(serializers.ModelSerializer):
    body = serializers.CharField(allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Answers

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("body", "meetup", "question"),
                message=("You cannot add a duplicate Answer."),
            )
        ]
        fields = "__all__"
