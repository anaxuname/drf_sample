from django.urls import path
from users.apps import UsersConfig
from users.views import (
    PaymentListView,
    UserCreateView,
    UserDeleteView,
    UserRetrieveView,
    UserUpdateView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentListView.as_view(), name="payment_list"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("retrieve/<int:pk>/", UserRetrieveView.as_view(), name="user_retrieve"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
