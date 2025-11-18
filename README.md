🔥 SQL Runner — Full Stack Application
React (Frontend) + Django (Backend) + SQLite + Docker

A full-stack SQL Runner application that lets users:

✔ Write SQL queries
✔ View results instantly
✔ Explore database tables
✔ Check table schema (columns, types, PK, defaults)
✔ Preview sample rows
✔ Works like an online SQL editor (Programiz SQL, SQLFiddle, etc.)

⭐ Tech Stack
Layer	Technology
Frontend	React (CodeMirror Editor + Fetch API)
Backend	Django REST Framework
Database	SQLite
Auth	JWT Authentication + Password Reset
Deployment	Docker (Frontend + Backend)
🎨 Frontend Features (React)

Beautiful SQL Query Editor

Run Query Button

Results Table

Tables Sidebar (Customers, Orders, Shippings)

On-click Table Schema View

Shows first 5 sample rows

Recent Queries list

Fully responsive modern UI

🧠 Backend Features (Django)

Execute SQL queries safely

Return results as JSON

List available tables

Get table schema

Sample row preview

JWT Authentication

Password Reset via Email

CORS Enabled

SQLite Database Integration

All errors handled properly

📁 Project Folder Structure
project/
│── backend/
│   ├── api/
│   ├── sql_runner.db
│   ├── requirements.txt
│   ├── manage.py
│   └── Dockerfile
│
│── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile

⚙️ Backend Setup (Django)
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run migrations
python manage.py migrate

3️⃣ Start the backend
python manage.py runserver


Backend runs on:
👉 http://localhost:8000

⚙️ Frontend Setup (React)
1️⃣ Install dependencies
npm install

2️⃣ Start React app
npm start


Frontend runs on:
👉 http://localhost:3000

📡 API Endpoints
Endpoint	Method	Description
/api/tables/	GET	List of all tables
/api/table/<name>/	GET	Schema + sample rows
/api/query/	POST	Execute SQL query
/api/signup/	POST	User registration
/api/login/	POST	User login (JWT)
/api/profile/	GET	Logged-in user data
/api/forgot-password/	POST	Send reset link
/api/reset-password/<uid>/<token>/	POST	Reset password
🗃 SQLite Database Included

Database file:

backend/sql_runner.db

Tables
Table Name	Purpose
Customers	Stores customer details
Orders	Stores customer orders
Shippings	Shipping details
Sample Queries
SELECT * FROM Customers;

SELECT first_name, age FROM Customers WHERE age > 25;

SELECT * FROM Orders WHERE amount >= 200;

🐳 Docker Setup
🐍 Backend Dockerfile

Located at: backend/Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

Build & Run
docker build -t sql-backend .
docker run -p 8000:8000 sql-backend

⚛ Frontend Dockerfile

Located at: frontend/Dockerfile

FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx","-g","daemon off;"]

Build & Run
docker build -t sql-frontend .
docker run -p 3000:80 sql-frontend

▶ Example API Usage
List tables
GET http://localhost:8000/api/tables/

Get table schema
GET http://localhost:8000/api/table/Customers/

Execute SQL Query
POST /api/query/
{
  "query": "SELECT * FROM Customers"
}

👤 Author
Arge Gangaprasad

B.Tech CSE — Lovely Professional University

📧 Email: argegangaprasad@gmail.com

🔗 GitHub: https://github.com/gangaprasadarge

🔗 LinkedIn: https://www.linkedin.com/in/arge-gangaprasad/
