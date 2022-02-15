from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from patient.models import UserModel, UserRole, Visit, VisitStatus


class LoginAndSignupTest(APITestCase):
    signup_url = reverse('patient_new:signup')
    login_url = reverse('patient_new:login')
    doctor_list_url = reverse('patient_new:doctor-list')

    def setUp(self) -> None:
        self.patient_1 = UserModel.objects.create(username="patient_1", role=UserRole.PATIENT, first_name="patient",
                                                     last_name="patient_zadeh")
        self.patient_1.set_password("123456")
        self.patient_1.save()

        self.client = APIClient()

    def test_signup_password_error(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.post(self.signup_url,
                                    data={'username': 'patient_3', 'first_name': 'test', 'last_name': 'test2',
                                          'password1': '123456', 'password2':'1234567'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_Duplicate_User(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.post(self.signup_url,
                                    data={'username': 'patient_1', 'first_name': 'test', 'last_name': 'test2',
                                          'password1': '123456', 'password2':'123456'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_password(self):
        """
            tests if a user can login with valid password
        """
        response = self.client.post(self.login_url, data={'username': 'patient_1', 'password': '123456'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_password(self):
        """
            tests if a user can login with valid password
        """
        response = self.client.post(self.login_url, data={'username': 'patient_1', 'password': '111111'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.doctor_list_url)
        """
            should redirect to login page
        """
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class DoctorListTest(APITestCase):
    doctor_list_url = reverse('patient_new:doctor-list')

    def setUp(self) -> None:
        self.patient = UserModel.objects.create(username="p3", role=UserRole.PATIENT, first_name="test",
                                                    last_name="test2")
        self.patient.set_password("123456")
        self.patient.save()


        self.client = APIClient()
        self.client.login(username='p3', password='123456')
        self.client.force_authenticate(user=self.patient)

    def test_visit_list_success(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_visit_list_fail_for_unauthenticated_user(self):
        """
        tests if a unauthenticated user can NOT access the list
        """
        self.client.logout()
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

