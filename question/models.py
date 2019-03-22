from django.contrib.auth.models import User
from django.db import models

from meetup.models import Meeting


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now_add=True)
    meetup_id = models.ForeignKey(
        Meeting, on_delete=models.CASCADE)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return (self.title, self.body)  # pragma: no cover

class Comment(models.Model):
    """This class represents the comment model."""

    question = models.ForeignKey(Question, related_name='comments',
                                 on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(User, related_name='comments',
                                   on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable representation of the comment model instance."""
        return (self.comment)


class Mycomment(models.Model):
    comment = models.TextField()
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
