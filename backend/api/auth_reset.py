from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import random, json

OTP_STORE = {}   # temp store {username: otp}

@csrf_exempt
def send_reset_otp(request):
    data = json.loads(request.body)
    username = data.get("username")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    otp = random.randint(100000, 999999)
    OTP_STORE[username] = otp

    print("RESET OTP:", otp)

    return JsonResponse({"success": True, "message": "OTP Sent"})

@csrf_exempt
def verify_reset_otp(request):
    data = json.loads(request.body)
    username = data.get("username")
    otp = data.get("otp")

    if OTP_STORE.get(username) != int(otp):
        return JsonResponse({"error": "Invalid OTP"}, status=400)

    return JsonResponse({"success": True})

@csrf_exempt
def reset_password(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    user.password = make_password(password)
    user.save()

    OTP_STORE.pop(username, None)

    return JsonResponse({"success": True, "message": "Password updated successfully"})
