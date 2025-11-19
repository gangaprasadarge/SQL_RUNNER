import psycopg2
from psycopg2.extras import RealDictCursor

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


# ==========================
# PostgreSQL CONNECTION
# ==========================

import dj_database_url
DB = dj_database_url.parse(settings.DATABASES["default"]["NAME"])


def get_pg_conn():
    return psycopg2.connect(
        dbname=DB["dbname"],
        user=DB["user"],
        password=DB["password"],
        host=DB["host"],
        port=DB["port"],
        sslmode="require",
        cursor_factory=RealDictCursor
    )


# ==========================
# AUTH APIs
# ==========================

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if not (name and email and password):
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(username=email).exists():
        return Response({"error": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=email, email=email, password=password, first_name=name
    )

    return Response({"success": True, "message": "Account created"})


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(username=email, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {"id": user.id, "email": user.email, "name": user.first_name}
    })


# ==========================
# SQL RUNNER — RUN QUERY
# ==========================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_query(request):
    query = request.data.get("query", "")

    if query.strip() == "":
        return JsonResponse({"error": "Empty query"}, status=400)

    try:
        conn = get_pg_conn()
        cur = conn.cursor()

        cur.execute(query)

        if cur.description:
            rows = cur.fetchall()
            columns = [col.name for col in cur.description]
            return JsonResponse({"columns": columns, "rows": rows})

        conn.commit()
        return JsonResponse({"message": "Query executed"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        conn.close()


# ==========================
# TABLE LIST
# ==========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = get_pg_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name;
        """)

        tables = [row["table_name"] for row in cur.fetchall()]
        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        conn.close()


# ==========================
# TABLE INFO (schema + sample rows)
# ==========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_pg_conn()
        cur = conn.cursor()

        # Columns
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
        """, (table_name,))
        columns = cur.fetchall()

        # Sample rows
        cur.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        sample_rows = cur.fetchall()

        return JsonResponse({
            "columns": columns,
            "sample_rows": sample_rows
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        conn.close()


# ==========================
# USER PROFILE
# ==========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "name": user.first_name
    })


# ==========================
# HEALTH CHECK
# ==========================

@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})
