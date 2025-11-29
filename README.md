# Vehicle Management API (Django + REST Framework)

A Vehicle Management System built using **Django**, **Django REST Framework**, and **SQLite**.  
This project demonstrates secure CRUD operations, role-based access control, XSS protection, and custom middleware.

---

## Features

### Vehicle CRUD
- Vehicle Number (Alphanumeric)
- Vehicle Type (Two / Three / Four wheelers)
- Vehicle Model
- Vehicle Description

### Role-Based Access
| Role         | Permissions                     |
|--------------|----------------------------------|
| Super Admin  | Create, Read, Update, Delete     |
| Admin        | Read, Update                     |
| User         | Read Only                        |

### Security
- XSS protection using **Bleach**
- Custom **IP filtering** middleware
- Validations for all fields

### Database
- Uses **SQLite** (default Django database)

---

## 📦 Installation & Setup

### 1️ Create virtual environment
python -m venv vechicle_env
vechicle_env\Scripts\activate
pip install -r requirements.txt

### 2️ Install dependencies
pip install -r requirements.txt

### 3️ Apply migrations
python manage.py makemigrations
python manage.py migrate

### 4️ Create admin user
python manage.py createsuperuser

### 5️ Run server
python manage.py runserver

### Vehicle Endpoints

| Method | URL                 | Description                  |
| ------ | ------------------- | ---------------------------- |
| GET    | /api/vehicles/      | List all vehicles            |
| POST   | /api/vehicles/      | Create vehicle (Super Admin) |
| GET    | /api/vehicles/{id}/ | Retrieve vehicle             |
| PUT    | /api/vehicles/{id}/ | Update (Admin, Super Admin)  |
| PATCH  | /api/vehicles/{id}/ | Partial update               |
| DELETE | /api/vehicles/{id}/ | Delete (Super Admin)         |

