# 🌐 SocialSphere

<div align="center">

### Modern Full-Stack Social Media Platform

A scalable social networking web application built using **Flask**, **MySQL**, **Bootstrap**, and **JavaScript**, enabling users to connect, share content, interact through likes and comments, and manage personalized profiles in a secure and responsive environment.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8+-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-black?logo=github)
![CodeAlpha](https://img.shields.io/badge/CodeAlpha-Internship-blue)

</div>

---

## 📖 Project Overview

SocialSphere is a full-stack social networking platform designed to simulate core features found in modern social media applications. The platform allows users to create accounts, publish posts, interact with content, build personal profiles, and engage with other users through a clean and intuitive interface.

The application follows a traditional multi-layer architecture with a Flask backend, MySQL database, and responsive frontend, demonstrating best practices in authentication, database design, CRUD operations, session management, and secure web application development.

This project was developed as part of the **CodeAlpha Full Stack Development Internship Program** to strengthen practical skills in full-stack software engineering and real-world application development.

---

## ✨ Core Features

### 🔐 Authentication & Authorization

* User Registration
* Secure Login & Logout
* Password Hashing with Flask-Bcrypt
* Session-Based Authentication
* Protected Application Routes
* Remember Me Functionality

### 📝 Content Management

* Create Posts
* Edit Posts
* Delete Posts
* Image Upload Support
* Dynamic Content Feed

### ❤️ Social Interactions

* Like & Unlike Posts
* Comment on Posts
* Community Engagement Features
* Interaction Tracking

### 👤 User Profiles

* Personalized User Profiles
* Profile Picture Upload
* Bio & Profile Information
* User Activity Display

### 🔎 Search System

* User Search Functionality
* Discover Community Members
* Quick Profile Navigation

### 📱 Responsive User Interface

* Mobile-First Design
* Tablet Compatibility
* Desktop Optimization
* Bootstrap 5 Components

---

## 🏛️ System Architecture

```text
Client Browser
      │
      ▼
Frontend Layer
(HTML • CSS • JavaScript • Bootstrap)
      │
      ▼
Flask Application Layer
(Authentication • Business Logic • Routing)
      │
      ▼
Data Access Layer
(mysql-connector-python)
      │
      ▼
MySQL Database
(Users • Posts • Likes • Comments)
```

---

## 🛠️ Technology Stack

| Category         | Technologies                         |
| ---------------- | ------------------------------------ |
| Frontend         | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Backend          | Python, Flask                        |
| Database         | MySQL                                |
| Authentication   | Flask-Login, Flask-Bcrypt            |
| Security         | Flask-WTF, CSRF Protection           |
| Configuration    | Python-Dotenv                        |
| Data Access      | mysql-connector-python               |
| Version Control  | Git, GitHub                          |
| Deployment Ready | Render, Railway                      |

---

## ⚙️ Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/vijayaragavan-dev/CodeAlpha_SocialSphere.git

cd CodeAlpha_SocialSphere
```

### 2. Setup MySQL Database

Run the database schema:

```bash
mysql -u root -p < database.sql
```

### 3. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Update the values inside `.env`:

```env
SECRET_KEY=your-secret-key

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DB=socialsphere
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

Application URL:

```text
http://localhost:5000
```

---

## 🗄️ Database Design

Core Entities:

```text
users
posts
likes
comments
followers
```

Database Features:

✅ Relational Database Design

✅ Primary & Foreign Keys

✅ Cascading Deletes

✅ Indexed Queries

✅ Data Integrity Constraints

---

## 🔒 Security Features

* Password Hashing using Flask-Bcrypt
* Session-Based Authentication
* CSRF Protection
* Secure Route Protection
* Input Validation & Sanitization
* Environment Variable Management
* SQL Injection Prevention Techniques

---

## 📚 Learning Outcomes

This project provided practical experience in:

* Full Stack Web Development
* Flask Application Architecture
* MySQL Database Design
* Authentication & Authorization
* CRUD Operations
* Responsive UI Development
* Secure Web Application Design
* Git & GitHub Workflow
* Real-World Project Development

---

## 👨‍💻 Author

**Vijayaragavan U**

Computer Science & Engineering Student

GitHub: https://github.com/vijayaragavan-dev

LinkedIn: https://www.linkedin.com/in/vijaya-ragavan-ki10052007

---

## 📄 License

This project was developed for educational purposes as part of the CodeAlpha Full Stack Development Internship Program.

---

<div align="center">

⭐ If you found this project useful, consider giving the repository a star.

Built with ❤️ using Flask and MySQL.

</div>
