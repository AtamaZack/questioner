from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase


class TestUserListing(APITestCase):
    def test_succesful_user_listing(self):
        """
        Ensure admin can get all users
        """
        admin = User.objects.create(
            username="admin",
            email="admin@questioner.com",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_authenticate(user=admin)

        url = reverse("users")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)

    def test_get_user_listing_as_non_admin(self):
        """
        Ensure we cannot get the user listing as non admins
        """

        user = User.objects.create(
            username="admin",
            email="admin@questioner.com",
            is_staff=False,
            is_superuser=False,
        )
        self.client.force_authenticate(user=user)

        url = reverse("users")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 403)
