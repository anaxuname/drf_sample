from django.shortcuts import get_object_or_404
from materials.paginators import MaterialPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics
from materials.models import Course, Lesson, Subscription
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from materials.services import StripeAPI, convert_rub_to_usd
from materials.tasks import send_email_to_subscribers
from users.models import Payment
from users.permissions import IsAuthorOrReadOnly, IsModerator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialPaginator

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action == "update" or self.action == "partial_update":
            permission_classes = [IsAuthorOrReadOnly | IsModerator]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        return super().perform_create(serializer)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        base_url = "{0}://{1}".format(self.request.scheme, self.request.get_host())
        send_email_to_subscribers.delay(lesson_pk=instance.pk, base_url=base_url)
        return super().perform_create(serializer)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialPaginator


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthorOrReadOnly]


class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "подписка добавлена или удалена"},
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="id курса",
                properties={
                    "course_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="id курса", example=1),
                },
            ),
        ),
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_id).all()

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})


class CheckoutCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        stripe_api = StripeAPI()
        if course_item.stripe_price_id is None or course_item.stripe_product_id is None:
            price = stripe_api.create_product(course_item.name, convert_rub_to_usd(course_item.price_rub))
            course_item.stripe_price_id = price["id"]
            course_item.stripe_product_id = price["product"]
            course_item.save()
        base_url = "{0}://{1}".format(self.request.scheme, self.request.get_host())
        session = stripe_api.create_session(course_item.stripe_price_id, base_url, course_id)
        return Response({"url": session.url})


class SuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course, id=kwargs.get("pk"))
        Payment.objects.create(user=user, paid_course=course, paymant_amount=course.price_rub)
        return Response({"message": "success"})


class CancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response({"message": "Payment error"})
