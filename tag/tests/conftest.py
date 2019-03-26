import pytest

from tag.models import Tag, MeetingTag


@pytest.mark.django_db
@pytest.fixture
def tag_objs(admin_user):
    tags = []
    for tag in ["sports", "Django", "API"]:
        tags.append(Tag.objects.create(title=tag, created_by=admin_user))
    return tags


@pytest.mark.django_db
@pytest.fixture
def disabled_tag(admin_user):
    return Tag.objects.create(
        title="Javascript", created_by=admin_user, active=False
    )


@pytest.mark.django_db
@pytest.fixture
def meetup_tag(user1, a_tag, meetup1):
    return MeetingTag.objects.create(
        meetup=meetup1, tag=a_tag, created_by=user1
    )
