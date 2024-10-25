from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser',
                          password='testpassword')  # Log in the user

    def test_update_user_profile(self):
        url = reverse('user-profile')  # Use the name defined in urls.py
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.put(url, data, format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the user data was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_update_user_profile_invalid_data(self):
        url = reverse('user-profile')
        data = {
            'username': '',  # Invalid username
            'email': 'not-an-email',  # Invalid email
        }
        response = self.client.put(url, data, format='json')

        # Check that the response is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
