from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    signup,
    login,
    forgot_password,
    reset_password,
    run_query,
    list_tables,
    table_info,
    health,
    user_profile,
)

urlpatterns = [

    # ---------- AUTH ----------
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path("reset-password/<str:uid>/<str:token>/", reset_password, name="reset-password"),
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
