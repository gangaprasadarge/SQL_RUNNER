from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ForgotPasswordView,
    ResetPasswordView,
    run_query,
    list_tables,
    table_info,
    health,
    user_profile,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),

    path("run-query/", run_query, name="run_query"),
    path("list-tables/", list_tables, name="list_tables"),
    path("table-info/<str:table_name>/", table_info, name="table_info"),
    path("health/", health, name="health"),
    path("profile/", user_profile, name="user_profile"),
]
