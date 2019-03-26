from django.contrib.auth.models import User
from django.db import models

from meetup.models import Meeting
from question.models import Question


class Answers(models.Model):
    """Answers Model."""

    body = models.TextField(null=False, blank=False)
    meetup = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, to_field="username"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("body", "question", "meetup")

    def __str__(self):
        return f"{self.body}"
