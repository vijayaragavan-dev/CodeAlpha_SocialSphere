# 🌐 SocialSphere

<div align="center">

### Full-Stack Social Media Platform

A modern social networking application built with **Flask**, **MySQL**, **Bootstrap**, and **JavaScript**, featuring user authentication, posts, likes, comments, profiles, and real-time social interactions.

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8+-orange?logo=mysql)](https://mysql.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

# 📌 Overview

SocialSphere is a full-stack social media platform that enables users to connect, share content, interact through comments and likes, and build their online presence through customizable profiles.

The project demonstrates modern web development practices including secure authentication, relational database design, responsive UI development, session management, and scalable backend architecture.

This project was developed as part of the **CodeAlpha Full Stack Development Internship Program**.

---

# 🚀 Live Features

### 👤 User Authentication

* User Registration
* Secure Login
* Logout Functionality
* Password Hashing using Bcrypt
* Session Management
* Remember Me Functionality

---

### 📝 Social Posts

Users can:

* Create Posts
* Edit Posts
* Delete Posts
* View Public Feed
* Upload Images
* Share Thoughts and Updates

---

### ❤️ Like System

* Like Posts
* Unlike Posts
* Real-Time Like Counter
* Prevent Duplicate Likes

---

### 💬 Comment System

Users can:

* Add Comments
* View Comments
* Delete Own Comments
* Interact with Community Posts

---

### 👥 User Profiles

Features include:

* Profile Page
* Profile Picture Support
* Bio Section
* User Information Display
* Activity Tracking

---

### 🔎 Social Feed

* Dynamic Feed Generation
* Latest Posts First
* Responsive Feed Layout
* User Activity Updates

---

### 📱 Responsive Design

* Mobile Friendly
* Tablet Friendly
* Desktop Optimized
* Bootstrap 5 UI Components

---

# 🏗️ System Architecture

```text
Client Browser
       │
       ▼
Flask Application
       │
       ▼
Business Logic Layer
       │
       ▼
MySQL Database
```

---

# 🛠️ Tech Stack

| Layer             | Technology                           |
| ----------------- | ------------------------------------ |
| Frontend          | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Backend           | Python Flask                         |
| Authentication    | Flask-Login, Flask-Bcrypt            |
| Database          | MySQL                                |
| ORM / Data Access | mysql-connector-python               |
| Security          | Flask-WTF, CSRF Protection           |
| Deployment Ready  | Render / Railway                     |
| Version Control   | Git & GitHub                         |

---

# 🔐 Security Features

### Authentication Security

* Password Hashing using Bcrypt
* Secure Session Handling
* Protected Routes
* Login Validation

### Application Security

* CSRF Protection
* SQL Injection Prevention
* Input Validation
* Secure Cookies
* XSS Protection

---

# ⚡ Performance Features

* Optimized Database Queries
* Indexed Tables
* Efficient Session Management
* Lightweight Flask Backend
* Responsive Frontend Rendering

---

# 🗄️ Database Design

The application uses MySQL as the primary relational database.

### Core Tables

```text
users
posts
likes
comments
followers
```

### Database Features

✅ Primary Keys

✅ Foreign Keys

✅ Cascading Deletes

✅ Indexed Queries

✅ Relational Integrity

---

# 📂 Project Structure

```text
SOCIALSPHERE/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── database.sql
├── .env.example
├── .gitignore
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── feed.html
│   ├── post_detail.html
│
└── uploads/
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/vijayaragavan-dev/CodeAlpha_SocialSphere.git

cd CodeAlpha_SocialSphere
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create:

```text
.env
```

Example:

```env
SECRET_KEY=your-secret-key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DB=socialsphere
```

---

## 5️⃣ Create Database

Open MySQL and execute:

```sql
CREATE DATABASE socialsphere;
```

Import:

```text
database.sql
```

using MySQL Workbench.

---

## 6️⃣ Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

# 📸 Screenshots

Add screenshots here:

```text
docs/screenshots/home.png
docs/screenshots/feed.png
docs/screenshots/profile.png
docs/screenshots/post.png
```

---

# 🎯 Key Learning Outcomes

This project demonstrates:

* Full Stack Development
* Authentication & Authorization
* Database Design
* CRUD Operations
* RESTful Routing
* Responsive UI Design
* Session Management
* Security Best Practices
* Git & GitHub Workflow

---

# 🚀 Future Enhancements

* Real-Time Chat System
* Friend Requests
* Notifications
* Story Feature
* Dark Mode
* Email Verification
* AI Content Recommendations
* Mobile Application

---

# 👨‍💻 Author

### Vijayaragavan

**Computer Science Engineering Student**

* GitHub: https://github.com/vijayaragavan-dev
* LinkedIn: Add your LinkedIn profile URL

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star on GitHub.

Built with ❤️ as part of the CodeAlpha Full Stack Development Internship Program.

</div>
