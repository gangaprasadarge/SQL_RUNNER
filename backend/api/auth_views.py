from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class SignupView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            return Response({"error": "Missing fields"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"}, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return Response({"success": True, "id": user.id}, status=201)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "name": user.first_name,
                "email": user.email
            }
        }, status=200)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"success": True})

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            "Reset Password",
            f"Click below to reset your password:\n\n{reset_link}\n\nIf you didn't request this, ignore the email.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )

        return Response({"success": True})


class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response({"error": "New password required"}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid reset link"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"success": True})
