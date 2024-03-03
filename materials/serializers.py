from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    list_lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        return Subscription.objects.filter(user=self.context["request"].user, course=obj).exists()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_list_lessons(self, obj):
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    class Meta:
        model = Course
        fields = ["name", "preview_course", "description", "count_lessons", "list_lessons", "subscription"]


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(validators=[LinkValidator("link")])

    class Meta:
        model = Lesson
        fields = [
            "name",
            "description",
            "link",
            "course",
        ]
