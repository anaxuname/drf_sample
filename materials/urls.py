from materials.views import CourseViewSet
from .apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

app_name = MaterialsConfig.name


router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [] + router.urls
