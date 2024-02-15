from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Course name")
    preview_course = models.ImageField(upload_to="course", blank=True, null=True, verbose_name="Course image")
    description = models.TextField(verbose_name="Course description")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Lesson name")
    preview_lesson = models.ImageField(upload_to="course", blank=True, null=True, verbose_name="Lesson image")
    description = models.TextField(verbose_name="Lesson description")
    link = models.CharField(max_length=200, verbose_name="Lesson link")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course pk")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
