from rest_framework import status
from rest_framework_api_key.models import APIKey
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import (
    AdministratorUser,
    NormalUser,
    User
)
from .serializers import (
    RegisterAdminUserSerializer,
    RegisterNormalUserSerializer
)


class RegisterAdminUserTestCase(APITestCase):

    endpoint = reverse('accounts:register_admin_user')
    user_data = {
        'username': 'TestAdmin1',
        'name': 'Test Admin1 Name',
        'password': 'password123',
        'password2': 'password123',
        'address': 'Some Address'
    }

    def setUp(self):
        # Create API Key for admin user registeration.
        api_key, key = APIKey.objects.create_key(name="admin_client_api_key")
        self.api_key = key
        self.api_authentication()

    def api_authentication(self):
        """
        Set the client API Key in the authorization headers.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key}')
        
    def test_success_register_admin_user(self):
        """
        Admin user succesful registration.
        """
        response = self.client.post(
            self.endpoint,
            data=self.user_data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_fail_register_admin_user_no_api_key(self):
        """
        Client doesn't send the API Key in the authorization headers,
        a 401 Unauthorized is returned.
        """
        self.client.force_authenticate(token=None)
        response = self.client.post(
            self.endpoint,
            data=self.user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_register_admin_user_without_body(self):
        """
        Client doesn't send the data in the request body,
        a 400 Bad Request is returned.
        """
        response = self.client.post(
            self.endpoint
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )



class RegisterNormalUserTestCase(APITestCase):

    endpoint = reverse('accounts:register_normal_user')
    user_data = {
        'username': 'TestNormalUser1',
        'name': 'Test NormalUser1 Name',
        'password': 'password123',
        'password2': 'password123',
        'address': 'Some Address',
        'mobile_number': '01234567891',
    }

    def test_success_register_normal_user(self):
        """
        Admin user succesful registration.
        """
        response = self.client.post(
            self.endpoint,
            data=self.user_data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_fail_register_normal_user_without_body(self):
        """
        Client doesn't send the data in the request body,
        a 400 Bad Request is returned.
        """
        response = self.client.post(
            self.endpoint
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class LoginAdminUserTestCase(APITestCase):
    endpoint = reverse('accounts:login')

    def setUp(self):
        """
        Create an auth account and assign it to the new
        created admin user.
        """
        self.user = User.objects.create_superuser(
            username='correct_username',
            name='Test Admin1 Name',
            password='correct_password',
        )
        self.admin_user = AdministratorUser.objects.create(
            user=self.user,
            address='Some Address'
        )

    def test_success_login_admin_user(self):
        user_data = {
            'username': 'correct_username',
            'password': 'correct_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_fail_login_admin_user_with_wrong_username(self):
        user_data = {
            'username': 'wrong_username',
            'password': 'correct_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_login_admin_user_with_wrong_password(self):
        user_data = {
            'username': 'correct_username',
            'password': 'wrong_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class LoginNormalUserTestCase(APITestCase):
    endpoint = reverse('accounts:login')

    def setUp(self):
        """
        Create an auth account and assign it to the new
        created normal user.
        """
        self.user = User.objects.create_user(
            username='correct_username',
            name='Test NormalUser1 Name',
            password='correct_password'
        )
        self.normal_user = NormalUser.objects.create(
            user=self.user,
            address='Some Address',
            mobile_number='01234567891'
        )

    def test_success_login_normal_user(self):
        user_data = {
            'username': 'correct_username',
            'password': 'correct_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_fail_login_normal_user_with_wrong_username(self):
        user_data = {
            'username': 'wrong_username',
            'password': 'correct_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_fail_login_normal_user_with_wrong_password(self):
        user_data = {
            'username': 'correct_username',
            'password': 'wrong_password'
        }
        response = self.client.post(
            self.endpoint,
            user_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )