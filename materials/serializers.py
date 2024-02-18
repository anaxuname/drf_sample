from rest_framework import serializers
from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    list_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_list_lessons(self, obj):
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    # course_detail = CourseSerializer(read_only=True, many=True, source="course")
    # count_lessons = serializers.SerializerMethodField()

    # def get_count_lessons(self, obj):
    #     return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Lesson
        fields = [
            "name",
            "description",
            "link",
            "course",
        ]
