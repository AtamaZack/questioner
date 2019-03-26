from django.contrib.auth.models import User
from django.db import models

from meetup.models import Meeting


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    meetups = models.ManyToManyField(
        Meeting,
        through='MeetingTag',
        related_name='rest_tags',
        through_fields=('tag', 'meetup'),
    )


class MeetingTag(models.Model):
    meetup = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("tag", "meetup")

    def __str__(self):
        return (self.tag)
