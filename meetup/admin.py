from django.contrib import admin

from .models import Meeting
from .models import MeetingTag
from .models import Tag

admin.site.register(Meeting)
admin.site.register(Tag)
admin.site.register(MeetingTag)
