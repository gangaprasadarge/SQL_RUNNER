import sqlite3
from pathlib import Path

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer





DB_PATH = Path(__file__).resolve().parent.parent / "sql_runner.db"


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_query(request):
    query = request.data.get("query", "")
    if not query.strip():
        return JsonResponse({"error": "empty query"}, status=400)

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(query)

        if cur.description:
            columns = [col[0] for col in cur.description]
            rows = [dict(row) for row in cur.fetchall()]
            return JsonResponse({"columns": columns, "rows": rows})

        conn.commit()
        return JsonResponse({"message": "Query executed", "rows_affected": cur.rowcount})

    except sqlite3.Error as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        try:
            conn.close()
        except:
            pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cur.fetchall()]
        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        try:
            conn.close()
        except:
            pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [{"name": r[1], "type": r[2], "pk": r[5]} for r in cur.fetchall()]

        cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
        rows = [dict(row) for row in cur.fetchall()]

        return JsonResponse({"columns": columns, "sample_rows": rows})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        try:
            conn.close()
        except:
            pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "id": user.id
    })


@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})


# TEMP USER CREATION (remove after first login)
@method_decorator(csrf_exempt, name='dispatch')
class CreateTempUser(APIView):
    def post(self, request):
        email = "argegangaprasad9515@gmail.com"
        password = "Test@12345"

        if User.objects.filter(username=email).exists():
            return Response({"error": "User already exists"}, status=400)

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name="Arge Gangaprasad",
        )

        return Response({"success": True, "message": "Temp user created!"})


from rest_framework import serializers

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True}, status=201)
    return Response(serializer.errors, status=400)
