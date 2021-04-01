import datetime, pytz, json

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_api_key.models import APIKey
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import (
    Promo
)
from .serializers import (
    PromoAdminUserSerializer,
    PromoNormalUserSerializerList,
    PromoNormalUserSerializerRetreive
)
from accounts.models import (
    AdministratorUser,
    NormalUser,
    User
)

class UserCreationTestCaseBase(APITestCase):
    def setUp(self):

        self.start_time = datetime.datetime(2021, 3, 31, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        self.end_time = datetime.datetime(2021, 5, 24, 20, 8, 7, 127325, tzinfo=pytz.UTC)

        admin_user_1, self.tkn_admin_user = self.create_admin_user()

        self.normal_user_1, self.tkn_normal_user_1 = self.create_normal_user(id=0)
        self.normal_user_1_promos = self.create_normal_user_promos(self.normal_user_1, start_id=0, end_id=5)

        self.normal_user_2, self.tkn_normal_user_2 = self.create_normal_user(id=1)
        self.normal_user_2_promos = self.create_normal_user_promos(self.normal_user_2, start_id=5, end_id=10)

        self.normal_user_3, self.tkn_normal_user_3 = self.create_normal_user(id=2)

    def create_admin_user(self):
        superuser_obj = User.objects.create_superuser(
            username='AdminUser',
            name='Test AdminUser Name',
            password='SomeStrongPassword'
        )
        admin_user = AdministratorUser.objects.create(
            user=superuser_obj,
            address='Some Address',
        )
        token = Token.objects.get(user=superuser_obj).key
        return admin_user, token

    def create_normal_user(self, id):
        user_obj = User.objects.create_user(
            username=f'NormalUser_{id}',
            name=f'Test NormalUser_{id} Name',
            password='SomeStrongPassword',
        )
        normal_user = NormalUser.objects.create(
            user=user_obj,
            address='Some Address',
            mobile_number='01234567891'
        )
        token = Token.objects.get(user=user_obj).key
        return normal_user, token

    def create_normal_user_promos(self, normal_user_obj, start_id, end_id):
        promos = []
        for index in range(start_id, end_id):
            promo = Promo.objects.create(
                normal_user=normal_user_obj,
                promo_code=f'SomePromoCode_{index}',
                promo_type=f'Some Type_{index}',
                promo_amount=100,
                description=f'Some Description_{index}',
                start_time=self.start_time,
                end_time=self.end_time,
                is_active=True
            )
            promos.append(promo)
        return promos

class PromoAdminUserTestCase(UserCreationTestCaseBase):

    def get_endpoint(self, action, obj_id_list=None):
        return reverse(
            f'promos:promo_admin_user-{action}',
            args=obj_id_list
        )

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    def authorize_admin_user(self, ):
        self.authenticate(self.tkn_admin_user)

    def authorize_normal_user_1(self):
        self.authenticate(self.tkn_normal_user_1)

    def revoke_authorization(self):
        self.client.force_authenticate(user=None)

    def test_success_list_authorized_admin_user(self):
        self.authorize_admin_user()
        response = self.client.get(
            self.get_endpoint('list')
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_fail_list_unauthorized(self):
        self.revoke_authorization()
        response = self.client.get(
            self.get_endpoint('list')
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_list_authorized_normal_user(self):
        self.authorize_normal_user_1()
        response = self.client.get(
            self.get_endpoint('list')
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def get_first_normal_user_1_promo_id(self):
        return self.normal_user_1_promos[0]

    def test_success_retreive_authorized_admin_user(self):
        self.authorize_admin_user()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.get(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_fail_retreive_unauthorized(self):
        self.revoke_authorization()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.get(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_retreive_authorized_normal_user(self):
        self.authorize_normal_user_1()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.get(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_success_patch_authorized_admin_user(self):
        self.authorize_admin_user()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        promo_type_before = obj.promo_type
        response = self.client.patch(
            self.get_endpoint('detail', [obj_id]),
            data={'promo_type': 'Promo Type Updated'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertNotEqual(
            response.data['promo_type'],
            promo_type_before
        )

    def test_fail_patch_unauthorized(self):
        self.revoke_authorization()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.patch(
            self.get_endpoint('detail', [obj_id]),
            data={'promo_type': 'Promo Type Updated'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_patch_authorized_normal_user(self):
        self.authorize_normal_user_1()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.patch(
            self.get_endpoint('detail', [obj_id]),
            data={'promo_type': 'Promo Type Updated'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_success_delete_authorized_admin_user(self):
        self.authorize_admin_user()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_fail_delete_unauthorized(self):
        self.revoke_authorization()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_delete_authorized_normal_user(self):
        self.authorize_normal_user_1()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def new_obj_data(self):
        return {
            'normal_user': self.normal_user_1.id,
            'promo_code': 'AdminCreatedPromoCode',
            'promo_type': 'Some Type',
            'promo_amount': 100,
            'description': 'Some Description',
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    def test_success_create_authorized_admin_user(self):
        self.authorize_admin_user()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id]),
            data=self.new_obj_data()
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_fail_create_unauthorized(self):
        self.revoke_authorization()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id]),
            data=self.new_obj_data()
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_fail_create_authorized_normal_user(self):
        self.authorize_normal_user_1()
        obj = self.get_first_normal_user_1_promo_id()
        obj_id = obj.id
        response = self.client.delete(
            self.get_endpoint('detail', [obj_id]),
            data=self.new_obj_data()
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )



class PromoNormalUserTestCase(UserCreationTestCaseBase):
    pass