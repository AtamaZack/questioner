import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from meetup.models import Meeting
from question.models import Question, Comment

UserModel = get_user_model()

class APIUserAPITestCase(APITestCase):
    """Test suite for the comment API views."""

    @pytest.mark.django_db
    def setUp(self):
        """Define the test client and other test variables."""

        # Create user
        self.user = UserModel.objects.create(username='test')
        # Create superuser
        self.admin = UserModel.objects.create(username='admin', is_superuser=True)
        # Create meetup
        self.meetup = Meeting.objects.create(
            id=1, title='The Django Meetup', date='2019-03-07', start='10:21:39',
            end='12:21:39', created_by=self.admin, created_at='2019-03-07 12:21:39')
        # Add a new question to a meetup
        self.question = Question.objects.create(
            id=1, title='Question title', body='Question body', created_by=self.user,
            meetup_id=self.meetup)
        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class TestCommentList(APIUserAPITestCase):
    """Test suite for comment list."""

    @pytest.mark.django_db
    def test_get_comment_list(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(url, data, format="json")
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_get_comment_list_with_invalid_meetup(self):
        url = reverse('comment', kwargs={'meetup_id': 100, 'question_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Meetup not found.')

    @pytest.mark.django_db
    def test_get_comment_list_with_invalid_question(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Question not found.')

    @pytest.mark.django_db
    def test_post_a_comment(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'Comment successfully created.')

    @pytest.mark.django_db
    def test_post_a_comment_with_invalid_meetup(self):
        url = reverse('comment', kwargs={'meetup_id': 100, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Meetup not found.')

    @pytest.mark.django_db
    def test_post_a_comment_with_invalid_question(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 100})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Question not found.')

    @pytest.mark.django_db
    def test_post_a_comment_with_missing_field(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "question": 1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'],
                         'Fields cannot be left empty or missing.')


class TestCommentDetail(APIUserAPITestCase):
    """Test suite for comment detail."""

    @pytest.mark.django_db
    def test_get_a_single_comment(self):
        comment = Comment.objects.create(comment='Add more color',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_get_a_comment_with_invalid_meetup(self):
        comment = Comment.objects.create(comment='blemishes only',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 120, 'question_id': 1, 'pk': comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Meetup not found.')

    @pytest.mark.django_db
    def test_get_a_comment_with_invalid_question(self):
        comment = Comment.objects.create(comment='blemishes only',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 199, 'pk': comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Question not found.')

    @pytest.mark.django_db
    def test_get_a_missing_comment(self):
        url = reverse('comment', kwargs={'meetup_id': 1, 'question_id': 1})
        data = {
            "comment": "blabla....",
            "question": 1
        }
        self.client.post(url, data, format="json")
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.json()['error'], 'Comment not found.')

    @pytest.mark.django_db
    def test_update_a_comment(self):
        comment = Comment.objects.create(comment='uganda zabu',
                                         question=self.question, created_by=self.user)
        data = {"comment": "life is cool", "question": 1}
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': comment.id})
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Comment successfully updated.')

    @pytest.mark.django_db
    def test_update_a_comment_with_invalid_meetup(self):
        comment = Comment.objects.create(comment='what kind of qn is this?',
                                         question=self.question, created_by=self.user)
        data = {"comment": 'What kind of Qusetion is this?', "question": 1}
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 127, 'question_id': 1, 'pk': comment.id})
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Meetup not found.')

    @pytest.mark.django_db
    def test_update_a_comment_with_invalid_question(self):
        comment = Comment.objects.create(comment='blemishes only',
                                         question=self.question, created_by=self.user)
        data = {"comment": "life is cool", "question": 1}
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 211, 'pk': comment.id})
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Question not found.')

    @pytest.mark.django_db
    def test_delete_a_single_comment(self):
        comment = Comment.objects.create(comment='Question not clear',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 1, 'pk': comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    @pytest.mark.django_db
    def test_delete_a_comment_with_invalid_meetup(self):
        comment = Comment.objects.create(comment='blemishes only',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 100, 'question_id': 1, 'pk': comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Meetup not found.')

    @pytest.mark.django_db
    def test_delete_a_comment_with_invalid_question(self):
        comment = Comment.objects.create(comment='blemishes only',
                                         question=self.question, created_by=self.user)
        url = reverse('comment_detail',
                      kwargs={'meetup_id': 1, 'question_id': 100, 'pk': comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], 'Question not found.')
