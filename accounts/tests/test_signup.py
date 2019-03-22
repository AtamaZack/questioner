from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestSignup(APITestCase):
    def test_signup_with_wrong_email(self):
        """
        Ensure we cannot signup with wrong email.
        """
        data = {"username": "bison", "password": "12345", "email": "biso.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'], [
            "Enter a valid email address."
        ])

    def test_get_profile(self):
        """
        Ensure we can logout.
        """

        data = User.objects.create(
            username="user1", email="user1@questioner.com", is_superuser=False)
        self.client.force_authenticate(user=data)

        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'][0]['user'], {
            'Username': 'user1', 'Email': 'user1@questioner.com'
        })

    def test_signup_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        data = {"username": "bisonlou", "password": "Pa$$word123",
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data'][0], {
            'username': 'bisonlou',
            'email': 'bisonlou@gmail.com',
            'is_admin': False}
        )

    def test_signup_user_with_short_password(self):
        """
        Ensure user cannot signup with a password shorter than 8 chars.
        """
        data = {"username": "bisonlou", "password": "123",
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_signup_user_with_common_password(self):
        """
        Ensure user cannot signup with a password
        similar to his username or among common passwords.
        """
        data = {"username": "bisonlou", "password": 'bison',
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_signup_user_with_short_password(self):
        """
        Ensure user cannot signup with a password shorter than 8 chars.
        """
        data = {"username": "bisonlou", "password": "123",
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_signup_user_with_common_password(self):
        """
        Ensure user cannot signup with a password
        similar to his username or among common passwords.
        """
        data = {"username": "bisonlou", "password": 'bison',
                "email": "bisonlou@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_signup_duplicate_user_with_valid_data(self):
        """
        Ensure user can sign up with valid data.
        """
        self.superuser = User.objects.create_superuser(
            "user1", "kalulearthur@gmail.com", "Pa$$word123"
        )
        data = {"username": "user1", "password": "Pa$$word123",
                "email": "kalulearthur@gmail.com"}
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors']['email'], [
                         'email already in use'])
        self.assertEqual(response.data['errors']['username'], [
                         'username already in use'])
