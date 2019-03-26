from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from meetup.models import Meeting
from question.models import Question


class TestQuestionViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(
            username="user1", email="user1@questioner.com", is_superuser=False
        )
        self.user2 = User.objects.create(
            username="user2", email="user2@questioner.com", is_superuser=False
        )
        self.admin = User.objects.create(
            username="admin",
            email="admin@questioner.com",
            is_staff=True,
            is_superuser=True,
        )
        self.meetup = Meeting.objects.create(
            title="Meetup title",
            date="2019-03-07",
            start="10:21:39",
            end="12:21:39",
            created_by=self.admin,
            created_at="2019-03-07 12:21:39",
        )
        self.qn_db = Question.objects.create(
            title=" QN Meetup title",
            body="2019-03-07",
            created_by=self.user1,
            meetup_id=self.meetup,
        )
        self.question = {
            "title": "Question 1 title",
            "body": "this is the body of question 1",
        }

        self.edit_qn_data = {
            "title": "Question 1 title - edited",
            "body": "this is the body of question 1",
        }

        self.question_missing_fields = {
            "body": "this is the body of question 1",
            "created_by": 1,
        }
        self.question_missing_title = {
            "body": "this is the body of question 1"
        }
        self.question_missing_body = {"title": "Question 1 title"}

    def test_other_users_can_upvote_on_a_question(self):
        self.client.force_authenticate(user=self.user2)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/upvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_invalid_question_upvote(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/1233/upvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_upvote_on_their_question(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/upvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_can_cancel_upvote(self):
        self.client.force_authenticate(user=self.user2)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/upvote/"
        self.client.get(
            url, content_type="application/json")
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_turn_downvote_to_upvote(self):
        self.client.force_authenticate(user=self.user2)

        url_1 = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/downvote/"
        url_2 = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/upvote/"
        self.client.get(
            url_1, content_type="application/json")
        response = self.client.get(
            url_2, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_downvote_on_their_question(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/downvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_other_users_can_downvote_on_a_question(self):
        self.client.force_authenticate(user=self.user2)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/downvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_invalid_question_downvote(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/1233/downvote/"
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_can_cancel_downvote(self):
        self.client.force_authenticate(user=self.user2)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/downvote/"
        self.client.get(
            url, content_type="application/json")
        response = self.client.get(
            url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_turn_upvote_to_downvote(self):
        self.client.force_authenticate(user=self.user2)

        url_1 = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/upvote/"
        url_2 = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/downvote/"
        self.client.get(
            url_1, content_type="application/json")
        response = self.client.get(
            url_2, content_type="application/json")
        self.assertEqual(response.status_code, 200)
