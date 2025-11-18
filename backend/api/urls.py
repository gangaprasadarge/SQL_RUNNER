from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth_views import SignupView, LoginView, ForgotPasswordView, ResetPasswordView
from .views import run_query, list_tables, table_info, health
from .views_profile import user_profile

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("profile/", user_profile),
    path("run_query/", run_query),
    path("tables/", list_tables),
    path("table_info/<str:table_name>/", table_info),
    path("", health),
    path("health/", health),
]
