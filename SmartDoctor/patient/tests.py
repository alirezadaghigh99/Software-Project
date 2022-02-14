from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from SmartDoctor.patient.models import UserModel, UserRole


class LoginAndSignupTest(APITestCase):
    signup_url = reverse('patient:signup')
    visit_list_url = reverse('doctor:visit-request-list')

    def setUp(self) -> None:
        self.data = {'username': "patient1", 'role': UserRole.PATIENT, 'first_name': "patient",
                     'last_name': "patient_zadeh", 'password1': '123456', 'password2': '123456'}
        self.data_wrong = {'username': "patient1", 'role': UserRole.PATIENT, 'first_name': "patient",
                           'last_name': "patient_zadeh", 'password1': '123456', 'password2': '1234567'}
        self.data_wrong_username = {'username': "p1", 'role': UserRole.PATIENT, 'first_name': "patient",
                                    'last_name': "patient_zadeh", 'password1': '123456', 'password2': '1234567'}

        self.p1 = UserModel.objects.create(username="p1", role=UserRole.PATIENT, first_name="test",
                                           last_name="test2")
        self.p1.set_password("123456")
        self.p1.save()
        self.client = APIClient()

    def test_signup_success(self):
        response = self.client.post(self.signup_url,
                                    data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_failure_wrong_same_password(self):
        response = self.client.post(self.signup_url,
                                    data=self.data_wrong_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


