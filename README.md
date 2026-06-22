# Employee Management System

A full-stack Employee Management System built using **Python, Flask, MySQL, Bootstrap, and Pandas**. The application provides secure employee record management with authentication, CRUD operations, dashboard analytics, search functionality, REST API integration, and Excel export capabilities.

---

# Features

## Authentication & Security

* Secure admin login system
* Password hashing using Werkzeug
* Session-based authentication
* Protected routes for authorized users only

## Employee Management

* Add Employee
* View Employee Directory
* Update Employee Details
* Delete Employee Records
* Search Employees by Name or Department

## Dashboard Analytics

* Total Employees Count
* Total Departments Count
* Average Employee Salary

## REST API

* Retrieve employee records in JSON format
* API endpoint for employee data access

## Export Functionality

* Export employee records to Excel (.xlsx)
* Preserves phone numbers and date formats

## User Interface

* Responsive Bootstrap design
* Dashboard cards and analytics
* Modern employee directory
* Search and filtering support

---

# Technology Stack

## Backend

* Python 3
* Flask

## Database

* MySQL

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2 Templates

## Libraries Used

* Flask
* Flask-MySQLdb
* mysqlclient
* Pandas
* OpenPyXL
* Werkzeug

---

# Project Structure

```text
EmployeeManagementSystem
│
├── app.py
│
├── templates
│   ├── login.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── add_employee.html
│   └── edit_employee.html
│
├── static
│   ├── css
│   └── js
│
├── employees.xlsx
├── requirements.txt
└── README.md
```

---

# Database Design

## Users Table

```sql
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);
```

## Employees Table

```sql
CREATE TABLE employees(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    joining_date DATE
);
```

---

# Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/Employee-Management-System.git
cd Employee-Management-System
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure MySQL

Create database:

```sql
CREATE DATABASE employee_management;
```

Select database:

```sql
USE employee_management;
```

Create tables using the SQL scripts provided above.

---

## 5. Create Admin User

Generate a password hash using:

```python
from werkzeug.security import generate_password_hash

print(generate_password_hash("admin123"))
```

Insert admin user:

```sql
INSERT INTO users(username,password,role)
VALUES(
'admin',
'HASHED_PASSWORD',
'admin'
);
```

---

## 6. Configure Database Credentials

Inside `app.py` update:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YOUR_PASSWORD'
app.config['MYSQL_DB'] = 'employee_management'
```

---

## 7. Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# API Documentation

## Get All Employees

```http
GET /api/employees
```

### Sample Response

```json
[
  {
    "id": 1,
    "name": "Harsha",
    "email": "harsha@gmail.com",
    "department": "IT"
  }
]
```

---

# Application Workflow

```text
Login
  ↓
Dashboard
  ↓
Employee Directory
  ↓
Add / Edit / Delete Employee
  ↓
Search Employees
  ↓
Export Employee Data
```

---

# Future Enhancements

* Role-Based Access Control
* Employee Profile Pictures
* Attendance Management
* Payroll Management
* Email Notifications
* Dark Mode Support
* Pagination
* Docker Deployment
* Cloud Database Integration

---

# Learning Outcomes

Through this project, the following concepts were implemented and understood:

* Flask Application Development
* MySQL Database Integration
* CRUD Operations
* Session Management
* Password Hashing
* REST API Development
* Data Export using Pandas
* Bootstrap Frontend Development
* Database Design and Queries
* Full-Stack Application Architecture

---

# Author

**Harshath K S**

* Computer Science Engineering Graduate
* Python & Software Development Enthusiast

---

# License

This project is developed for educational and portfolio purposes.
Last Updated: June 2026