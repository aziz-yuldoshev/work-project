# Django CRM — Customer Relationship Management

A web-based Customer Relationship Management (CRM) system built with Python and Django. The application helps manage customers, orders, and products through a centralized dashboard.

## 🚀 Features

- 📊 Dashboard for managing business data
- 👥 Customer management
- 📦 Order management
- 🛍️ Product management
- 🔍 Customer, order, and product detail pages
- ✏️ Create, edit, and delete operations
- 🗄️ SQLite database integration
- 🧩 Django-based modular architecture

## 🛠️ Technologies

- **Python**
- **Django**
- **SQLite**
- **HTML**
- **CSS**
- **Git & GitHub**

## 📁 Project Structure

```text
crm_project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── crm/
│   ├── migrations/
│   ├── templates/
│   │   └── crm/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── .gitignore
└── manage.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aziz-yuldoshev/work-project.git
cd work-project
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows CMD:**

```cmd
venv\Scripts\activate
```

### 4. Install Django

```bash
python -m pip install django
```

### 5. Configure the secret key

Set the `DJANGO_SECRET_KEY` environment variable before running the project.

**Windows CMD:**

```cmd
set DJANGO_SECRET_KEY=your-secret-key
```

Use your own secret key. Never publish real secret keys or passwords in the repository.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/

## 🔐 Security Notes

- Secret keys should be stored in environment variables.
- Database files and virtual environments should not be committed.
- Do not publish passwords, API keys, or private customer data.
- `DEBUG = True` is intended for local development, not production deployment.

## 🎯 Project Purpose

This project demonstrates practical experience with Django application structure, database models, URL routing, templates, and CRUD operations.

## 👨‍💻 Author

**Aziz Yuldoshev**

GitHub: [@aziz-yuldoshev](https://github.com/aziz-yuldoshev)

## 📄 License

This project is available for learning and portfolio demonstration. A formal license can be added if the project is distributed publicly.
