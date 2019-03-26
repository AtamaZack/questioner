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
        return "{}".format(self.title)
