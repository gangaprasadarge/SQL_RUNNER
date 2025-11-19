import os
import django
from django.conf import settings
from django.core.management import call_command
from django.db.utils import OperationalError
import time

# --- Configure Django Settings ---
# This ensures that Django's environment is set up so manage.py commands can run
if not settings.configured:
    # Replace 'sqlrunner' with the actual name of your Django project's settings module
    # e.g., if your project is in a folder named 'myproject', it would be 'myproject.settings'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqlrunner.settings") 
    django.setup()

def initialize_database():
    print("Attempting to initialize database...")

    # --- 1. Run Django Migrations ---
    # This command will create all your application's tables (in PostgreSQL on Render, SQLite locally)
    # It also handles creating Django's built-in tables (auth, admin, sessions, etc.)
    max_retries = 5
    for i in range(max_retries):
        try:
            print(f"Running Django migrations (Attempt {i+1}/{max_retries})...")
            call_command('migrate')
            print("Django migrations completed successfully.")
            break # Exit loop if migrations succeed
        except OperationalError as e:
            print(f"Database not ready yet or connection error: {e}")
            if i < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Max retries reached. Migrations failed.")
                raise # Re-raise the exception if all retries fail
        except Exception as e:
            print(f"An unexpected error occurred during migrations: {e}")
            raise # Re-raise for other errors

    # --- 2. Create Superuser (TEMPORARY - REMOVE AFTER ONE USE FOR SECURITY) ---
    # This section is for creating an admin user if you cannot use the shell.
    # It should be REMOVED from this script immediately after your superuser is created.
    # Leaving it in production is a significant security risk.
    print("\n--- WARNING: Superuser creation code is for initial setup ONLY ---")
    print("--- REMOVE THIS SECTION IMMEDIATELY AFTER FIRST SUCCESSFUL RUN ---")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    superuser_username = os.environ.get("SUPERUSER_USERNAME", "admin")
    superuser_email = os.environ.get("SUPERUSER_EMAIL", "admin@example.com")
    # For actual production, DO NOT hardcode a password here.
    # Use an environment variable and ensure it's removed/changed after first use.
    superuser_password = os.environ.get("SUPERUSER_PASSWORD", "a_very_strong_temp_password_123!") 

    if not User.objects.filter(username=superuser_username).exists():
        try:
            print(f"Creating superuser '{superuser_username}'...")
            User.objects.create_superuser(
                username=superuser_username,
                email=superuser_email,
                password=superuser_password
            )
            print(f"Superuser '{superuser_username}' created successfully. CHANGE THIS PASSWORD IMMEDIATELY!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print(f"Superuser '{superuser_username}' already exists.")
    print("--- END OF TEMPORARY SUPERUSER SECTION ---\n")


    # --- Placeholder for Initial Data (Optional) ---
    # If you have specific initial data you need, you would create Django fixtures
    # or write a custom Django management command for data seeding.
    # Manual SQL inserts like your original script are generally not done this way
    # with Django's ORM.

    print("Database initialization script finished.")


if __name__ == "__main__":
    initialize_database()

