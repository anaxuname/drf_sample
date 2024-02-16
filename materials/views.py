from materials.serializers import CourseSerializer, LessonsSerializer
from rest_framework import viewsets, generics
from materials.models import Course, Lesson


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonsSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonsSerializer
    queryset = Lesson.objects.all()
