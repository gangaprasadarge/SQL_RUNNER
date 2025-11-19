from django.urls import path
from .views import run_query, list_tables, table_info, health
from .auth_views import SignupView, LoginView, ForgotPasswordView, ResetPasswordView
from .views_profile import user_profile

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view()),

    path("run-query/", run_query),
    path("list-tables/", list_tables),
    path("table-info/<str:table_name>/", table_info),
    path("health/", health),
    path("profile/", user_profile),
]
