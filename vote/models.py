from django.contrib.auth.models import User
from django.db import models

from question.models import Question


class Vote(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    voter_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField()
    date_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.voter_id, self.vote)  # pragma: no cover
