FROM python:3.12.10-slim

WORKDIR /app

# Copy requirements first for caching and efficient builds
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project, including backend folder and all other files
COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN python manage.py migrate && python init_db.py

CMD ["gunicorn", "sqlrunner.wsgi:application", "--bind", "0.0.0.0:8000"]
