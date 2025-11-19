from django.urls import path
from .auth_views import (
    SignupView,
    LoginView,
    ForgotPasswordView,
    ResetPasswordView,
)
from .views import (
    run_query,
    list_tables,
    table_info,
    health,
)
from .views_profile import user_profile

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(), name="reset_password"),

    path("run-query/", run_query, name="run_query"),
    path("list-tables/", list_tables, name="list_tables"),
    path("table-info/<str:table_name>/", table_info, name="table_info"),
    path("health/", health, name="health"),
    path("profile/", user_profile, name="user_profile"),
]
