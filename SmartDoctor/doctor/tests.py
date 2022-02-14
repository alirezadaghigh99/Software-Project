# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from patient.models import UserModel, UserRole, Visit, VisitStatus


class VisitListTest(APITestCase):
    visit_list_url = reverse('doctor:visit-request-list')

    def setUp(self) -> None:
        self.doctor_user = UserModel.objects.create(username="doctor_user", role=UserRole.DOCTOR, first_name="test",
                                                    last_name="test2")
        self.doctor_user.set_password("123456")
        self.doctor_user.save()

        self.client = APIClient()
        self.client.login(username='doctor_user', password='123456')
        self.client.force_authenticate(user=self.doctor_user)

    def test_visit_list_success(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.get(self.visit_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_visit_list_fail_for_unauthenticated_user(self):
        """
        tests if a unauthenticated user can NOT access the list
        """
        self.client.logout()
        response = self.client.get(self.visit_list_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class VisitAcceptOrReject(APITestCase):
    @staticmethod
    def visit_accept_reject_url_func(visit_id, accept):
        return reverse('doctor:accept-reject-visit', args=(visit_id, accept))

    def setUp(self) -> None:
        self.doctor_user = UserModel.objects.create(username="doctor_user", role=UserRole.DOCTOR, first_name="test",
                                                    last_name="test2")
        self.doctor_user.set_password("123456")
        self.doctor_user.save()

        self.patient_user = UserModel.objects.create(username="patient_user", role=UserRole.DOCTOR, first_name="test",
                                                     last_name="test2")
        self.patient_user.set_password("123456")
        self.patient_user.save()

        self.visit1 = Visit.objects.create(doctor=self.doctor_user, patient=self.patient_user,
                                           status=VisitStatus.PENDING, time=timezone.now())
        self.visit2 = Visit.objects.create(doctor=self.doctor_user, patient=self.patient_user,
                                           status=VisitStatus.PENDING, time=timezone.now())

        self.client = APIClient()
        login = self.client.login(username='doctor_user', password='123456')
        if not login:
            raise Exception("can not login with provided credential!")
        # self.client.force_authenticate(user=self.doctor_user)

    def test_accept_success(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.get(self.visit_accept_reject_url_func(self.visit1.id, 1))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Visit.objects.get(pk=self.visit1.id).status == VisitStatus.ACCEPT)

    def test_accept_for_unauthenticated_user(self):
        """
        tests if a unauthenticated user can NOT access the list
        """
        self.client.logout()
        response = self.client.get(self.visit_accept_reject_url_func(self.visit1.id, 1))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Visit.objects.get(pk=self.visit1.id).status == VisitStatus.PENDING)

    def test_reject_success(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.get(self.visit_accept_reject_url_func(self.visit1.id, 0))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Visit.objects.get(pk=self.visit1.id).status == VisitStatus.REJECT)

    def test_reject_for_unauthenticated_user(self):
        """
        tests if a unauthenticated user can NOT access the list
        """
        self.client.logout()
        response = self.client.get(self.visit_accept_reject_url_func(self.visit1.id, 0))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Visit.objects.get(pk=self.visit1.id).status == VisitStatus.PENDING)


class LoginAndSignupTest(APITestCase):
    signup_url = reverse('doctor:signup')
    login_url = reverse('doctor:login')
    visit_list_url = reverse('doctor:visit-request-list')

    def setUp(self) -> None:
        self.doctor_user1 = UserModel.objects.create(username="doctor_user2", role=UserRole.DOCTOR, first_name="test",
                                                     last_name="test2")
        self.doctor_user1.set_password("123456")
        self.doctor_user1.save()

        self.client = APIClient()

    def test_signup(self):
        """
        tests if a authenticated user can access the visit list
        """
        response = self.client.post(self.signup_url,
                                    data={'username': 'doctor_user', 'first_name': 'test', 'last_name': 'test2',
                                          'password': '123456'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(UserModel.objects.filter(username='doctor_user', first_name='test', last_name='test2').exists())
        self.assertTrue(self.client.login(username='doctor_user', password='123456'))

    def test_login_valid_password(self):
        """
            tests if a user can login with valid password
        """
        response = self.client.post(self.login_url, data={'username': 'doctor_user2', 'password': '123456'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.get(self.visit_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_password(self):
        """
            tests if a user can login with valid password
        """
        response = self.client.post(self.login_url, data={'username': 'doctor_user2', 'password': '111111'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.visit_list_url)
        """
            should redirect to login page
        """
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
