from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_views import SignupView, LoginView, ForgotPasswordView, ResetPasswordView
from .views import run_query, list_tables, table_info, health
from .views_profile import user_profile


urlpatterns = [

    # ---------- AUTH ----------
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(), name="reset-password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # ---------- USER PROFILE ----------
    path("profile/", user_profile, name="profile"),

    # ---------- SQL RUNNER ----------
    path("run_query/", run_query, name="run-query"),
    path("tables/", list_tables, name="table-list"),
    path("table_info/<str:table_name>/", table_info, name="table-info"),

    # ---------- HEALTH ----------
    path("", health, name="root-health"),
    path("health/", health, name="health"),
]
