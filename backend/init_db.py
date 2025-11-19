import os
import django
from django.core.management import call_command

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqlrunner.settings")
django.setup()

def initialize_database():
    print("Starting database initialization...")

    # Run migrations (safe for Render deployment)
    try:
        print("Applying migrations...")
        call_command("migrate")
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error during migrations: {e}")

    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()
