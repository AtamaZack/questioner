import json

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

    def test_admin_cannot_add_a_question(self):
        self.client.force_authenticate(user=self.admin)

        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["error"], "Admin is not allowed to add questions"
        )

    def test_anonymous_user_cannot_add_a_question(self):
        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_user_cannot_add_a_question_with_missing_data(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/"
        response1 = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_title),
        )

        response2 = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_body),
        )

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response1.data["title"][0], "This field is required.")

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.data["body"][0], "This field is required.")

    def test_user_cannot_add_a_question_to_invalid_meetup(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/1212/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 400)

    def test_user_can_add_a_question(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.post(
            url,
            content_type="application/json",
            data=json.dumps(self.question),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["data"][0]["success"],
            "Question successfully added to meetup",
        )
        self.assertEqual(
            response.data["data"][0]["question"]["meetup_id"], self.meetup.id
        )
        self.assertEqual(
            response.data["data"][0]["question"]["created_by"], self.user1.id
        )
        self.assertEqual(
            response.data["data"][0]["question"]["title"],
            self.question["title"],
        )
        self.assertEqual(
            response.data["data"][0]["question"]["body"], self.question["body"]
        )

    def test_user_can_get_a_question_with_invalid_id(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_user_cannot_get_a_question_with_invalid_meetup(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/1234/questions/{int(self.qn_db.id)}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_user_can_get_a_question(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{self.meetup.id}/questions/{self.qn_db.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"][0]["question"]["title"], self.qn_db.title
        )
        self.assertEqual(
            response.data["data"][0]["question"]["body"], self.qn_db.body
        )

    def test_user_cannot_get_invalid_meetup_questions(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/1232/questions/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_user_can_get_meetup_questions(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/meetups/{self.meetup.id}/questions/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_a_question_wrong_id(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/meetings/{self.meetup.id}/questions/{74}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_admin_cannot_update_a_question(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"
        response = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.edit_qn_data),
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data,
            {
                "error": "Admin is not allowed to update a question",
                "status": 401,
            },
        )

    def test_editing_a_question_invlid_meetup(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/meetups/1234/questions/{int(self.qn_db.id)}/"
        response = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.edit_qn_data),
        )
        self.assertEqual(response.status_code, 400)

    def test_editing_a_question_not_question_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"
        response = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.edit_qn_data),
        )
        self.assertEqual(response.status_code, 401)

    def test_editing_a_question(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/meetups/{self.meetup.id}/questions/{self.qn_db.id}/"
        response = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.edit_qn_data),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["data"][0]["success"], "Question successfully edited"
        )
        self.assertEqual(
            response.data["data"][0]["question"]["title"],
            self.edit_qn_data["title"],
        )
        self.assertEqual(
            response.data["data"][0]["question"]["body"],
            self.edit_qn_data["body"],
        )

    def test_editing_a_question_missing_title(self):
        self.client.force_authenticate(user=self.user1)

        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"

        response1 = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_title),
        )

        response2 = self.client.put(
            url,
            content_type="application/json",
            data=json.dumps(self.question_missing_body),
        )

        self.assertEqual(response1.status_code, 400)
    
    def test_user_cannot_delete_question_created_by_another_user(self):
        self.client.force_authenticate(user=self.user2)
        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["error"],
            "You cannot delete question created by another user",
        )

    def test_user_cannot_delete_question_with_invalid_meetup(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/meetups/1234/questions/{int(self.qn_db.id)}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_user_can_delete_question_created_by_them(self):
        self.client.force_authenticate(user=self.user1)
        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"

        response = self.client.delete(url)
        self.assertEqual(
            response.data,
            {
                "status": 200,
                "data": [{"success": "Question has been deleted"}],
            },
        )

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.qn_db.id)

    def test_admin_soft_delete_a_question(self):
        self.client.force_authenticate(user=self.admin)
        url = f"/meetups/{int(self.qn_db.meetup_id.id)}/questions/{int(self.qn_db.id)}/"

        response = self.client.delete(url)
        self.assertEqual(
            response.data["data"][0],
            {"status": 200, "success": "Question has been soft deleted"},
        )

        self.qn_details = Question.objects.get(id=self.qn_db.id)
        self.assertEqual(self.qn_details.id, self.qn_db.id)
        self.assertTrue(self.qn_details.delete_status)
        self.assertEqual(self.qn_details.title, self.qn_db.title)
        