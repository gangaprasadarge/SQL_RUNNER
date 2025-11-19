import psycopg2
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import dj_database_url


# ==========================
#  POSTGRES CONNECTION
# ==========================
def get_pg_connection():
    """Create PostgreSQL connection using DATABASE_URL."""
    
    # Render automatically provides DATABASE_URL, so use that
    db_url = settings.DATABASES["default"]["URL"]

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


# ==========================
#  LIST TABLES
# ==========================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tables(request):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==========================
#  TABLE INFO
# ==========================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        # columns
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
        """, [table_name])

        columns = [{"name": col[0], "type": col[1]} for col in cur.fetchall()]

        # sample rows
        cur.execute(f'SELECT * FROM "{table_name}" LIMIT 5')
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        sample_data = [dict(zip(colnames, row)) for row in rows]

        cur.close()
        conn.close()

        return JsonResponse({"columns": columns, "sample_rows": sample_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ==========================
#  RUN QUERY
# ==========================
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

        # SELECT queries return results
        if cur.description:
            columns = [col[0] for col in cur.description]
            rows = cur.fetchall()
            data = [dict(zip(columns, row)) for row in rows]

            cur.close()
            conn.close()

            return JsonResponse({"columns": columns, "rows": data})

        # INSERT, UPDATE, DELETE
        conn.commit()
        affected = cur.rowcount

        cur.close()
        conn.close()

        return JsonResponse({"message": "Query executed", "rows_affected": affected})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ==========================
#  HEALTH CHECK
# ==========================
@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})
