from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from rest_framework.permissions import AllowAny

from users.permissions import IsAuthorOrReadOnly, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action == "update" or self.action == "partial_update":
            permission_classes = [IsAuthorOrReadOnly | IsModerator]
        elif self.action == "create" or self.action == "destroy":
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthorOrReadOnly]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    # serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
