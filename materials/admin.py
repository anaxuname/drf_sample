from django.contrib import admin

from materials.models import Course, Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "price_rub", "user")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "link", "user")
