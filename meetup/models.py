from django.contrib.auth.models import User
from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    date = models.DateField(null=False)
    start = models.TimeField()
    end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return (self.title)
