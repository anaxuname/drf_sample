from django.urls import reverse
from materials.models import Course
from users.models import Payment, User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", full_name="Test User", phone_number="+79876543210")
        self.user.set_password("testpassword")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_user(self):
        url = reverse("users:user_create")
        data = {
            "email": "test1@example.com",
            "full_name": "Test User",
            "password": "test1234",
            "phone_number": "+79876543211",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email="test1@example.com").phone_number, "+79876543211")

    def test_get_user(self):
        url = reverse("users:user_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).email, "test@example.com")

    def test_update_user(self):
        url = reverse("users:user_update", args=[self.user.id])
        data = {
            "full_name": "Test2 User2",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.id).full_name, "Test2 User2")

    def test_delete_user(self):
        url = reverse("users:user_delete", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PaymentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.ru")
        self.user.set_password("testpassword")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.course = Course.objects.create(name="Test Course", user=self.user, description="Test description")
        self.payment = Payment.objects.create(
            user=self.user, date="2022-01-01", paid_course=self.course, paymant_amount=10
        )

    def test_get_payment(self):
        url = reverse("users:payment_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get(pk=self.payment.id).user, self.user)
