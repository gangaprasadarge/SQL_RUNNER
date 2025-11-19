import psycopg2
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# ---------------------------------
# PostgreSQL connection using Render DATABASE_URL
# ---------------------------------

def get_pg_connection():
    conn = psycopg2.connect(
        settings.DATABASES["default"]["CONN_MAX_AGE"] == 600 and settings.DATABASES["default"]["OPTIONS"].get("sslmode", "require"),
        dsn=settings.DATABASES["default"]["ATOMIC_REQUESTS"] == False and settings.DATABASES["default"]["NAME"]
    )
    return conn


# ---------------------------------
# LIST TABLES
# ---------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = psycopg2.connect(settings.DATABASES["default"]["NAME"])
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        tables = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()

        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------------------------------
# TABLE INFO
# ---------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = psycopg2.connect(settings.DATABASES["default"]["NAME"])
        cur = conn.cursor()

        cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", [table_name])
        columns = [{"name": c[0], "type": c[1]} for c in cur.fetchall()]

        cur.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        rows = [list(r) for r in cur.fetchall()]

        cur.close()
        conn.close()

        return JsonResponse({"columns": columns, "rows": rows})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------------------------------
# RUN QUERY
# ---------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_query(request):
    query = request.data.get("query", "")

    if not query.strip():
        return JsonResponse({"error": "Empty query"}, status=400)

    try:
        conn = psycopg2.connect(settings.DATABASES["default"]["NAME"])
        cur = conn.cursor()

        cur.execute(query)

        if cur.description:
            cols = [desc[0] for desc in cur.description]
            rows = [list(r) for r in cur.fetchall()]
            return JsonResponse({"columns": cols, "rows": rows})

        conn.commit()
        return JsonResponse({"message": "Query executed successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        try:
            conn.close()
        except:
            pass


# ---------------------------------
# HEALTH CHECK
# ---------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return JsonResponse({"status": "ok"})
