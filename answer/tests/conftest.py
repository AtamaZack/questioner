import pytest

from answer.models import Answers
from meetup.models import Meeting
from question.models import Question


@pytest.mark.django_db
@pytest.fixture
def question1(user1, meetup1):
    return Question.objects.create(
        title=" QN Meetup title",
        body="2019-03-07",
        created_by=user1,
        meetup_id=meetup1,
    )


@pytest.mark.django_db
@pytest.fixture
def meetup1(admin_user):
    return Meeting.objects.create(
        title="The Django Meetup",
        body="The Django meetup description",
        date="2019-03-07",
        start="10:21:39",
        end="12:21:39",
        created_by=admin_user,
        created_at="2019-03-07 12:21:39",
    )


@pytest.mark.django_db
@pytest.fixture
def answered_question(staff1, question1, meetup1):
    return Answers.objects.create(
        body="Django is a Python framework",
        created_by=staff1,
        meetup=meetup1,
        question=question1,
    )
