import psycopg2
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import dj_database_url


# ======================================
# PostgreSQL CONNECTION
# ======================================

def get_pg_connection():
    db = dj_database_url.parse(settings.DATABASES['default']['NAME'])

    return psycopg2.connect(
        dbname=db['dbname'],
        user=db['user'],
        password=db['password'],
        host=db['host'],
        port=db['port'],
        sslmode="require"
    )


# ======================================
# LIST TABLES
# ======================================

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
        """)

        tables = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return JsonResponse({"tables": tables})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ======================================
# RUN SQL QUERY
# ======================================

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

        # Query returns rows
        if cur.description:
            columns = [c.name for c in cur.description]
            rows = cur.fetchall()

            result_rows = [
                {columns[i]: row[i] for i in range(len(columns))}
                for row in rows
            ]

            return JsonResponse({"columns": columns, "rows": result_rows})

        else:
            conn.commit()
            return JsonResponse({"message": "Query executed."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    finally:
        cur.close()
        conn.close()


# ======================================
# TABLE INFO
# ======================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def table_info(request, table_name):
    try:
        conn = get_pg_connection()
        cur = conn.cursor()

        # Get columns
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
        """, [table_name])

        columns = [{"name": c[0], "type": c[1]} for c in cur.fetchall()]

        # Sample rows
        cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
        rows = cur.fetchall()

        sample_rows = []
        col_names = [desc[0] for desc in cur.description]

        for row in rows:
            sample_rows.append(
                {col_names[i]: row[i] for i in range(len(col_names))}
            )

        return JsonResponse({"columns": columns, "sample_rows": sample_rows})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        cur.close()
        conn.close()
