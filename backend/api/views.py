import os
import psycopg2
import dj_database_url
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings


# ---------------------------------------------------
# POSTGRES CONNECTION (IMPORTANT)
# ---------------------------------------------------
def get_pg_connection():
    db_url = os.environ.get("DATABASE_URL")   # from Render
    config = dj_database_url.parse(db_url)

    conn = psycopg2.connect(
        dbname=config["NAME"],
        user=config["USER"],
        password=config["PASSWORD"],
        host=config["HOST"],
        port=config["PORT"],
        sslmode="require"
    )
    return conn


# ---------------------------------------------------
# LIST TABLES
# ---------------------------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name;
        """)

        tables = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------------------------------------------------
# TABLE SCHEMA
# ---------------------------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
        """, [table_name])

        columns = [{"name": c[0], "type": c[1]} for c in cur.fetchall()]

        cur.execute(f'SELECT * FROM "{table_name}" LIMIT 5')
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        data = [dict(zip(colnames, row)) for row in rows]

        cur.close()
        conn.close()

        return JsonResponse({"columns": columns, "sample_rows": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------------------------------------------------
# RUN SQL QUERY (EDITOR)
# ---------------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_query(request):
    query = request.data.get("query", "").strip()

    if not query:
        return JsonResponse({"error": "Empty query"}, status=400)

    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute(query)

        # SELECT QUERY
        if cur.description:
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()
            data = [dict(zip(columns, row)) for row in rows]

            cur.close()
            conn.close()
            return JsonResponse({"columns": columns, "rows": data})

        # INSERT/UPDATE/DELETE
        conn.commit()
        affected = cur.rowcount

        cur.close()
        conn.close()

        return JsonResponse({"message": "Query executed", "rows_affected": affected})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})
