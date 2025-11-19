import os
import psycopg2
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


def get_pg_connection():
    db_url = os.environ.get("DATABASE_URL")  # Render PostgreSQL URL

    conn = psycopg2.connect(
        dbname=db_url.split("/")[-1],
        user=db_url.split("//")[1].split(":")[0],
        password=db_url.split(":")[2].split("@")[0],
        host=db_url.split("@")[1].split(":")[0],
        port=db_url.split(":")[-1].split("/")[0],
        sslmode="require"
    )
    return conn


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema='public' ORDER BY table_name;
        """)
        tables = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        return JsonResponse({"tables": tables})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name=%s
        """, (table_name,))
        columns = [{"name": c[0], "type": c[1]} for c in cur.fetchall()]

        cur.execute(f'SELECT * FROM "{table_name}" LIMIT 5')
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        sample = [dict(zip(colnames, r)) for r in rows]

        cur.close()
        conn.close()

        return JsonResponse({"columns": columns, "sample_rows": sample})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_query(request):
    query = request.data.get("query", "")

    if not query.strip():
        return JsonResponse({"error": "Empty query"}, status=400)

    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(query)

        if cur.description:
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()
            data = [dict(zip(columns, r)) for r in rows]
            cur.close()
            conn.close()
            return JsonResponse({"columns": columns, "rows": data})

        conn.commit()
        affected = cur.rowcount
        cur.close()
        conn.close()

        return JsonResponse({"message": "Query executed", "rows_affected": affected})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})
