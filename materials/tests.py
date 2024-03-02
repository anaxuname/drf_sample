from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.ru")
        self.user.set_password("testpassword")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.course = Course.objects.create(name="Test Course", user=self.user, description="Test description")
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            user=self.user,
            course=self.course,
            link="https://www.youtube.com/123",
            description="Test description",
        )

    def test_get_list_courses(self):
        response = self.client.get(reverse("materials:course-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "Test Course",
                        "preview_course": None,
                        "description": "Test description",
                        "count_lessons": self.course.lessons.count(),
                        "list_lessons": [lesson.name for lesson in self.course.lessons.all()],
                    }
                ],
            },
        )

    def test_lesson_create(self):
        data = {
            "name": "Test Lesson",
            "description": "Test description",
            "link": "https://www.youtube.com/123",
            "course": self.course.pk,
        }
        response = self.client.post(reverse("materials:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "name": "Test Lesson",
                "description": "Test description",
                "link": "https://www.youtube.com/123",
                "course": self.course.pk,
            },
        )

    def test_lesson_list(self):
        response = self.client.get(reverse("materials:lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "Test Lesson",
                        "description": "Test description",
                        "link": "https://www.youtube.com/123",
                        "course": self.course.pk,
                    }
                ],
            },
        )

    def test_lesson_detail(self):
        response = self.client.get(reverse("materials:lesson_detail", args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "name": "Test Lesson",
            "description": "Test description",
            "link": "https://www.youtube.com/123",
            "course": self.course.pk,
        }
        self.assertEqual(response.data, expected_data)

    def test_lesson_delete(self):
        response = self.client.delete(reverse("materials:lesson_delete", args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_update(self):
        data = {
            "name": "Test Lesson",
            "description": "Test description",
            "link": "https://www.youtube.com/123",
            "course": self.course.pk,
        }
        response = self.client.put(reverse("materials:lesson_update", args=[self.lesson.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "name": "Test Lesson",
                "description": "Test description",
                "link": "https://www.youtube.com/123",
                "course": self.course.pk,
            },
        )

    def test_subscribe(self):
        data = {"course_id": self.course.pk}
        response = self.client.post(reverse("materials:subscribe"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
